"""
FastAPI 래퍼 — GPU 서버의 상태 확인 엔드포인트를 제공하고,
백그라운드 스레드에서 워커 폴링 루프를 실행한다.

워커 루프 자체는 app/worker.py 에 있으며 단독 실행도 가능하다.
FastAPI를 두는 이유는 GPU 서버의 생존/처리 상태를 외부에서 확인하기 위한 것으로,
작업 수신은 여전히 워커가 Django를 폴링하는 방식(pull)이다.

실행:
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

import logging
import threading
import time
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI

from . import config, worker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
)
log = logging.getLogger("main")

STARTED_AT = time.time()
_worker_thread: threading.Thread | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _worker_thread
    _worker_thread = threading.Thread(target=worker.run_forever, daemon=True)
    _worker_thread.start()
    log.info("워커 스레드 시작")
    yield
    log.info("종료")


app = FastAPI(title="Blind Dating GPU Worker", lifespan=lifespan)


@app.get("/health")
def health():
    """워커 스레드와 ComfyUI 연결 상태를 함께 확인한다."""
    comfy_ok = False
    try:
        r = requests.get(f"{config.COMFYUI_URL}/system_stats", timeout=3)
        comfy_ok = r.ok
    except requests.RequestException:
        pass

    alive = bool(_worker_thread and _worker_thread.is_alive())
    return {
        "status": "ok" if (alive and comfy_ok) else "degraded",
        "worker_alive": alive,
        "comfyui_reachable": comfy_ok,
        "uptime_sec": round(time.time() - STARTED_AT, 1),
    }


@app.get("/config")
def current_config():
    """현재 로드된 스타일 매핑 확인용. 시크릿은 노출하지 않는다."""
    return {
        "backend_url": config.BACKEND_URL,
        "comfyui_url": config.COMFYUI_URL,
        "styles": list(config.WORKFLOW_CONFIG),
        "default_style": config.DEFAULT_STYLE,
        "poll_interval": config.POLL_INTERVAL,
        "generate_timeout": config.GENERATE_TIMEOUT,
    }
