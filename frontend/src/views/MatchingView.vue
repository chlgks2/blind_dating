<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="matching-body">

        <header class="title-block" :class="{ 'is-hidden': selectedId !== null }">
          
          <h1 class="matching-title">Soul<br/>Match</h1>
          <p class="matching-sub">잘 맞을 것 같은 다섯 명을 골라봤어요</p>
        </header>

        <div class="selected-name" :class="{ 'is-visible': selectedId !== null }">
          {{ matchingUsers.find(u => u.id === selectedId)?.name }}님과
          {{ matchingUsers.find(u => u.id === selectedId)?.similarity }}% 취향이 비슷해요
        </div>

        <div class="cards-stage" :class="{ 'has-selection': selectedId !== null }" @click.self="closeDetail">
          <div class="stage-overlay" @click="closeDetail"></div>

          <div
            v-for="(user, index) in matchingUsers"
            :key="user.id"
            class="scatter-card"
            :class="[`card-pos-${index + 1}`, { 'is-active': selectedId === user.id }, { 'is-dimmed': selectedId !== null && selectedId !== user.id }]"
            @click="selectedId === user.id ? null : toggleCard(user.id)"
          >
            <div class="card-glass">
              <img :src="user.image" :alt="user.name" class="card-img" />
              <div class="card-glass-overlay"></div>
            </div>

            <div class="sparkle-container">
              <span class="sp sp-1">✦</span>
              <span class="sp sp-2">✦</span>
              <span class="sp sp-3">✦</span>
              <span class="sp sp-4">✦</span>
              <span class="sp sp-5">✦</span>
              <span class="sp sp-6">✦</span>
            </div>

            <div class="card-detail">
              <div class="card-detail-row">
                <button class="btn-heart" @click.stop="toggleLike(user.id)">
                  <Heart :size="18" :stroke-width="1.5" :fill="likedIds.has(user.id) ? '#fff' : 'none'" color="#fff" />
                </button>
                <div class="action-btns">
                  <button class="icon-btn" @click.stop="sendFriendRequest(user.id)">
                    <UserPlus :size="11" />
                  </button>
                  <button class="icon-btn" @click.stop="startChat(user.name)">
                    <MessageCircle :size="11" />
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>

        <div class="bottom-nav" :class="{ 'is-hidden': selectedId !== null }">
          <button class="btn-home" @click="router.push('/')">
            <Home :size="18" :stroke-width="1.5" />
          </button>
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

const sendFriendRequest = (id) => {
  console.log('친구 요청:', id)
  // 나중에 API 연결
}

const startChat = (name) => {
  router.push({ path: '/payment', query: { userName: name } })
}

const likedIds = ref(new Set())

const toggleLike = (id) => {
  if (likedIds.value.has(id)) {
    likedIds.value.delete(id)
  } else {
    likedIds.value.add(id)
  }
  likedIds.value = new Set(likedIds.value) // 반응성 트리거
}

import { Heart, UserPlus, MessageCircle, Home } from 'lucide-vue-next'

</script>

<style scoped>
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   BODY LAYOUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
.matching-body {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 60px 24px 50px;
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

.selected-name {
  position: absolute;
  top: 52px;
  left: 0;
  width: 100%;
  text-align: center;
  margin-top: 50px;

  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 300;
  color: #fff;
  opacity: 0;
  transform: translateY(-8px);
  transition: opacity 0.4s ease, transform 0.4s ease;
  pointer-events: none;
  z-index: 20;
}

.selected-name.is-visible {
  opacity: 1;
  transform: translateY(0);
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

.bottom-nav {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
  z-index: 50;

  transition: opacity 0.4s ease, transform 0.4s ease;
}

.bottom-nav.is-hidden {
  opacity: 0;
  transform: translateX(-50%) translateY(8px);  /* translateX 유지 */
  pointer-events: none;
}

.btn-home {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, transform 0.15s ease;
  box-shadow:
    0 0 12px rgba(255, 255, 255, 0.4),
    0 0 28px rgba(255, 255, 255, 0.2),
    0 0 50px rgba(255, 200, 220, 0.15);
  animation: home-glow 5s ease-in-out infinite;
}

@keyframes home-glow {
  0%, 100% {
    box-shadow:
      0 0 12px rgba(255, 255, 255, 0.4),
      0 0 28px rgba(255, 255, 255, 0.2),
      0 0 50px rgba(255, 200, 220, 0.15);
  }
  50% {
    box-shadow:
      0 0 18px rgba(255, 255, 255, 0.6),
      0 0 40px rgba(255, 255, 255, 0.3),
      0 0 70px rgba(255, 200, 220, 0.25);
  }
}

.btn-home:hover {
  background: rgba(255, 255, 255, 0.45);
  transform: scale(1.1);
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
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 60%, transparent 100%);
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

  animation: floating ease-in-out infinite;
}

.card-pos-1 { transform: translate(-105px, -160px) rotate(-13deg); animation-duration: 3.2s; animation-delay: 0.0s; }
.card-pos-2 { transform: translate(108px,  -115px) rotate(11deg);  animation-duration: 4.1s; animation-delay: 2.3s; }
.card-pos-3 { transform: translate(-110px,  95px)  rotate(-9deg);  animation-duration: 3.7s; animation-delay: 1.0s; }
.card-pos-4 { transform: translate(105px,  145px)  rotate(15deg);  animation-duration: 4.5s; animation-delay: 3.1s; }
.card-pos-5 { transform: translate(0px,   -12px)   rotate(-2deg);  animation-duration: 3.9s; animation-delay: 1.7s; }

@keyframes floating {
  0%   { translate: 0 0; }
  50%  { translate: 0 -10px; }
  100% { translate: 0 0; }
}

/* 글라스 이미지 래퍼 */
.card-glass {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
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
    rgba(250, 139, 206, 0.06) 100%
  );
  border-top: 1px solid rgba(255,255,255,0.20);
  border-radius: 18px;
  pointer-events: none;
}

