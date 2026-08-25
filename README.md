# 💘 지금까지 이런 소개팅은 없었다

## 당신이 찾던 당신과 찰떡인 사람, 우리가 찾아줄게.

질문에 답하는 것만으로 나와 잘 맞는 상대를 찾아주는 **블라인드 소개팅 서비스**입니다.

단순히 취미 몇 개가 같은 사람을 연결하는 것이 아니라,

- 같은 가치관을 가진 사람
- 서로의 성향을 보완해 줄 수 있는 사람
- 나와 잘 맞는 사람

을 설문 결과와 매칭 알고리즘을 통해 추천합니다.

그리고 **얼굴 사진을 그대로 노출하지 않기 위해**, 업로드한 사진을 AI 스타일 아바타로 변환해 프로필로 사용합니다.

---

# 📌 프로젝트 소개

| | |
|---|---|
| **기간** | 2026.06 (약 N주) |
| **팀** | 2인 |
| **역할** | Backend · AI/GPU 파이프라인 / Frontend UI |
| **구성** | Vue 3 SPA · Django(REST + WebSocket) · Linux GPU 추론 서버 |

사용자가 다양한 질문에 답하면, 각 답변의 **중요도(weight)** 와 **성향(같을수록 좋음 / 다를수록 좋음)** 을 분석해 가장 높은 궁합 점수를 가진 상대를 추천합니다.
얼굴이나 외적인 요소보다 성향과 가치관을 우선으로 연결하는 것을 목표로 합니다.

---

# 🏗 시스템 아키텍처

```
┌─────────────────┐
│    Vue 3 SPA    │  Vite · Pinia · Vue Router · Axios
└────────┬────────┘
         │  REST (JWT)            WebSocket (JWT in query)
         ▼
┌──────────────────────────────────────┐        ┌──────────────┐
│   Django + DRF + Channels (Daphne)   │◀──────▶│    Redis     │
│                                      │        │ Channel Layer│
│  accounts · matching · AIJob queue    │        └──────────────┘
└───────┬───────────────────▲──────────┘
        │                   │
        │ 원본/결과 저장     │  ① GET  /ai/next-job/         작업 선점
        ▼                   │  ② POST /ai/complete-upload/  결과 업로드
┌──────────────┐            │
│   AWS S3     │            └──── outbound polling ────┐
│ originals/   │                                       │
│ generated/   │                          ┌────────────────────────────┐
└──────────────┘                          │   GPU Server               │
                                          │   폴링 워커 (+ FastAPI)     │
┌──────────────┐                          │        │                   │
│   PortOne    │◀── 결제 검증 ────────────│   ComfyUI (SDXL / SD1.5)   │
└──────────────┘                          │   LoRA · IPAdapter FaceID  │
                                          │   FaceDetailer · SD Upscale│
                                          └────────────────────────────┘
```

**핵심 설계: GPU 서버는 Django를 폴링한다 (pull / worker 방식)**

이미지 1장 생성에 수십 초 이상이 걸려 동기 HTTP 호출로는 타임아웃이 발생합니다.
Django가 GPU 서버를 호출하는 push 방식 대신, **GPU 서버가 Django의 작업 큐를 폴링해 가져가는 pull 방식**을 선택했습니다.

- GPU 서버에 **인바운드 포트를 열 필요가 없음** → 사설망·유동 IP 환경에서도 동작
- GPU 서버가 죽어도 작업은 DB에 `pending` 으로 남아 **유실되지 않음**
- 워커 프로세스를 추가하면 그대로 **수평 확장**

자세한 내용 👉 **[`ai/README.md`](ai/README.md)**

---

# ✨ 주요 기능

### 회원 시스템
- 회원가입 / 로그인 / JWT 인증 / 토큰 갱신 / 내 정보 조회
- `AbstractUser` 확장 커스텀 유저 (닉네임, 성별, 출생연도, 설문 완료 여부, 매칭 성향)

