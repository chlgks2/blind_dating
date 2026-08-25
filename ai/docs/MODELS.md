# 사용 모델 목록

이 프로젝트에서 사용한 모델은 **전부 공개된 사전학습 모델**이며, 별도의 파인튜닝이나 학습은 하지 않았습니다.
작업 내용은 **여러 체크포인트·LoRA·IPAdapter·업스케일러를 비교하고 조합해 하나의 추론 파이프라인으로 연결한 것**입니다.

가중치 총합이 **약 69GB** 이므로 저장소에는 포함하지 않았습니다.
[`../models/manifest.json`](../models/manifest.json) 과 [`../scripts/download_models.py`](../scripts/download_models.py) 로 동일 환경을 재구성할 수 있습니다.

- ★ = 운영 파이프라인에 실제 사용
- ☆ = 초기 실험에 사용 후 교체
- 그 외 = 스타일 재현도 비교를 위해 함께 확보한 후보 모델
- ⚠️ = 출처 URL 확인 후 `manifest.json` 에 기입 필요

---

## 1. Checkpoint (13종, 약 59GB)

| 사용 | 파일 | 용량 | 계열 | 역할 / 비교 결과 |
|:--:|---|--:|---|---|
| ★ | `dreamshaperXL_lightningDPMSDE.safetensors` | 6.9GB | SDXL | **운영 베이스.** 저스텝 계열로 생성 시간이 짧아, 사용자 대기 시간을 줄이기 위해 최종 채택 |
| ★ | `meinamix_v12Final.safetensors` | 2.1GB | SD1.5 | 2-스테이지 실험 파이프라인의 2단계 애니 화풍 변환용 |
| ☆ | `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` | 7.1GB | SDXL | **초기 실험 베이스.** 실사 기반 + IPAdapter FaceID 호환이 좋아 정체성 유지에 유리했으나 생성 시간이 길어 운영에서는 교체 (`workflows/ui/` 참고) |
| | `animagine-xl-4.0.safetensors` | 6.9GB | SDXL | 애니 특화 SDXL. 화풍은 강하나 원본 인물 보존이 약해 미채택 |
| | `sd_xl_base_1.0.safetensors` | 6.9GB | SDXL | 기준선(baseline) 비교용 |
| | `revAnimated_v122EOL.safetensors` | 5.5GB | SD1.5 | 애니/일러스트 후보 |
| | `revAnimated_v2Rebirth.safetensors` | 4.2GB | SD1.5 | 위 모델 후속 버전 비교 |
| | `flat2DAnimerge_v45Sharp.safetensors` | 2.1GB | SD1.5 | 플랫 2D 화풍 후보 |
| | `anythingv5nijimix_25BEST_sd15.safetensors` | 2.1GB | SD1.5 | 애니 화풍 후보 |
| | `anything-v4.0-pruned-fp32.safetensors` | 4.3GB | SD1.5 | 애니 화풍 후보 |
| | `chilloutmix_NiPrunedFp32Fix.safetensors` | 4.3GB | SD1.5 | 실사 계열 비교용 |
| | `v1-5-pruned-emaonly.safetensors` | 4.3GB | SD1.5 | 기준선 비교용 |
| | `2dTo3DEmoji_30img.ckpt` | 2.1GB | SD1.5 | 제페토/3D 이모지 스타일 실험 |

## 2. LoRA (9종, 약 3.5GB)

| 사용 | 파일 | 용량 | weight | 역할 |
|:--:|---|--:|:--:|---|
| ★ | `giblylast.safetensors` | 456MB | **0.8 / 0.8** (ghibli)<br>**0.7 / 0.7** (anime2d) | 지브리 스타일. 후보 4종 A/B 비교 후 채택. 스타일별로 weight를 따로 튜닝 |
| ★ | `thickline_fp16.safetensors` | 151MB | **0.6 / 0.6** | 굵은 선 셀 애니. 2-스테이지 실험 2단계에서 사용 |
| | `tangbohu-pixarstyle-xl.safetensors` | 457MB | — | 픽사 스타일 후보. 전용 워크플로우 미구현으로 운영 미반영 |
| ★ | `ip-adapter-faceid-plusv2_sdxl_lora.safetensors` | 372MB | 0.6 | IPAdapter FaceID 전용 LoRA (UnifiedLoader가 자동 로드) |
| | `Ghibli_xl_v2.safetensors` | 810MB | — | 지브리 후보. 스타일 강도는 높으나 얼굴 왜곡 발생 |
| | `ghibli_style_offset.safetensors` | 151MB | — | 지브리 후보(offset 방식). 변환 강도 부족 |
| | `Fresh Ideas@Studio Ghibli style_SDXL.safetensors` | 456MB | — | 지브리 후보 |
| | `cute-anime v1.safetensors` | 456MB | — | 애니 화풍 후보 |
| | `zerotwo.safetensors` | 228MB | — | 캐릭터 LoRA 동작 검증용 |

