# 변환 전/후 샘플

| 파일 | 내용 |
|---|---|
| `before_after.jpg` | **변환 전/후 비교** — `anime2d` 스타일, 2인분 |
| `after_anime2d.png` | `anime2d` 단일 결과 (원본 해상도) |

## 사진 사용에 대해

샘플에 쓰인 사진은 **본인과 팀원 본인의 사진이며, 게재 동의를 받았습니다.**
**서비스 사용자(베타 테스터 포함)의 사진은 저장소에 포함돼 있지 않습니다.**

## 재현하기

```bash
cd ai
python scripts/run_local.py --style ghibli  --image sample.jpg --out docs/images/after_ghibli.png
python scripts/run_local.py --style anime2d --image sample.jpg --out docs/images/after_anime2d.png
```

입력 이미지는 `ComfyUI/input/` 에 두어야 합니다.

## 더 넣으면 좋을 비교 이미지

| 파일 | 내용 | 어필 포인트 |
|---|---|---|
| `facedetailer_compare.png` | FaceDetailer 적용 전/후 얼굴 크롭 | 문제를 인식하고 노드로 해결했음 |
| `upscale_compare.png` | 업스케일 denoise 0.15 vs 0.5 | 파라미터 근거를 실측으로 확인했음 |
| `stage1_vs_stage2.png` | 2-스테이지 1단계(정체성) / 2단계(화풍) | 모델 체이닝 설계 의도 |

> 파일당 1MB 이하로 리사이즈해서 올리십시오.
