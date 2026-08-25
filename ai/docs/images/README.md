# 변환 전/후 샘플

`after_anime2d.png` — `anime2d` 스타일 변환 결과.

입력 원본 사진은 개인 사진이라 저장소에 포함하지 않았습니다.

## 전/후 비교 이미지를 추가하려면

포트폴리오에서는 **전/후를 나란히 놓는 것이 가장 효과가 큽니다.**
개인 사진을 쓰지 않고 만들려면, 상업적 이용이 가능한 무료 인물 사진으로 파이프라인을 한 번 더 돌리면 됩니다.

1. Unsplash / Pexels 에서 정면 인물 사진 1장을 받는다 (라이선스 확인)
2. `ComfyUI/input/` 폴더에 `sample.jpg` 로 저장
3. 파이프라인 실행

```bash
cd ai
python scripts/run_local.py --style ghibli  --image sample.jpg --out docs/images/after_ghibli.png
python scripts/run_local.py --style anime2d --image sample.jpg --out docs/images/after_anime2d.png
cp /path/to/sample.jpg docs/images/before.jpg
```

4. `ai/README.md` 의 "결과 예시" 섹션과 루트 `README.md` 를 전/후 표로 교체

### 그 밖에 넣으면 좋은 비교 이미지

| 파일 | 내용 | 어필 포인트 |
|---|---|---|
| `facedetailer_compare.png` | FaceDetailer 적용 전/후 얼굴 크롭 | 문제를 인식하고 노드로 해결했음 |
| `upscale_compare.png` | 업스케일 denoise 0.15 vs 0.5 | 파라미터 근거를 실측으로 확인했음 |
| `stage1_vs_stage2.png` | 2-스테이지 1단계(정체성) / 2단계(화풍) | 모델 체이닝 설계 의도 |

> `.gitignore` 에서 `docs/images/` 하위 이미지는 예외 처리되어 커밋됩니다.
> 파일당 1MB 이하로 리사이즈해서 올리세요.
