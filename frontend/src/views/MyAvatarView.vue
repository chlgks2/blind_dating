<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <div class="login-body">
        
        <div class="title-block">
          <h1 class="signin-title">Your Profile</h1>
          <p class="signin-sub">당신의 취향을 담은 프로필이 생성되었습니다</p>
        </div>

        <div class="avatar-card-container">
          <div class="avatar-card">
            <img src="@/assets/result.png" alt="Final AI Avatar" class="avatar-img" />
          </div>
        </div>

        <div class="action-block">
          <button class="btn-continue" @click="goToMatching">
            매칭하러 가기
          </button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToMatching = () => {
  router.push('/matching')
}
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