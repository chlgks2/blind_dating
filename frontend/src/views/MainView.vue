<template>
  <div class="app-shell">
    <div class="mobile-frame">
  
      <div class="main-screen">

        <main class="main-content-area">

          <!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               ORBIT ANIMATION
          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
          <div class="orbit-system">
            <div class="sun" @click="router.push('/select-style')"></div>

            <div class="orbit orbit-1">
              <div class="planet p-1"></div>
            </div>
            <div class="orbit orbit-2">
              <div class="planet p-2"></div>
            </div>
            <div class="orbit orbit-3">
              <div class="planet p-3"></div>
            </div>
            <div class="orbit orbit-4">
              <div class="planet p-4"></div>
            </div>
            <div class="orbit orbit-5">
              <div class="planet p-5"></div>
            </div>
          </div>

        </main>

        <nav class="bottom-nav">
          <button class="nav-btn" :class="{ active: activeNav === 'likes' }" @click="activeNav = 'likes'; router.push('/likes')">
            <Heart :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" :class="{ active: activeNav === 'chat' }" @click="activeNav = 'chat'; router.push('/chatlist')">
            <MessageCircle :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" :class="{ active: activeNav === 'profile' }" @click="activeNav = 'profile'; router.push('/profile')">
            <User :size="22" :stroke-width="1.5" />
          </button>
        </nav>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, MessageCircle, User } from 'lucide-vue-next'

const router = useRouter()
const activeNav = ref('likes')
</script>


<style scoped>
.main-screen {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.main-content-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 100px;
  padding-top: 60px;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ORBIT ANIMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
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
  box-shadow:
  0 0 20px rgba(255, 255, 255, 0.9),
  0 0 50px rgba(255, 255, 255, 0.5),
  0 0 90px rgba(255, 255, 255, 0.2);
  z-index: 10;
  animation: sun-pulse 3s ease-in-out infinite;
  cursor: pointer;
}

@keyframes sun-pulse {
  0%, 100% { transform: scale(1);   box-shadow: 0 0 20px rgba(255,255,255,0.9), 0 0 50px rgba(255,200,220,0.6); }
  50%       { transform: scale(1.1); box-shadow: 0 0 30px rgba(255,255,255,1),   0 0 70px rgba(255,200,220,0.8); }
}

/* 궤도 링 — conic-gradient로 꼬리만 표시 */
.orbit {
  position: absolute;
  border-radius: 50%;
  border: none;
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 2px), white calc(100% - 2px));
  mask: radial-gradient(farthest-side, transparent calc(100% - 2px), white calc(100% - 2px));
}

.orbit-1 {
  width: 165px; height: 165px;
  background: conic-gradient(transparent 0deg, rgba(255,255,255,0.03) 15deg, rgba(255,255,255,0.5) 355deg, transparent 360deg);
  animation: trail-spin 6s linear infinite;
}
.orbit-2 {
  width: 210px; height: 210px;
  background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 15deg, rgba(255,255,255,0.4) 355deg, transparent 360deg);
  animation: trail-spin 20s linear infinite;
}
.orbit-3 {
  width: 290px; height: 290px;
  background: conic-gradient(transparent 0deg, rgba(255,255,255,0.03) 15deg, rgba(255,255,255,0.45) 355deg, transparent 360deg);
  animation: trail-spin 9s linear infinite;
}
.orbit-4 {
  width: 350px; height: 350px;
  background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 80deg, rgba(255,255,255,0.35) 355deg, transparent 360deg);
  animation: trail-spin 14s linear infinite;
}
.orbit-5 {
  width: 440px; height: 440px;
  background: conic-gradient(transparent 0deg, rgba(255,255,255,0.02) 90deg, rgba(255,255,255,0.4) 355deg, transparent 360deg);
  animation: trail-spin 24s linear infinite;
}

@keyframes trail-spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* 행성 */
.planet {
  position: absolute;
  border-radius: 50%;
  top: 50%;
  left: 50%;
}

.p-1 {
  width: 11px; height: 11px;
  margin-top: -5.5px; margin-left: -5.5px;
  background: radial-gradient(circle, #fff 0%, rgba(255,180,200,0.9) 100%);
  box-shadow: 0 0 8px rgba(255,255,255,0.9);
  animation: planet-spin 6s linear infinite;
  transform-origin: -55px 0;
}
.p-2 {
  width: 10px; height: 10px;
  margin-top: -5px; margin-left: -5px;
  background: radial-gradient(circle, #fff 0%, rgba(255,200,220,0.9) 100%);
  box-shadow: 0 0 7px rgba(255,255,255,0.8);
  animation: planet-spin 20s linear infinite;
  transform-origin: -85px 0;
}
.p-3 {
  width: 13px; height: 13px;
  margin-top: -6.5px; margin-left: -6.5px;
  background: radial-gradient(circle, #fff 0%, rgba(255,150,180,0.9) 100%);
  box-shadow: 0 0 10px rgba(255,255,255,0.8);
  animation: planet-spin 9s linear infinite;
  transform-origin: -115px 0;
}
.p-4 {
  width: 10px; height: 10px;
  margin-top: -5px; margin-left: -5px;
  background: radial-gradient(circle, #fff 0%, rgba(200,180,255,0.9) 100%);
  box-shadow: 0 0 7px rgba(255,255,255,0.7);
  animation: planet-spin 14s linear infinite;
  transform-origin: -147.5px 0;
}
.p-5 {
  width: 9px; height: 9px;
  margin-top: -4.5px; margin-left: -4.5px;
  background: radial-gradient(circle, #fff 0%, rgba(230,180,255,0.9) 100%);
  box-shadow: 0 0 7px rgba(255,255,255,0.6);
  animation: planet-spin 24s linear infinite;
  transform-origin: -180px 0;
}

@keyframes planet-spin {
  from { transform: rotate(0deg) translateX(0); }
  to   { transform: rotate(360deg) translateX(0); }
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   NAV BAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
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

.nav-btn:hover {
  color: #fff;
}
</style>