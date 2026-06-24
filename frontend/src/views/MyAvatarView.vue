<template>
  <div class="app-shell">
    <div class="mobile-frame">
      
      <div class="bg-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        
        <div class="particle-container">
          <div class="particle p-1"></div>
          <div class="particle p-2"></div>
          <div class="particle p-3"></div>
          <div class="particle p-4"></div>
        </div>
      </div>

      <div class="login-body">
        
        <div class="title-block">
          <h1 class="signin-title">Your Avatar</h1>
          <p class="signin-sub">당신의 성향을 담은 AI 아바타가 완성되었습니다 ✨</p>
        </div>

        <div class="avatar-card-container">
          <div class="avatar-card">
            <img src="@/assets/result.png" alt="Final AI Avatar" class="avatar-img" />
            
            <div class="avatar-overlay">
              <span class="badge">MY PERSONA</span>
              <h2 class="avatar-name">Cyberpunk Dreamer</h2>
            </div>
          </div>
        </div>

        <div class="action-block">
          <button class="btn-continue" @click="goToMatching">
            매칭하러 가기 💘
          </button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 🚀 매칭 화면으로 넘어가는 함수 (나중에 쫀득한 페이드 인터랙션 추가 가능!)
const goToMatching = () => {
  router.push('/matching') // 본 게임인 매칭 뷰 경로로 이동
}
</script>

<style scoped>
/* ── 톤앤매너 일치를 위한 공통 배경 & 파티클 스타일 ── */
.bg-orbs { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(70px); }
.orb-1 { width: 280px; height: 280px; background: radial-gradient(circle, rgba(255,180,210,0.65) 0%, transparent 70%); top: -80px; left: -60px; animation: drift 12s ease-in-out infinite alternate; }
.orb-2 { width: 220px; height: 220px; background: radial-gradient(circle, rgba(240,130,170,0.50) 0%, transparent 70%); top: 60px; right: -50px; animation: drift 15s ease-in-out infinite alternate-reverse; }
.orb-3 { width: 180px; height: 180px; background: radial-gradient(circle, rgba(255,210,230,0.55) 0%, transparent 70%); top: 260px; left: 60px; animation: drift 10s ease-in-out infinite alternate; }
@keyframes drift { 0% { transform: translate(0, 0) scale(1) rotate(0deg); } 50% { transform: translate(40px, -60px) scale(1.2) rotate(180deg); } 100% { transform: translate(-30px, 30px) scale(0.9) rotate(360deg); } }

.particle-container { position: absolute; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.particle { position: absolute; background: rgba(255, 255, 255, 0.4); border-radius: 50%; filter: blur(1px); animation: floatUp infinite linear; }
.p-1 { width: 3px; height: 3px; top: 80%; left: 15%; animation-duration: 12s; opacity: 0.3; }
.p-2 { width: 5px; height: 5px; top: 60%; right: 20%; animation-duration: 16s; opacity: 0.2; animation-delay: 2s; }
.p-3 { width: 2px; height: 2px; top: 90%; left: 70%; animation-duration: 9s; opacity: 0.4; animation-delay: 1s; }
.p-4 { width: 4px; height: 4px; top: 40%; left: 40%; animation-duration: 20s; opacity: 0.25; animation-delay: 4s; }
@keyframes floatUp { 0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; } 10% { opacity: 0.3; } 90% { opacity: 0.3; } 100% { transform: translateY(-200px) translateX(20px) scale(0.8); opacity: 0; } }

/* ── 레이아웃 구조 ── */
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
  to { opacity: 1; transform: translateY(0); }
}

.title-block { margin-bottom: 24px; text-align: left; }
.signin-title { font-size: 38px; font-weight: 400; color: #fff; letter-spacing: 0.02em; font-family: var(--font-display); text-transform: uppercase; }
.signin-sub { margin-top: 6px; font-size: 14px; color: rgba(255,255,255,0.75); font-family: var(--font-body); }

/* 🃏 중앙 대문짝 아바타 카드 디자인 */
.avatar-card-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 0;
}

.avatar-card {
  position: relative;
  width: 280px;            /* 💡 화면에 꽉 차지 않고 예쁘게 떨어지는 너비 */
  aspect-ratio: 4 / 5;     /* 💡 이전 스타일 카드와 통일감을 주는 4:5 비율 */
  border-radius: 28px;     /* 좀 더 부드러운 라운딩 적용 */
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.4);
  
  /* ⭐ 핵심: 아까 원했던 화이트 & 핑크 톤의 은은한 글로우(광채) 상시 발산! */
  box-shadow: 
    0 0 20px rgba(255, 255, 255, 0.4),
    0 0 40px rgba(240, 130, 170, 0.25);
    
  animation: cardFloating 4s ease-in-out infinite; /* 카드 혼자 아련하게 둥둥 뜨는 모션 추가 */
}

@keyframes cardFloating {
  0% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0); }
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 이미지 하단 텍스트 레이어 오버레이 */
.avatar-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 32px 20px 24px 20px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0) 100%);
  text-align: left;
  box-sizing: border-box;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}

.avatar-name {
  font-size: 22px;
  font-weight: 600;
  color: #ffffff;
  font-family: var(--font-body);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 🚀 하단 공통 버튼 */
.action-block { padding: 16px 0 40px 0; }
.btn-continue {
  width: 100%; padding: 14px; background: #fff; color: #c85080; font-size: 14.5px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; border: none; border-radius: 999px; cursor: pointer;
  box-sizing: border-box; transition: all 0.2s ease; font-family: var(--font-body);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.btn-continue:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.15); }
</style>