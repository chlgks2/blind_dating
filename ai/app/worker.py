"""
GPU 워커 — Django 작업 큐를 폴링해 ComfyUI로 이미지를 생성하고 결과를 반환한다.

흐름:
    GET  {BACKEND_URL}/api/accounts/ai/next-job/        작업 선점
      → S3 원본 다운로드
      → POST {COMFYUI_URL}/upload/image                 ComfyUI input 폴더로 업로드
      → POST {COMFYUI_URL}/prompt                       워크플로우 실행 요청
      → GET  {COMFYUI_URL}/history/{prompt_id}          완료 폴링 (타임아웃 있음)
      → GET  {COMFYUI_URL}/view                         결과 이미지 수집
    POST {BACKEND_URL}/api/accounts/ai/complete-upload/  결과 전송 (실패 시 /ai/complete/ 로 에러 통보)

단독 실행:
    python -m app.worker
"""

import json
import logging
import random
import time
import uuid

import requests

from . import config

log = logging.getLogger("worker")

SEED_MAX = 2**32 - 1


def _headers() -> dict:
    """워커 전용 인증 헤더. 토큰이 없으면 헤더를 붙이지 않는다."""
    return {"X-Worker-Token": config.WORKER_TOKEN} if config.WORKER_TOKEN else {}


# ---------------------------------------------------------------- ComfyUI


def load_workflow(filename: str) -> dict:
    """워크플로우 JSON을 로드하고 모든 seed를 랜덤화한다.

    seed를 고정하면 ComfyUI가 동일 prompt를 history 캐시로 판단해
    이전 결과를 그대로 반환한다. 사용자마다 다른 결과를 내려면 필수.
    """
    path = config.WORKFLOW_DIR / filename
    with open(path, encoding="utf-8") as f:
        workflow = json.load(f)

    for node in workflow.values():
        if "seed" in node.get("inputs", {}):
            node["inputs"]["seed"] = random.randint(1, SEED_MAX)

    return workflow


