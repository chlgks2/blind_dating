# 💘 지금까지 이런 소개팅은 없었다

## 당신이 찾던 당신과 찰떡인 사람, 우리가 찾아줄게.

질문에 답하는 것만으로 나와 잘 맞는 상대를 찾아주는 블라인드 소개팅 서비스입니다.

단순히 취미 몇 개가 같은 사람을 연결하는 것이 아니라,

- 같은 가치관을 가진 사람
- 서로의 성향을 보완해 줄 수 있는 사람
- 나와 잘 맞는 사람

을 설문 결과와 매칭 알고리즘을 통해 추천합니다.

---

# 📌 프로젝트 소개

사용자가 다양한 질문에 답하면,

각 답변의 중요도와 성향을 분석하여 가장 높은 유사도를 가진 상대를 추천하는 블라인드 소개팅 플랫폼입니다.

얼굴이나 외적인 요소보다 성향과 가치관을 우선으로 연결하는 것을 목표로 합니다.

---

# ✨ 주요 기능

### 회원 시스템

- 회원가입
- 로그인
- JWT 인증
- 내 정보 조회

### 취향 설문 시스템

- A vs B 양자택일 질문
- 스와이프 기반 설문 UX
- 답변 저장
- 설문 재참여 지원

### 매칭 시스템

- Similar (같을수록 좋은 질문)
- Complement (다를수록 좋은 질문)
- Neutral (재미용 질문)
- 질문별 가중치 적용
- 유사도 기반 추천

### 친구 요청 시스템

- 친구 요청 전송
- 친구 요청 수락 / 거절
- 상호 연결 생성

### 실시간 채팅

- Django Channels 기반 WebSocket 채팅
- Redis Channel Layer 사용
- 채팅 내역 저장
- 실시간 메시지 전송

### 결제 시스템

- PortOne 연동
- 소개팅 채팅 오픈 결제
- 양측 결제 완료 시 채팅방 활성화

---

# 🛠 Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Channels
- Simple JWT
- Redis
- SQLite3

### Frontend

- Vue 3
- Pinia
- Vue Router
- Axios
- Vite

### Realtime

- WebSocket
- Redis Channel Layer

### Payment

- PortOne

---

# 📂 프로젝트 구조

```text
blind_dating
│
├── backend
│   ├── accounts
│   ├── matching
│   ├── config
│   ├── manage.py
│   └── requirements.txt
│
└── frontend
    ├── src
    ├── public
    ├── package.json
    └── vite.config.js
```

---

# ⚙️ 실행 방법

## Backend

```bash
cd backend

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 API

### 회원가입

```
POST /api/accounts/signup/
```

### 로그인

```
POST /api/accounts/login/
```

### 토큰 재발급

```
POST /api/accounts/login/refresh/
```

### 내 정보 조회

```
GET /api/accounts/me/
```

### 질문 목록 조회

```
GET /api/matching/questions/
```

### 답변 제출

```
POST /api/matching/answers/
```

### 매칭 결과 조회

```
GET /api/matching/matches/
```

---

# 🧠 매칭 알고리즘

- 질문별 가중치(weight) 적용
- 단일 선택 질문 지원
- 복수 선택 질문 지원
- 자카드 유사도(Jaccard Similarity) 적용
- 비슷할수록 좋은 질문(Similar)
- 다를수록 좋은 질문(Complement)
- 사용자 매칭 성향 반영

---

# 🚀 개발 목표

외모나 스펙보다

**"정말 잘 맞는 사람을 찾아주는 소개팅 서비스"**

를 만드는 것이 목표입니다.

사용자가 질문에 답하는 과정 자체도 재미있고,

만났을 때 "생각보다 정말 잘 맞는다"라는 경험을 제공하는 서비스를 지향합니다.

---

# 🚀 개발 목표

외모나 스펙보다

**"정말 잘 맞는 사람을 찾아주는 소개팅 서비스"**

를 만드는 것이 목표입니다.

사용자가 질문에 답하는 과정 자체도 재미있고,

만났을 때 "생각보다 정말 잘 맞는다"라는 경험을 제공하는 서비스를 지향합니다.

---

# 🎉 Special Thanks

## 강다영 최고 ✨
