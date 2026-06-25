<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <!-- ── 로그인된 유저: 매칭 홈 ── -->
      <div v-if="isLoggedIn" class="main-screen" @click="handleLoggedInClick">

        <main class="main-content-area">
          <div class="orbit-system">
            <div class="sun"></div>
            <div class="orbit orbit-1"><div class="planet p-1"></div></div>
            <div class="orbit orbit-2"><div class="planet p-2"></div></div>
            <div class="orbit orbit-3"><div class="planet p-3"></div></div>
            <div class="orbit orbit-4"><div class="planet p-4"></div></div>
            <div class="orbit orbit-5"><div class="planet p-5"></div></div>
          </div>
        </main>

        <nav class="bottom-nav">
          <button class="nav-btn" :class="{ active: activeNav === 'likes' }"
            @click.stop="activeNav = 'likes'; router.push('/friend-requests')">
            <Heart :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" :class="{ active: activeNav === 'chat' }"
            @click.stop="activeNav = 'chat'; router.push('/chatlist')">
            <MessageCircle :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" :class="{ active: activeNav === 'profile' }"
            @click.stop="activeNav = 'profile'; router.push('/profile')">
            <User :size="22" :stroke-width="1.5" />
          </button>
        </nav>

      </div>

      <!-- ── 비로그인 유저: 랜딩 페이지 ── -->
      <div v-else class="landing-screen" @click="router.push('/signin')">

        <div class="landing-orbit-bg">
          <div class="orbit orbit-1"><div class="planet p-1"></div></div>
          <div class="orbit orbit-2"><div class="planet p-2"></div></div>
          <div class="orbit orbit-3"><div class="planet p-3"></div></div>
          <div class="orbit orbit-4"><div class="planet p-4"></div></div>
          <div class="orbit orbit-5"><div class="planet p-5"></div></div>
        </div>

        <div class="landing-content">
          <p class="landing-eyebrow">BLIND DATING</p>
          <h1 class="landing-title">당신의<br/>인연을<br/>찾아요</h1>
          <p class="landing-sub">AI가 만든 아바타로 시작하는<br/>블라인드 소개팅</p>
        </div>

        <div class="landing-bottom">
          <div class="tap-hint">
            <span class="tap-dot"></span>
            화면을 터치해 시작하세요
          </div>
          <div class="auth-links" @click.stop>
            <button class="btn-signin" @click="router.push('/signin')">로그인</button>
            <button class="btn-signup" @click="router.push('/signup')">회원가입</button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, MessageCircle, User } from 'lucide-vue-next'

const router = useRouter()
const isLoggedIn = !!localStorage.getItem('access')
const activeNav = ref('')

// 로그인된 유저가 오빗 영역 클릭 → 매칭으로 이동
const handleLoggedInClick = () => {
  router.push('/matching')
}
</script>

<style scoped>
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   공통 - 오빗 시스템
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.orbit {
  position: absolute;
  border-radius: 50%;
  border: none;
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 2px), white calc(100% - 2px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 2px), white calc(100% - 2px));
}

.orbit-1 { width: 165px; height: 165px; background: conic-gradient(transparent 0deg, rgba(255,255,255,0.03) 15deg, rgba(255,255,255,0.5) 355deg, transparent 360deg); animation: trail-spin 6s linear infinite; }
.orbit-2 { width: 210px; height: 210px; background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 15deg, rgba(255,255,255,0.4) 355deg, transparent 360deg); animation: trail-spin 20s linear infinite; }
.orbit-3 { width: 290px; height: 290px; background: conic-gradient(transparent 0deg, rgba(255,255,255,0.03) 15deg, rgba(255,255,255,0.45) 355deg, transparent 360deg); animation: trail-spin 9s linear infinite; }
.orbit-4 { width: 350px; height: 350px; background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 80deg, rgba(255,255,255,0.35) 355deg, transparent 360deg); animation: trail-spin 14s linear infinite; }
.orbit-5 { width: 440px; height: 440px; background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 90deg, rgba(255,255,255,0.4) 355deg, transparent 360deg); animation: trail-spin 24s linear infinite; }

@keyframes trail-spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