### AI 프로필 아바타 생성 🆕
- 사진 업로드 + 스타일 선택 (지브리 / 2D 애니 / 픽사 / 제페토)
- **DB 기반 비동기 작업 큐** (`pending → processing → done / failed`)
- GPU 서버가 작업을 가져가 ComfyUI 파이프라인으로 변환 후 결과 반환
- 프론트는 3초 간격 상태 폴링, 완료 시 S3 URL 표시

### 취향 설문 시스템
- A vs B 양자택일 질문 / 스와이프 기반 UX / 답변 저장 / 재참여 지원

### 매칭 시스템
- `Similar`(같을수록 좋은 질문) · `Complement`(다를수록 좋은 질문) · `Neutral`(재미용)
- 질문별 가중치 적용, 사용자 매칭 성향 반영, 0~100 정규화 점수

### 친구 요청 시스템
- 요청 전송 / 수락·거절 / 상호 연결(Match) 생성

### 실시간 채팅
- Django Channels + Redis Channel Layer 기반 WebSocket
- **WebSocket용 JWT 인증 미들웨어 직접 구현** (쿼리스트링 토큰 검증)
- 연결 시 채팅방 참가자 여부 검증 후 수락 / 채팅 내역 저장

### 결제 시스템
- PortOne 연동, 서버 사이드 결제 재검증
- **양측 모두 결제 완료 시에만** 채팅방 활성화

---

# 🛠 Tech Stack

### Backend
`Python` · `Django 6.0` · `Django REST Framework` · `Simple JWT` · `Django Channels` · `Daphne (ASGI)` · `Redis` · `boto3 (AWS S3)` · `SQLite3`

### AI / GPU Server
`Python` · `FastAPI` · `ComfyUI` · `PyTorch / CUDA` · `Stable Diffusion XL` · `SD 1.5` · `LoRA` · `IP-Adapter FaceID` · `InsightFace` · `Ultralytics YOLOv8` · `SAM` · `Ultimate SD Upscale`

### Frontend
`Vue 3` · `Vite` · `Pinia` · `Vue Router` · `Axios`

### Infra / External
`AWS S3` · `Redis` · `PortOne`

---

# 📂 프로젝트 구조

```text
blind_dating
│
├── backend                  Django (REST + WebSocket)
│   ├── accounts             인증 · 프로필 · AI 작업 큐
│   ├── matching             질문/답변 · 매칭 · 채팅 · 결제
│   ├── config               settings / asgi / urls
│   ├── manage.py
│   └── requirements.txt
│
├── ai                       GPU 추론 서버 (폴링 워커 + ComfyUI)
│   ├── README.md            아키텍처 · 파이프라인 · 설계 근거
│   ├── app                  worker.py(폴링 루프) · config.py · main.py(FastAPI /health)
│   ├── workflows            ComfyUI 워크플로우 JSON (운영 / 실험 / UI 편집용)
│   ├── models/manifest.json 모델 목록 (가중치는 미포함)
│   ├── scripts              모델 다운로드 · 파이프라인 단독 검증
│   └── docs                 MODELS.md · 변환 전후 샘플 이미지
│
└── frontend                 Vue 3 SPA
    ├── src
    ├── public
    ├── package.json
    └── vite.config.js
```

> ⚠️ AI 모델 가중치(합계 약 69GB)는 저장소에 포함되지 않습니다.
> 전부 공개 사전학습 모델이며 `ai/scripts/download_models.py` 로 동일 환경을 재구성할 수 있습니다.

---

# ⚙️ 실행 방법

## 1. Backend

```bash
cd backend
pip install -r requirements.txt

cp .env.example .env      # SECRET_KEY, AWS_*, PORTONE_* 설정

python manage.py migrate
python manage.py seed_questions    # 질문 시딩
daphne -b 0.0.0.0 -p 8000 config.asgi:application    # WebSocket 포함 실행
```

> Redis가 실행되어 있어야 채팅이 동작합니다. `docker run -p 6379:6379 redis`

