"""워커 설정. 모든 값은 환경변수(.env)에서 읽는다."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Django 백엔드 API (워커가 폴링할 대상)
BACKEND_URL = os.environ["BACKEND_URL"].rstrip("/")

# 로컬 ComfyUI HTTP API
COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188").rstrip("/")

# 워커 인증 토큰 (Django 워커 엔드포인트 보호용, 미설정 시 헤더 생략)
WORKER_TOKEN = os.environ.get("WORKER_TOKEN", "")

# 작업이 없을 때 다음 폴링까지 대기(초)
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "3"))

# 폴링/전송 에러 후 재시도 대기(초)
ERROR_BACKOFF = int(os.environ.get("ERROR_BACKOFF", "5"))

# ComfyUI 생성 1건 최대 대기(초). 초과 시 실패 처리 → 무한 대기 방지
GENERATE_TIMEOUT = int(os.environ.get("GENERATE_TIMEOUT", "600"))

# HTTP 요청 타임아웃(초)
HTTP_TIMEOUT = int(os.environ.get("HTTP_TIMEOUT", "60"))

# 워크플로우 JSON 디렉터리 (ComfyUI API 포맷)
WORKFLOW_DIR = Path(os.environ.get("WORKFLOW_DIR", BASE_DIR / "workflows"))

# 스타일별 워크플로우와, 워커가 값을 주입/추출할 노드 번호
#   load_image_node      : LoadImage        → 입력 파일명 주입
#   positive_prompt_node : CLIPTextEncode   → 성별 프롬프트 보강
#   save_image_node      : SaveImage        → 결과 이미지 추출
WORKFLOW_CONFIG = {
    "ghibli": {
        "file": "ghibli.json",
        "load_image_node": "10",
        "positive_prompt_node": "18",
        "save_image_node": "42",
    },
    "anime2d": {
        "file": "anime2d.json",
        "load_image_node": "10",
        "positive_prompt_node": "18",
        "save_image_node": "42",
    },
    # Django STYLE_CHOICES 에는 pixar / zepeto 도 있으나 전용 워크플로우 미구현.
    # 매핑이 없으면 DEFAULT_STYLE 로 대체되며 그 사실을 로그로 남긴다.
}

DEFAULT_STYLE = "anime2d"
