<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <div class="login-body">
        
        <div class="title-block">
          <h1 class="signin-title">Your Profile</h1>
          <p class="signin-sub">당신의 취향을 담은 프로필이 생성되었습니다</p>
        </div>

        <!-- 생성 완료: 이미지 표시 -->
        <div v-if="avatarUrl" class="avatar-card-container">
          <div class="avatar-card">
            <img :src="avatarUrl" alt="Final AI Avatar" class="avatar-img" />
          </div>
        </div>

        <!-- 생성 중: 대기 UI -->
        <div v-else-if="isGenerating" class="generating-wrap">
          <div class="generating-dots">
            <span></span><span></span><span></span>
          </div>
          <p class="generating-text">이미지 생성 중이에요</p>
          <p class="generating-sub">잠시만 기다려주세요</p>
        </div>

        <!-- 이미지도 없고 생성 중도 아님 (실패/미등록) -->
        <div v-else class="generating-wrap">
          <p class="generating-text">이미지를 불러올 수 없어요</p>
          <p class="generating-sub">프로필 사진을 다시 업로드해주세요</p>
        </div>

        <div class="action-block">
          <button class="btn-continue" :disabled="!avatarUrl" @click="goToMatching">
            매칭하러 가기
          </button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const avatarUrl = ref(null)   // null = 아직 모름
const isGenerating = ref(false)
let pollTimer = null

const stopPoll = () => {
  if (pollTimer) { clearTimeout(pollTimer); pollTimer = null }
}

const pollStatus = async () => {
  const jobId = localStorage.getItem('ai_job_id')
  if (!jobId) { isGenerating.value = false; return }
  try {
    const res = await api.get(`/accounts/ai/status/${jobId}/`)
    if (res.data.status === 'done' && res.data.generated_url) {
      localStorage.setItem('ai_generated_url', res.data.generated_url)
      avatarUrl.value = res.data.generated_url
      isGenerating.value = false
      stopPoll()
    } else if (res.data.status === 'failed') {
      isGenerating.value = false
      stopPoll()
    } else {
      // pending / processing → 3초 후 재시도
      pollTimer = setTimeout(pollStatus, 3000)
    }
  } catch (e) {
    pollTimer = setTimeout(pollStatus, 3000)
  }
}

onMounted(async () => {
  // 이미 저장된 URL이 있으면 바로 표시
  const cached = localStorage.getItem('ai_generated_url')
  if (cached) {
    avatarUrl.value = cached
    return
  }
  // 없으면 생성 중 상태로 폴링 시작
  isGenerating.value = true
  await pollStatus()
})

onUnmounted(stopPoll)

const goToMatching = () => router.push('/matching')
</script>

<style scoped>

.login-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 52px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 52px);
  animation: fadeInEffect 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInEffect {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.title-block {
  margin-top: 30px;
  margin-bottom: 24px;
  text-align: center;
}

.signin-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 400;
  color: var(--white);
  letter-spacing: 0.02em;
  line-height: 1.1;
  text-transform: uppercase;
}

.signin-sub {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-sub);
  line-height: 1.6;
  font-weight: 300;
}

.generating-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding-bottom: 60px;
}

.generating-dots {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.generating-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  animation: dot-blink 1.4s ease-in-out infinite;
}

.generating-dots span:nth-child(2) { animation-delay: 0.2s; }
.generating-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dot-blink {
  0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
  40%            { opacity: 1;   transform: scale(1.2); }
}

.generating-text {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 300;
  color: #fff;
  margin: 0;
  letter-spacing: 0.02em;
}

.generating-sub {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.45);
  margin: 0;
}

.avatar-card-container {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 0;
  margin-top: 40px;
  margin-bottom: 15px;
}

.avatar-card {
  position: relative;
  width: 240px;
  aspect-ratio: 3 / 4;
  border-radius: 28px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.4);
  box-shadow:
    0 0 20px rgba(255, 255, 255, 0.4),
    0 0 40px rgba(240, 130, 170, 0.25);
  animation: cardFloating 4s ease-in-out infinite;
}

@keyframes cardFloating {
  0%   { transform: translateY(0); }
  50%  { transform: translateY(-8px); }
  100% { transform: translateY(0); }
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.action-block {
  padding: 16px 0 40px 0;
  overflow: visible;
}


.btn-continue { 
    width: 240px; 
    margin: 0 auto;
    display: block;
    padding: 14px; 
    
    background: linear-gradient(135px, #ffffff 0%, rgba(255, 255, 255, 0.9) 50%, #ffffff 100%);
    background-size: 200% 200%;
    color: var(--app-canvas-bg);
    
    font-size: 15px; 
    font-weight: 600; 
    letter-spacing: 0.08em; 
    text-transform: uppercase; 
    border: none; 
    border-radius: var(--r-pill); /* 💡 999px 대신 토큰 사용 */
    cursor: pointer; 
    box-sizing: border-box; 
    font-family: var(--font-display); 
    font-weight: 500;
    position: relative;
    z-index: 1;
    
    animation: glow-aurora 4s ease infinite;
    box-shadow: 
      0 0 20px rgba(255, 255, 255, 0.4),  /* 내부 광채 */
      0 0 40px rgba(255, 255, 255, 0.2),  /* 중간 광채 */
      0 0 80px rgba(255, 255, 255, 0.1);  /* 외부 확산 광채 */
    
    transition: all 0.3s ease;
}

/* 🔥 [핵심] 버튼이 활성화(:not(:disabled))되었을 때만 일렁임과 오라 발동! */
.btn-continue:not(:disabled) {
    animation: glow-aurora 4s ease infinite;
    box-shadow: 
      0 0 30px rgba(255, 255, 255, 0.5), 
      0 0 60px rgba(255, 255, 255, 0.3),
      0 0 100px rgba(255, 255, 255, 0.1);
}

/* 호버했을 때 살짝 떠오르는 텐션 */
.btn-continue:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 
      0 0 40px rgba(255, 255, 255, 0.6), 
      0 0 80px rgba(255, 255, 255, 0.4);
}

/* ❌ 비활성화 상태일 때는 일렁임도 끄고 투명하게 */
.btn-continue:disabled { 
    background: rgba(255, 255, 255, 0.3); 
    color: rgba(255, 255, 255, 0.6); 
    cursor: not-allowed; 
    box-shadow: none;
    animation: none;
}


/* 💡 활성화된 버튼의 뒤쪽에 가짜 복사본을 만들어 흐릿하게(blur) 만들고 숨쉬듯 키워줍니다 */
.btn-continue:not(:disabled)::before {
    content: '';
    position: absolute;
    inset: -2px; /* 버튼보다 살짝 크게 */
    border-radius: var(--r-pill);
    background: linear-gradient(90deg, rgba(255,255,255,0.8), rgba(255, 186, 212, 0.609), rgba(255, 255, 255, 0.8));
    background-size: 200%;
    z-index: -1; /* 버튼 글씨 뒤로 숨기 */
    filter: blur(10px);
    opacity: 0.7;
    animation: glow-aurora 3s linear infinite, pulse-glow 2s ease-in-out infinite alternate;
}

@keyframes pulse-glow {
    from { transform: scale(0.98); opacity: 0.5; }
    to { transform: scale(1.03); opacity: 0.9; }
}

</style>