## 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

## 3. AI GPU Server

```bash
cd ai
pip install -r requirements.txt
python scripts/download_models.py --comfy-root /opt/ComfyUI

cp .env.example .env      # BACKEND_URL, COMFYUI_URL 설정

python -m app.worker                                   # 워커만 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000        # FastAPI 래퍼(/health)와 함께
```

자세한 설치·설정은 [`ai/README.md`](ai/README.md) 참고.

---

# 🔑 API

### 인증 / 프로필

| 메서드 | 엔드포인트 | 설명 |
|---|---|---|
| `POST` | `/api/accounts/signup/` | 회원가입 |
| `POST` | `/api/accounts/login/` | 로그인 (JWT 발급) |
| `POST` | `/api/accounts/login/refresh/` | 토큰 재발급 |
| `GET` | `/api/accounts/me/` | 내 정보 조회 |

### AI 아바타 생성

| 메서드 | 엔드포인트 | 설명 |
|---|---|---|
| `POST` | `/api/accounts/ai/create/` | 사진 업로드 + 스타일 선택 → 작업 등록 (즉시 `job_id` 반환) |
| `GET` | `/api/accounts/ai/status/<job_id>/` | 작업 상태 조회 (폴링) |
| `GET` | `/api/accounts/ai/next-job/` | **[워커]** 대기 작업 1건 선점 |
| `POST` | `/api/accounts/ai/complete-upload/` | **[워커]** 결과 이미지 전송 → S3 업로드 → 완료 처리 |
| `POST` | `/api/accounts/ai/complete/` | **[워커]** 완료/실패 통보 |

### 매칭 / 설문

| 메서드 | 엔드포인트 | 설명 |
|---|---|---|
| `GET` | `/api/matching/questions/` | 질문 목록 |
| `POST` | `/api/matching/answers/` | 답변 제출 |
| `GET` | `/api/matching/matches/recommend/` | 추천 상대 목록 |

### 친구 요청 / 채팅 / 결제

| 메서드 | 엔드포인트 | 설명 |
|---|---|---|
| `POST` | `/api/matching/friend-request/send/` | 친구 요청 전송 |
| `POST` | `/api/matching/friend-request/respond/` | 수락 / 거절 |
| `GET` | `/api/matching/friend-request/received/` | 받은 요청 목록 |
| `GET` | `/api/matching/my-matches/` | 내 채팅방 목록 |
| `GET` | `/api/matching/matches/<match_id>/messages/` | 채팅 내역 |
| `POST` | `/api/matching/payment/verify/` | 결제 서버 검증 |
| `WS` | `/ws/chat/<match_id>/?token=<JWT>` | 실시간 채팅 |

---

# 🧠 매칭 알고리즘

단순 일치율이 아니라, **질문의 성격에 따라 점수 부호를 뒤집어** 궁합을 계산합니다.

```python
for qid in (A가 답한 질문 ∩ B가 답한 질문):
    same     = (A의 선택 == B의 선택)
    base_sim = 1.0 if same else 0.0

    # 다를수록 좋은 질문은 유사도를 반전
    sim = (1.0 - base_sim) if q.match_type == 'complement' else base_sim

    weight = q.weight
    # 양쪽 모두 '다른 사람'을 선호하면 complement 질문 가중치 증폭
    if both_prefer_complement and q.match_type == 'complement':
        weight *= 1.5

    score  += sim * weight
    total  += weight

return round(score / total * 100, 1)     # 0 ~ 100
```

- **질문별 가중치**로 가치관 질문과 재미용 질문의 영향력을 분리
- **사용자의 매칭 성향(`match_preference`)** 을 알고리즘에 반영
- **공통 응답 질문만** 분모로 삼아 설문 진행도 차이로 인한 점수 왜곡 제거
- 다수 비교 시 `Question` 을 dict로 캐싱해 반복 쿼리 제거

---

