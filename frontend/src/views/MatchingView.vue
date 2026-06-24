<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           BACKGROUND : 딥 스페이스 오브
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
      <div class="bg-orbs" aria-hidden="true">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="orb orb-4"></div>
        <div class="sparkle s1"></div>
        <div class="sparkle s2"></div>
        <div class="sparkle s3"></div>
        <div class="sparkle s4"></div>
      </div>

      <!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           BODY
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
      <div class="matching-body">

        <!-- 상단 타이틀 (카드 선택 시 페이드아웃) -->
        <header class="title-block" :class="{ 'is-hidden': selectedId !== null }">
          <p class="label-tag">BLIND DATING</p>
          <h1 class="matching-title">Soul<br/>Match</h1>
          <p class="matching-sub">당신과 유사도가 높은 5명의 페르소나입니다.</p>
        </header>

        <!-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
             CARDS STAGE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ -->
        <div
          class="cards-stage"
          :class="{ 'has-selection': selectedId !== null }"
          @click.self="closeDetail"
        >
          <!-- 선택 시 뒷배경 딤드 오버레이 -->
          <div class="stage-overlay" @click="closeDetail"></div>

          <div
            v-for="(user, index) in matchingUsers"
            :key="user.id"
            class="scatter-card"
            :class="[
                `card-pos-${index + 1}`,
                { 'is-active': selectedId === user.id },
                { 'is-dimmed': selectedId !== null && selectedId !== user.id },
            ]"
           @click="selectedId === user.id ? null : toggleCard(user.id)"
>
            <!-- 글라스 이미지 래퍼 -->
            <div class="card-glass">
              <img :src="user.image" :alt="user.name" class="card-img" />
              <!-- 이미지 위 글라스 레이어 -->
              <div class="card-glass-overlay"></div>
            </div>

            <!-- 상세 정보 (active 시 슬라이드업) -->
            <div class="card-detail">
              <span class="match-badge">{{ user.similarity }}% MATCH</span>
              <h2 class="user-name">{{ user.name }}</h2>
              <p class="user-bio">"{{ user.bio }}"</p>
              <button class="btn-chat" @click.stop="startChat(user.name)">
                대화하기
              </button>
            </div>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

import boy1 from '@/assets/boy1.png'
import boy2 from '@/assets/boy2.png'
import boy3 from '@/assets/boy3.png'
import boy4 from '@/assets/boy4.png'
import boy5 from '@/assets/boy5.png'

const matchingUsers = ref([
  { id: 1, name: '나는야최한',    similarity: 94, bio: '사이버펑크와 테크를 사랑하는 디자이너', image: boy1 },
  { id: 2, name: '최한입니다',      similarity: 88, bio: '밤샘 코딩과 에스프레소를 즐기는 개발자', image: boy2 },
  { id: 3, name: '최한', similarity: 82, bio: '몽환적인 보라색 오로라를 그리는 사람',  image: boy3 },
  { id: 4, name: '최영우',      similarity: 79, bio: '레트로 게임과 도트 아트를 수집합니다',  image: boy4 },
  { id: 5, name: '나는최영우',      similarity: 75, bio: '달빛 아래서 새로운 브랜딩 기획하기',    image: boy5 },
])

const selectedId = ref(null)

const toggleCard = (id) => {
  selectedId.value = selectedId.value === id ? null : id
}

const closeDetail = () => {
  selectedId.value = null
}

const startChat = (name) => {
  router.push({ path: '/payment', query: { userName: name } })
}
</script>

<style scoped>
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   BACKGROUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.bg-orbs {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  animation: orb-drift ease-in-out infinite alternate;
}

.orb-1 {
  width: 320px; height: 320px;
  background: radial-gradient(circle, var(--orb-1) 0%, transparent 70%);
  top: -100px; left: -80px;
  animation-duration: 14s;
}
.orb-2 {
  width: 260px; height: 260px;
  background: radial-gradient(circle, var(--orb-2) 0%, transparent 70%);
  top: 30%; right: -70px;
  animation-duration: 18s;
  animation-direction: alternate-reverse;
}
.orb-3 {
  width: 220px; height: 220px;
  background: radial-gradient(circle, var(--orb-3) 0%, transparent 70%);
  bottom: 10%; left: -40px;
  animation-duration: 11s;
}
.orb-4 {
  width: 160px; height: 160px;
  background: radial-gradient(circle, var(--orb-4) 0%, transparent 70%);
  bottom: 20%; right: 10%;
  animation-duration: 16s;
  animation-direction: alternate-reverse;
}

@keyframes orb-drift {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(20px, 28px) scale(1.08); }
}