def upload_input_image(image_bytes: bytes, filename: str) -> str:
    """ComfyUI input 폴더에 이미지를 올리고, ComfyUI가 부여한 파일명을 반환."""
    resp = requests.post(
        f"{config.COMFYUI_URL}/upload/image",
        files={"image": (filename, image_bytes, "image/jpeg")},
        timeout=config.HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["name"]


def apply_gender_prompt(workflow: dict, node_id: str, gender: str) -> None:
    """성별에 따라 positive 프롬프트를 보강한다.

    gender 가 없거나 인식할 수 없으면 프롬프트를 건드리지 않는다.
    (예전 구현은 기본값을 'M' 으로 두어, 백엔드가 gender를 보내지 않으면
     모든 사용자에게 '1boy' 가 붙는 문제가 있었다.)
    """
    if node_id not in workflow or gender not in ("M", "F"):
        return

    text = workflow[node_id]["inputs"].get("text", "")
    if "1girl" in text or "1boy" in text:
        return

    word = "1girl, beautiful detailed face" if gender == "F" else "1boy, handsome face"
    workflow[node_id]["inputs"]["text"] = f"{word}, {text}"


def wait_for_result(prompt_id: str) -> dict:
    """생성 완료까지 history를 폴링한다. GENERATE_TIMEOUT 초과 시 예외."""
    deadline = time.monotonic() + config.GENERATE_TIMEOUT

    while time.monotonic() < deadline:
        resp = requests.get(
            f"{config.COMFYUI_URL}/history/{prompt_id}", timeout=config.HTTP_TIMEOUT
        )
        resp.raise_for_status()
        history = resp.json()

        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI 실행 오류: {status.get('messages')}")
            return entry

        time.sleep(1)

    raise TimeoutError(f"생성 대기 시간 초과 ({config.GENERATE_TIMEOUT}s)")


def fetch_output_image(entry: dict, save_node: str) -> bytes:
    """history 응답에서 SaveImage 노드의 결과 이미지를 내려받는다."""
    outputs = entry.get("outputs", {})
    if save_node not in outputs:
        raise KeyError(
            f"SaveImage 노드 {save_node} 출력 없음. 실제 출력 노드: {list(outputs)}"
        )

    info = outputs[save_node]["images"][0]
    resp = requests.get(
        f"{config.COMFYUI_URL}/view",
        params={
            "filename": info["filename"],
            "subfolder": info["subfolder"],
            "type": info["type"],
        },
        timeout=config.HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.content


def generate(style: str, input_filename: str, gender: str) -> bytes:
    """스타일에 맞는 워크플로우로 이미지를 생성해 bytes로 반환."""
    cfg = config.WORKFLOW_CONFIG.get(style)
    if cfg is None:
        log.warning("'%s' 전용 워크플로우 없음 → 기본(%s) 사용", style, config.DEFAULT_STYLE)
        cfg = config.WORKFLOW_CONFIG[config.DEFAULT_STYLE]

    workflow = load_workflow(cfg["file"])
    workflow[cfg["load_image_node"]]["inputs"]["image"] = input_filename
    apply_gender_prompt(workflow, cfg["positive_prompt_node"], gender)

    resp = requests.post(
        f"{config.COMFYUI_URL}/prompt",
        json={"prompt": workflow, "client_id": str(uuid.uuid4())},
        timeout=config.HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    prompt_id = resp.json()["prompt_id"]
    log.info("ComfyUI 실행 요청: workflow=%s prompt_id=%s", cfg["file"], prompt_id)

    entry = wait_for_result(prompt_id)
    return fetch_output_image(entry, cfg["save_image_node"])


# ---------------------------------------------------------------- Django


def fetch_next_job() -> dict | None:
    """대기 중인 작업 1건을 선점한다. 없으면 None."""
    resp = requests.get(
        f"{config.BACKEND_URL}/api/accounts/ai/next-job/",
        headers=_headers(),
        timeout=config.HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json().get("job")


def report_success(job_id: int, image_bytes: bytes) -> None:
    """결과 이미지를 백엔드로 전송한다. S3 업로드는 백엔드가 수행."""
    resp = requests.post(
        f"{config.BACKEND_URL}/api/accounts/ai/complete-upload/",
        headers=_headers(),
        data={"job_id": job_id},
        files={"result": (f"result_{job_id}.png", image_bytes, "image/png")},
        timeout=config.HTTP_TIMEOUT,
    )
    resp.raise_for_status()


def report_failure(job_id: int, message: str) -> None:
    """실패를 통보해 job이 processing 상태로 남지 않게 한다."""
    try:
        requests.post(
            f"{config.BACKEND_URL}/api/accounts/ai/complete/",
            headers=_headers(),
            json={"job_id": job_id, "error": message[:500]},
            timeout=config.HTTP_TIMEOUT,
        ).raise_for_status()
    except requests.RequestException:
        log.exception("실패 통보 자체가 실패 (job %s)", job_id)


# ---------------------------------------------------------------- 루프


def process_job(job: dict) -> None:
    job_id = job["job_id"]
    style = job.get("style", config.DEFAULT_STYLE)
    gender = job.get("gender")  # 백엔드가 아직 내려주지 않으면 None → 프롬프트 미보강

    log.info("[job %s] 시작 style=%s gender=%s", job_id, style, gender)
    started = time.monotonic()

    try:
        original = requests.get(job["original_url"], timeout=config.HTTP_TIMEOUT)
        original.raise_for_status()

        input_name = upload_input_image(original.content, f"input_{job_id}.jpg")
        result = generate(style, input_name, gender)

        report_success(job_id, result)
        log.info("[job %s] 완료 (%.1fs)", job_id, time.monotonic() - started)

    except Exception as e:  # noqa: BLE001 — 어떤 예외든 job을 failed로 마감해야 한다
        log.exception("[job %s] 실패", job_id)
        report_failure(job_id, f"{type(e).__name__}: {e}")


def run_forever() -> None:
    log.info("워커 시작 backend=%s comfyui=%s", config.BACKEND_URL, config.COMFYUI_URL)
    log.info("활성 스타일: %s (기본 %s)", list(config.WORKFLOW_CONFIG), config.DEFAULT_STYLE)

    while True:
        try:
            job = fetch_next_job()
            if job:
                process_job(job)
            else:
                time.sleep(config.POLL_INTERVAL)
        except requests.RequestException:
            log.exception("폴링 실패 — %ss 후 재시도", config.ERROR_BACKOFF)
            time.sleep(config.ERROR_BACKOFF)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
    )
    run_forever()