/* ── 액티브 : 중앙으로 오며 화면에 꽉 차게 ── */
.scatter-card.is-active {
  transform: translate(0, 0) rotate(0deg) scale(2.15) !important;
  z-index: 100;
  cursor: default;

}

.scatter-card.is-active .card-glass {
  border-color: var(--dark-border-hi);
  animation: card-aura 3s linear infinite;
}

@keyframes card-aura {
  0%   { box-shadow: 0 0 40px rgba(255,236,242,0.6), 0 0 80px rgba(255,141,208,0.3); }
  33%  { box-shadow: 0 0 60px rgba(255,255,255,0.8), 0 0 100px rgba(255,200,230,0.5); }
  66%  { box-shadow: 0 0 30px rgba(255,141,208,0.6), 0 0 70px rgba(255,236,242,0.4); }
  100% { box-shadow: 0 0 40px rgba(255,236,242,0.6), 0 0 80px rgba(255,141,208,0.3); }
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
  padding: 20px 14px 14px;
 
  border-radius: 0 0 18px 18px;
  box-sizing: border-box;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.35s ease 0.28s, transform 0.35s ease 0.28s;
  pointer-events: none;
  z-index: 3;

  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.3) 0%,
    transparent 100%
  );
}

.is-active .card-detail {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.card-detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.match-badge {
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 100;
  color: var(--font-body);
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

.action-btns {
  display: flex;
  gap: 6px;
}

.icon-btn {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, transform 0.15s ease;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.45);
  transform: scale(1.1);
}

.icon-btn:active {
  transform: scale(0.9);
}

.btn-heart {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  transition: transform 0.15s ease;
}
.btn-heart:active {
  animation: heart-pop 0.25s ease;
}

.heart-empty {
  font-size: 22px;
  color: #fff;
  text-shadow: 0 0 8px rgba(255,255,255,0.6);
}
.heart-filled {
  font-size: 22px;
  color: #ff6b9d;
  text-shadow: 0 0 10px rgba(255,107,157,0.8);
  animation: heart-pop 0.25s ease;
}

@keyframes heart-pop {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.35); }
  100% { transform: scale(1); }
}


@media (prefers-reduced-motion: reduce) {
  .orb, .sparkle { animation: none; }
}

.sparkle-container {
  position: absolute;
  inset: -20px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 4;
}

.is-active .sparkle-container {
  opacity: 1;
}

.sp {
  position: absolute;
  color: rgba(255, 255, 255, 0.9);
  font-size: 10px;
  animation: sparkle-float 8s ease-in-out infinite;
  text-shadow: 0 0 6px #fff, 0 0 12px #fff;
}

.sp-1 { top: 10%;  left: 5%;   animation-delay: 0.0s; font-size: 8px; animation-duration: 2.0s;  }
.sp-2 { top: 25%;  right: 3%;  animation-delay: 0.6s; font-size: 12px; animation-duration: 2.8s; }
.sp-3 { top: 60%;  left: 2%;   animation-delay: 1.1s; font-size: 7px; animation-duration: 1.8s; }
.sp-4 { top: 5%;   right: 10%; animation-delay: 0.3s; font-size: 10px; animation-duration: 3.1s; }
.sp-5 { bottom: 15%; left: 10%; animation-delay: 0.9s; font-size: 9px; animation-duration: 2.4s; }
.sp-6 { bottom: 5%;  right: 8%; animation-delay: 1.5s; font-size: 11px; animation-duration: 1.6s; }

@keyframes sparkle-float {
  0%   { transform: translateY(0)    scale(0.8); opacity: 0; }
  30%  { opacity: 1; }
  70%  { opacity: 0.7; }
  100% { transform: translateY(-18px) scale(1.2); opacity: 0; }
}
</style>