## 3. 얼굴 정체성 유지 — IPAdapter / CLIP Vision / InsightFace

| 사용 | 파일 | 용량 | 출처 | 역할 |
|:--:|---|--:|---|---|
| ★ | `ip-adapter-faceid-plusv2_sdxl.bin` | 1.5GB | `h94/IP-Adapter-FaceID` | **FaceID Plus V2.** 얼굴 임베딩을 조건으로 주입. `provider=CUDA` (초기 CPU 설정에서 임베딩 추출이 병목) |
| ★ | `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | 2.5GB | `laion/CLIP-ViT-H-14-laion2B-s32B-b79K` | IPAdapter용 이미지 인코더 |
| ★ | `insightface/buffalo_l` | 340MB | InsightFace 릴리스 | `det_10g`(검출), `w600k_r50`(ID 임베딩), `2d106det`·`1k3d68`(랜드마크), `genderage` |
| | `ip-adapter-plus_sdxl_vit-h.safetensors` | 848MB | `h94/IP-Adapter` | 일반 이미지 프롬프트 비교용 |
| | `ip-adapter_sdxl.safetensors` | 703MB | `h94/IP-Adapter` | 기본 IPAdapter 비교용 |

IPAdapter FaceID 운영 설정: `preset=FACEID PLUS V2`, `provider=CUDA`, `weight_type=linear`, `combine_embeds=concat`, `embeds_scaling=V only`

| 스타일 | `weight` | `lora_strength` | LoRA weight | 의도 |
|---|--:|--:|--:|---|
| `ghibli` | 0.65 | 0.85 | 0.8 | 화풍을 강하게, 정체성은 약하게 |
| `anime2d` | 0.75 | 0.6 | 0.7 | 정체성을 강하게, 화풍은 약하게 |

## 4. 얼굴 검출 · 세그멘테이션 (FaceDetailer)

| 사용 | 파일 | 용량 | 경로 | 역할 |
|:--:|---|--:|---|---|
| ★ | `face_yolov8m.pt` | 52MB | `models/ultralytics/bbox/` | 얼굴 bbox 검출 |
| ★ | `sam_vit_b_01ec64.pth` | 375MB | `models/sams/` | 검출 영역 마스크 생성 (자연스러운 합성) |
| | `hand_yolov8s.pt` | 23MB | `models/ultralytics/bbox/` | 손 디테일링 실험 |
| | `person_yolov8m-seg.pt` | 55MB | `models/ultralytics/segm/` | 인물 세그멘테이션 실험 |

## 5. 업스케일

| 사용 | 파일 | 용량 | 출처 | 설정 |
|:--:|---|--:|---|---|
| ★ | `4x-UltraSharp.pth` | 67MB | `lokCX/4x-Ultrasharp` | Ultimate SD Upscale에서 `upscale_by=1.2`, `denoise=0.15~0.2`, tile 512~768, `seam_fix=Linear` |

> 4배 업스케일러를 그대로 쓰지 않고 배율과 denoise를 억제한 이유: 업스케일 단계의 디노이즈가 사실상 재생성이라 얼굴 인상이 바뀌었습니다. 역할을 "디테일 보정"으로 제한했습니다.

---

## 6. ComfyUI Custom Nodes

| 노드 팩 | 저장소 | 사용 목적 |
|---|---|---|
| ComfyUI-Manager | `ltdrdata/ComfyUI-Manager` | 노드/모델 관리 |
| ComfyUI_IPAdapter_plus | `cubiq/ComfyUI_IPAdapter_plus` | IPAdapter FaceID |
| ComfyUI_UltimateSDUpscale | `ssitu/ComfyUI_UltimateSDUpscale` | 타일 기반 업스케일 |
| ComfyUI-Impact-Pack | `ltdrdata/ComfyUI-Impact-Pack` | FaceDetailer |
| ComfyUI-Impact-Subpack | `ltdrdata/ComfyUI-Impact-Subpack` | UltralyticsDetectorProvider |
| ComfyUI-Advanced-ControlNet | `Kosinkadink/ComfyUI-Advanced-ControlNet` | 구조 제어 실험 |
| comfyui-art-venture | `sipherxyz/comfyui-art-venture` | 유틸리티 노드 |
| efficiency-nodes-comfyui | `jags111/efficiency-nodes-comfyui` | 그래프 단순화 |
| ComfyUI-YoloWorld-EfficientSAM | `ZHO-ZHO-ZHO/ComfyUI-YoloWorld-EfficientSAM` | 세그멘테이션 실험 |

---

## 7. 라이선스 주의

체크포인트와 LoRA는 각각 별도의 라이선스(CreativeML Open RAIL-M, Fair AI Public License 등)를 따릅니다.
**본 저장소는 가중치를 재배포하지 않으며**, 각 모델의 원 배포처 라이선스 조건을 확인한 뒤 사용해야 합니다.
