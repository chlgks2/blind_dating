#!/usr/bin/env python3
"""
models/manifest.json 을 읽어 ComfyUI 모델을 일괄 다운로드합니다.

가중치는 저장소에 포함하지 않고, 이 스크립트로 동일한 추론 환경을 재구성합니다.

사용법:
    pip install huggingface_hub requests
    python scripts/download_models.py --comfy-root /path/to/ComfyUI
    python scripts/download_models.py --comfy-root /path/to/ComfyUI --all   # 비교용 후보까지
    python scripts/download_models.py --comfy-root /path/to/ComfyUI --dry-run
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / "models" / "manifest.json"


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def download_hf(repo: str, file: str, dest: Path) -> None:
    from huggingface_hub import hf_hub_download

    cached = hf_hub_download(repo_id=repo, filename=file)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cached, dest)


def download_url(url: str, dest: Path) -> None:
    import requests

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
                done += len(chunk)
                if total:
                    pct = done * 100 // total
                    print(f"\r    {pct:3d}%  {human(done)} / {human(total)}", end="")
    print()
    tmp.rename(dest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comfy-root", required=True, help="ComfyUI 설치 경로")
    ap.add_argument("--all", action="store_true", help="비교용 후보 모델까지 전체 다운로드")
    ap.add_argument("--dry-run", action="store_true", help="다운로드하지 않고 계획만 출력")
    args = ap.parse_args()

    root = Path(args.comfy_root).expanduser().resolve()
    if not root.is_dir():
        print(f"[!] ComfyUI 경로를 찾을 수 없습니다: {root}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    models = manifest["models"]
    targets = models if args.all else [m for m in models if m.get("required")]

    print(f"ComfyUI  : {root}")
    print(f"대상 모델: {len(targets)} / {len(models)}\n")

    skipped, failed, ok, manual = [], [], 0, []

    for m in targets:
        dest = root / m["dest"]
        label = f'{m["name"]}  ({m.get("size", "?")})'

        if dest.exists() and dest.is_file():
            print(f"[skip] {label}  — 이미 존재")
            continue

        src = m["source"]
        stype = src.get("type")

        if stype == "manual":
            manual.append(m)
            print(f"[man ] {label}  — {src.get('note', '수동 설치 필요')}")
            continue

        if stype == "hf" and not (src.get("repo") and src.get("file")):
            skipped.append(m)
            print(f"[TODO] {label}  — 출처 미기입 ({src.get('note', '')})")
            continue

        if args.dry_run:
            where = src.get("repo") or src.get("url")
            print(f"[plan] {label}  ← {where}")
            continue

        print(f"[get ] {label}")
        try:
            if stype == "hf":
                download_hf(src["repo"], src["file"], dest)
            elif stype == "url":
                download_url(src["url"], dest)
            else:
                raise ValueError(f"알 수 없는 source.type: {stype}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            failed.append((m, e))
            print(f"       [!] 실패: {e}")

    print("\n" + "=" * 60)
    print(f"완료 {ok}건 / 실패 {len(failed)}건 / 출처 미기입 {len(skipped)}건 / 수동 {len(manual)}건")

    if skipped:
        print("\n[출처 미기입] models/manifest.json 의 source.repo / source.file 을 채워주세요:")
        for m in skipped:
            print(f"  - {m['name']}  →  {m['dest']}")

    if failed:
        print("\n[실패]")
        for m, e in failed:
            print(f"  - {m['name']}: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