/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   BODY LAYOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.matching-body {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 52px 24px 0;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   HEADER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.title-block {
  flex-shrink: 0;
  margin-bottom: 20px;
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.title-block.is-hidden {
  opacity: 0;
  transform: translateY(-16px);
  pointer-events: none;
}

.label-tag {
  font-family: var(--font-display);
  font-size: 10px;
  letter-spacing: 0.3em;
  color: var(--neon-purple);
  margin-bottom: 8px;
  text-shadow: 0 0 12px var(--neon-glow);
}

.matching-title {
  font-family: var(--font-display);
  font-size: 42px;
  font-weight: 400;
  color: #fff;
  line-height: 1.05;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  text-shadow:
    0 0 40px rgba(167,139,250,0.3),
    0 0 80px rgba(167,139,250,0.15);
}

.matching-sub {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   CARDS STAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.cards-stage {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stage-overlay {
  position: fixed;
  inset: 0;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.45s ease;
  z-index: 5;
}
.has-selection .stage-overlay {
  opacity: 1;
  pointer-events: auto;
  cursor: pointer;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   SCATTER CARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.scatter-card {
  position: absolute;
  width: 160px;
  aspect-ratio: 4 / 5;
  border-radius: 18px;
  overflow: visible;
  cursor: pointer;
  transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
  z-index: 10;
}

/* 글라스 이미지 래퍼 */
.card-glass {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--dark-border);
  box-shadow:
    0 8px 32px rgba(0,0,0,0.5),
    inset 0 1px 0 rgba(255,255,255,0.08);
  transition: border-color 0.4s, box-shadow 0.4s;
  flex-shrink: 0;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.6s ease;
}

/* 글라스 반사 레이어 */
.card-glass-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.12) 0%,
    rgba(255,255,255,0.02) 45%,
    rgba(167,139,250,0.06) 100%
  );
  border-top: 1px solid rgba(255,255,255,0.20);
  border-radius: 18px;
  pointer-events: none;
}

/* ── 산개 위치 ── */
.card-pos-1 { transform: translate(-105px, -160px) rotate(-13deg); }
.card-pos-2 { transform: translate(108px,  -115px) rotate(11deg);  }
.card-pos-3 { transform: translate(-110px,  95px)  rotate(-9deg);  }
.card-pos-4 { transform: translate(105px,  145px)  rotate(15deg);  }
.card-pos-5 { transform: translate(0px,   -12px)   rotate(-2deg);  z-index: 11; }

/* ── 액티브 : 중앙으로 오며 화면에 꽉 차게 ── */
.scatter-card.is-active {
  transform: translate(0, 0) rotate(0deg) scale(2.15) !important;
  z-index: 100;
  cursor: default;
}
.scatter-card.is-active .card-glass {
  border-color: var(--dark-border-hi);
  box-shadow:
    0 0 0 1px rgba(167,139,250,0.25),
    0 24px 60px rgba(0,0,0,0.75),
    0 0 50px rgba(167,139,250,0.18);
}
.scatter-card.is-active .card-glow-ring {
  opacity: 1;
}
.scatter-card.is-active .card-img {
  transform: scale(1.04);
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   CARD DETAIL INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.card-detail {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;

  padding: 40px 14px 14px;
  text-align: left;
  
  background: linear-gradient(
    to top,
    rgba(6, 8, 26, 0.96) 0%,
    rgba(6, 8, 26, 0.72) 55%,
    transparent 100%
  );
  border-radius: 0 0 18px 18px;
  box-sizing: border-box;

  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.35s ease 0.28s, transform 0.35s ease 0.28s;
  pointer-events: none;
  z-index: 3;
}
.is-active .card-detail {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.match-badge {
  display: inline-block;
  padding: 2px 7px;
  font-family: var(--font-display);
  font-size: 7.5px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: var(--neon-purple);
  background: rgba(167,139,250,0.14);
  border: 1px solid rgba(167,139,250,0.35);
  border-radius: 999px;
  margin-bottom: 5px;
  text-shadow: 0 0 8px var(--neon-glow);
}

.user-name {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  margin: 0 0 3px;
  letter-spacing: 0.02em;
}

.user-bio {
  font-size: 8.5px;
  color: var(--text-muted);
  line-height: 1.4;
  margin-bottom: 10px;
}

.btn-chat {
  width: 100%;
  padding: 7px 0;
  background: rgba(167,139,250,0.12);
  color: #fff;
  border: 1px solid rgba(167,139,250,0.38);
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 8.5px;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
  backdrop-filter: blur(8px);
}
.btn-chat:hover {
  background: rgba(167,139,250,0.28);
  border-color: rgba(167,139,250,0.65);
  box-shadow: 0 0 16px rgba(167,139,250,0.28);
}

@media (prefers-reduced-motion: reduce) {
  .orb, .sparkle { animation: none; }
}
</style>