.planet { position: absolute; border-radius: 50%; top: 50%; left: 50%; }
.p-1 { width: 11px; height: 11px; margin-top: -5.5px; margin-left: -5.5px; background: radial-gradient(circle, #fff 0%, rgba(255,180,200,0.9) 100%); box-shadow: 0 0 8px rgba(255,255,255,0.9); animation: planet-spin 6s linear infinite; transform-origin: -55px 0; }
.p-2 { width: 10px; height: 10px; margin-top: -5px; margin-left: -5px; background: radial-gradient(circle, #fff 0%, rgba(255,200,220,0.9) 100%); box-shadow: 0 0 7px rgba(255,255,255,0.8); animation: planet-spin 20s linear infinite; transform-origin: -85px 0; }
.p-3 { width: 13px; height: 13px; margin-top: -6.5px; margin-left: -6.5px; background: radial-gradient(circle, #fff 0%, rgba(255,150,180,0.9) 100%); box-shadow: 0 0 10px rgba(255,255,255,0.8); animation: planet-spin 9s linear infinite; transform-origin: -115px 0; }
.p-4 { width: 10px; height: 10px; margin-top: -5px; margin-left: -5px; background: radial-gradient(circle, #fff 0%, rgba(200,180,255,0.9) 100%); box-shadow: 0 0 7px rgba(255,255,255,0.7); animation: planet-spin 14s linear infinite; transform-origin: -147.5px 0; }
.p-5 { width: 9px; height: 9px; margin-top: -4.5px; margin-left: -4.5px; background: radial-gradient(circle, #fff 0%, rgba(230,180,255,0.9) 100%); box-shadow: 0 0 7px rgba(255,255,255,0.6); animation: planet-spin 24s linear infinite; transform-origin: -180px 0; }

@keyframes planet-spin {
  from { transform: rotate(0deg) translateX(0); }
  to   { transform: rotate(360deg) translateX(0); }
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   로그인된 유저 화면 (기존)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.main-screen {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  cursor: pointer;
}

.main-content-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 100px;
  padding-top: 60px;
}

.orbit-system {
  position: relative;
  width: 380px;
  height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sun {
  position: absolute;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: radial-gradient(circle, #fff 0%, rgba(255, 220, 230, 0.9) 50%, transparent 100%);
  box-shadow: 0 0 20px rgba(255,255,255,0.9), 0 0 50px rgba(255,255,255,0.5), 0 0 90px rgba(255,255,255,0.2);
  z-index: 10;
  animation: sun-pulse 3s ease-in-out infinite;
}

@keyframes sun-pulse {
  0%, 100% { transform: scale(1);   box-shadow: 0 0 20px rgba(255,255,255,0.9), 0 0 50px rgba(255,200,220,0.6); }
  50%       { transform: scale(1.1); box-shadow: 0 0 30px rgba(255,255,255,1),   0 0 70px rgba(255,200,220,0.8); }
}

.bottom-nav {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  padding: 6px 10px;
  z-index: 50;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  width: 52px;
  height: 40px;
  border-radius: 999px;
  transition: background 0.25s ease, color 0.25s ease;
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  width: 64px;
}

.nav-btn:hover { color: #fff; }

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   비로그인 랜딩 화면
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.landing-screen {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
  cursor: pointer;
  overflow: hidden;
}

/* 오빗 배경 (장식용) */
.landing-orbit-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 440px;
  height: 440px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  opacity: 0.6;
}

/* 텍스트 컨텐츠 */
.landing-content {
  position: relative;
  z-index: 1;
  padding: 80px 32px 0;
  animation: fade-up 1s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.landing-eyebrow {
  font-family: var(--font-display);
  font-size: 11px;
  letter-spacing: 0.22em;
  color: rgba(255, 255, 255, 0.45);
  margin: 0 0 20px;
  text-transform: uppercase;
}

.landing-title {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 300;
  color: #fff;
  line-height: 1.08;
  letter-spacing: -0.01em;
  margin: 0 0 20px;
  text-shadow: 0 0 60px rgba(255, 180, 210, 0.3);
}

.landing-sub {
  font-size: 13px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.7;
  margin: 0;
}

/* 하단 */
.landing-bottom {
  position: relative;
  z-index: 1;
  padding: 0 32px 52px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fade-up 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
}

.tap-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  font-family: var(--font-display);
  letter-spacing: 0.04em;
}

.tap-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  animation: dot-pulse 2s ease-in-out infinite;
}

@keyframes dot-pulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50%       { opacity: 1;   transform: scale(1.3); }
}

.auth-links {
  display: flex;
  gap: 10px;
}

.btn-signin {
  flex: 1;
  padding: 14px;
  background: #fff;
  color: #1a0a12;
  border: none;
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: transform 0.14s ease;
}

.btn-signin:active { transform: scale(0.97); }

.btn-signup {
  flex: 1;
  padding: 14px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s, transform 0.14s ease;
}

.btn-signup:hover  { background: rgba(255, 255, 255, 0.18); }
.btn-signup:active { transform: scale(0.97); }
</style>