# 🎨 AI 아바타 파이프라인 (요약)

<img src="ai/docs/images/after_anime2d.png" width="280">

`anime2d` 스타일 변환 결과 예시

```
원본 사진
  │
  ├─ IPAdapter FaceID (Plus V2) ─ InsightFace buffalo_l 임베딩   ← 얼굴 정체성
  │
  ▼
SDXL (DreamShaper XL Lightning) + Ghibli LoRA (0.8)
  → KSampler  img2img, denoise 0.6, dpmpp_2m_sde/karras          ← 화풍 변환
  → FaceDetailer  YOLOv8-face + SAM, denoise 0.3                 ← 얼굴 디테일 복원
  → Ultimate SD Upscale  4x-UltraSharp ×1.2, denoise 0.15        ← 해상도 보정
  ▼
결과 이미지 → S3
```

| 판단 | 이유 |
|---|---|
| txt2img 대신 **img2img (denoise 0.6)** | 원본의 구도·포즈를 유지하면서 화풍만 바꾸기 위해 |
| 베이스를 **저스텝 SDXL(DreamShaper XL Lightning)** 로 교체 | 초기 Juggernaut-XL v9 대비 생성 시간을 줄여 사용자 대기 시간 단축 |
| **FaceDetailer** 추가 | 전신 사진에서 얼굴에 할당되는 해상도가 부족해 뭉개지는 문제 해결 |
| 4x 업스케일러를 **×1.2 / denoise 0.15** 로 억제 | 업스케일 단계의 디노이즈가 얼굴 인상을 바꿔버리는 문제 해결 |
| IPAdapter weight와 LoRA weight를 **스타일별로 따로 튜닝** | 정체성과 화풍이 같은 샘플링에서 상쇄되므로 두 축을 분리해 조정 |

**SDXL(정체성) → 픽셀 공간 경유 → SD1.5 + thickline LoRA(화풍)** 의 2단계 모델 체이닝도 구현·검증했으나, 생성 시간이 약 2배로 늘어 운영에는 반영하지 않았습니다. (`ai/workflows/experimental/`)

전체 설계 근거·파라미터·모델 비교 결과 👉 **[`ai/README.md`](ai/README.md)** · **[`ai/docs/MODELS.md`](ai/docs/MODELS.md)**

---

# 🚧 알려진 한계와 개선 계획

| 한계 | 개선 방향 |
|---|---|
| 워커 엔드포인트가 인증 없이 공개 | 워커 전용 시크릿 헤더 + IP 화이트리스트 |
| 작업 선점이 비원자적 → 다중 워커 시 중복 처리 가능 | `select_for_update(skip_locked=True)` 또는 Celery + Redis 브로커 |
| 유저·워커 양쪽 폴링으로 불필요한 요청 발생 | 기존 Channels 재사용해 WebSocket 푸시 / SSE |
| 워커가 처리 중 죽으면 `processing` 잔류 | `updated_at` 기반 타임아웃 재큐잉 + 재시도 카운트 |
| `NextJobAPIView` 응답에 `gender` 가 없어 성별 프롬프트 보강이 비활성 | 응답에 `user.gender` 추가 |
| `pixar` · `zepeto` 는 선택지만 있고 전용 워크플로우 미구현 | 워크플로우 추가 (현재는 기본 스타일로 대체) |
| SQLite로 동시 쓰기 취약 | PostgreSQL 전환 |
| 채팅 토큰이 쿼리스트링에 노출 | 단기 1회용 티켓 토큰 교환 방식 |

---

# 🚀 개발 목표

외모나 스펙보다

**"정말 잘 맞는 사람을 찾아주는 소개팅 서비스"**

를 만드는 것이 목표입니다.

사용자가 질문에 답하는 과정 자체도 재미있고, 만났을 때 "생각보다 정말 잘 맞는다"라는 경험을 제공하는 서비스를 지향합니다.

---

# 🎉 Special Thanks

## 강다영 최고 ✨
