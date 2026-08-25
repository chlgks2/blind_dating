#!/usr/bin/env python3
"""
백엔드 없이 ComfyUI 파이프라인만 단독 검증하는 스크립트.

워커 개발 초기에 "워크플로우 JSON을 API로 실행 → 결과 이미지 회수" 경로만
따로 확인하기 위해 사용했다.

사용법:
    # ComfyUI input 폴더에 이미지를 두고 파일명을 지정
    python scripts/run_local.py --style ghibli --image sample.jpg --out result.png
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config, worker  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="ghibli", choices=list(config.WORKFLOW_CONFIG))
    ap.add_argument("--image", required=True, help="ComfyUI input/ 폴더에 있는 파일명")
    ap.add_argument("--gender", choices=["M", "F"], default=None)
    ap.add_argument("--out", default="result.png")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s")

    data = worker.generate(args.style, args.image, args.gender)
    Path(args.out).write_bytes(data)
    print(f"저장 완료: {args.out} ({len(data) / 1024:.0f}KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
