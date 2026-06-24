<template>
  <div id="app">

    <!-- ── 전역 배경 레이어: 모바일 프레임 영역에만 클립 ── -->
    <div class="bg-frame" aria-hidden="true">
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="orb orb-4"></div>
    </div>

    <!-- ── 화면 카드 레이어 (z-index: 1) ── -->
    <router-view v-slot="{ Component }">
      <transition name="fade">
        <component :is="Component" />
      </transition>
    </router-view>

  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  position: relative;
  width: 100%;
  min-height: 100vh;
}

/* ── 배경 프레임: 모바일 프레임과 동일 크기로 고정, 바깥은 절대 침범 안 함 ── */
.bg-frame {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 500px;
  height: 100vh;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;

  background-color: var(--app-canvas-bg);
}


.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
}

.orb-1 {
  width: 600px; height: 700px;
  background: radial-gradient(circle, var(--orb-2) 0%, transparent 65%);
  top: -200px; left: -100px;
  animation: drift-1 12s ease-in-out infinite;
}
.orb-2 {
  width: 540px; height: 480px;
  background: radial-gradient(circle, var(--orb-3) 0%, transparent 65%);
  top: 0px; right: -220px;
  animation: drift-2 14s ease-in-out infinite;
}
.orb-3 {
  width: 600px; height: 700px;
  background: radial-gradient(circle, var(--orb-5) 0%, transparent 60%);
  bottom: -100px; left: -280px;
  animation: drift-3 10s ease-in-out infinite;
}
.orb-4 {
  width: 600px; height: 400px;
  background: radial-gradient(circle, var(--orb-6) 0%, transparent 60%);
  bottom: -350px; right: -300px;
  animation: drift-4 14s ease-in-out infinite;
}

@keyframes drift-1 {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(140px, 100px); }
  50%  { transform: translate(80px, 180px); }
  75%  { transform: translate(-60px, 80px); }
  100% { transform: translate(0, 0); }
}
@keyframes drift-2 {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(-120px, 90px); }
  50%  { transform: translate(-60px, 200px); }
  75%  { transform: translate(80px, 60px); }
  100% { transform: translate(0, 0); }
}
@keyframes drift-3 {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(160px, -120px); }
  50%  { transform: translate(80px, -200px); }
  75%  { transform: translate(-80px, -100px); }
  100% { transform: translate(0, 0); }
}
@keyframes drift-4 {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(-140px, -80px); }
  50%  { transform: translate(-60px, -180px); }
  75%  { transform: translate(100px, -80px); }
  100% { transform: translate(0, 0); }
}


/* ── 페이드 트랜지션 ── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from
.fade-leave-to {
  opacity: 0;
}

/* 📄 App.vue에 추가 => questionsview에서 빔 페이드효과*/
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
