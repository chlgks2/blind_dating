<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <div class="login-body">
        
        <div class="progress-container" v-if="currentIndex < mockQuestions.length">
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <span class="progress-text">{{ currentIndex + 1 }} / {{ mockQuestions.length }}</span>
        </div>

        <div class="title-block" v-if="currentIndex < mockQuestions.length">
          <h1 class="signin-title">Questions</h1>
          <p class="signin-sub">더 끌리는 쪽으로 하트를 밀어보세요</p>
        </div>

        <div class="game-container">
          <div v-if="currentIndex >= mockQuestions.length" class="end-card">
            <h2>답변 완료!</h2>
            <p>프로필 생성이 거의 다 된 것 같네요</p>
            <button class="btn-continue" @click="submitResults">이미지 확인하기</button>
          </div>

          <div v-else class="play-zone">
            <div class="question-header">
              <h2>{{ mockQuestions[currentIndex].text }}</h2>
            </div>

            <div class="split-zone">
              <div class="choice-sector left-sector" :class="{ active: swipeDirection === 'left' }">
                <span class="choice-label">A</span>
                <span class="choice-text">{{ mockQuestions[currentIndex].choice_A }}</span>
              </div>

              <div class="choice-sector right-sector" :class="{ active: swipeDirection === 'right' }">
                <span class="choice-label">B</span>
                <span class="choice-text">{{ mockQuestions[currentIndex].choice_B }}</span>
              </div>

              <!-- <div
                class="heart-picker"
                :style="heartStyle"
                @mousedown="startDrag"
                @touchstart="startDrag"
              >
                <span class="heart-icon">❤️</span>
              </div> -->
              <div
                class="heart-picker"
                :style="heartStyle"
                @mousedown="startDrag"
                @touchstart="startDrag"
              >
                <img src="../assets/heart.png" class="heart-img" draggable="false"/>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

// 백엔드 질문으로 교체 (option_a/option_b → choice_A/choice_B 매핑)
const mockQuestions = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/matching/questions/')
    mockQuestions.value = res.data.map(q => ({
      id: q.id,
      text: `${q.option_a} vs ${q.option_b}`,
      choice_A: q.option_a,
      choice_B: q.option_b,
    }))
  } catch (e) {
    console.error('질문 로드 실패:', e)
  }
})

const currentIndex = ref(0)
const userAnswers = ref([])
const startX = ref(0)
const moveX = ref(0)
const isDragging = ref(false)

const progressPercentage = computed(() => {
  return (currentIndex.value / mockQuestions.value.length) * 100
})

const heartStyle = computed(() => {
  if (!isDragging.value && moveX.value === 0) {
    return { transition: 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)' }
  }
  return {
    transform: `translate(-50%, -50%) translateX(${moveX.value}px) scale(${isDragging.value ? 1.15 : 1})`,
  }
})

const swipeDirection = computed(() => {
  if (moveX.value > 60) return 'right'
  if (moveX.value < -60) return 'left'
  return ''
})

const handleSelect = (choiceCode) => {
  userAnswers.value.push({
    question_id: mockQuestions.value[currentIndex.value].id,
    choice: choiceCode
  })
  currentIndex.value++
  moveX.value = 0
  isDragging.value = false
}

const startDrag = (e) => {
  isDragging.value = true
  const clientX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX
  startX.value = clientX
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('touchmove', onDrag)
  window.addEventListener('mouseup', endDrag)
  window.addEventListener('touchend', endDrag)
}

const onDrag = (e) => {
  if (!isDragging.value) return
  const clientX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX
  let diff = clientX - startX.value
  if (diff > 130) diff = 130
  if (diff < -130) diff = -130
  moveX.value = diff
}

const endDrag = () => {
  if (!isDragging.value) return
  isDragging.value = false
  if (moveX.value > 80) handleSelect('B')
  else if (moveX.value < -80) handleSelect('A')
  else moveX.value = 0
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('touchmove', onDrag)
  window.removeEventListener('mouseup', endDrag)
  window.removeEventListener('touchend', endDrag)
}

const submitResults = async () => {
  try {
    // 백엔드 형식으로 변환: { question: id, selected: 'A'|'B' }
    const payload = userAnswers.value.map(a => ({
      question: a.question_id,
      selected: a.choice,
    }))
    await api.post('/matching/answers/', { answers: payload })
    router.push('/my-avatar')
  } catch (err) {
    console.error('답변 제출 실패:', err)
    router.push('/my-avatar')
  }
}
</script>

<style scoped>

.login-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 32px);
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 35px;
}
.progress-bar-bg {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--orb-5) 0%, var(--orb-6) 100%);
  border-radius: 999px;
  transition: width 0.3s ease;
}
.progress-text {
  font-size: 12px;
  color: #fff;
  font-family: var(--font-display);
  font-weight: 500;
}

.title-block { margin-bottom: 24px; }
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
  font-size: 12px;
  color: var(--text-sub);
  line-height: 1.6;
  font-weight: 300;
}

.game-container {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.play-zone {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin-top: 30px;
}

.question-header {
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 24px;
}
.question-header h2 {
  font-size: 20px;
  color: #fff;
  font-weight: 400;
  line-height: 1.5;
  word-break: keep-all;
  font-family: var(--font-display);
}

.split-zone {
  position: relative;
  flex: 1;
  max-height: 300px;
  display: flex;
  gap: 12px;
}

.choice-sector {
  flex: 1;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
  transition: all 0.3s ease;
}

.choice-sector.active {
  background: rgba(255, 255, 255, 0.35);
  border: 1px solid #fff;
  transform: scale(1.03);
}

.choice-label {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 12px;
  font-family: var(--font-display);
}

.choice-text {
  font-size: 16px;
  color: #fff;
  font-weight: 500;
  line-height: 1.4;
  word-break: keep-all;
  font-family: var(--font-body);
}

/* .heart-picker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 64px;
  height: 64px;
  background: #ffffff;
  border-radius: 50%;
  box-shadow: 0 8px 24px rgba(224, 122, 160, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  cursor: grab;
  z-index: 10;
  user-select: none;
  touch-action: none;
} */

.heart-picker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 64px;
  height: 64px;
  background: none;        /* 흰 원 제거 */
  border-radius: 0;
  box-shadow: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  z-index: 10;
  user-select: none;
  touch-action: none;
}

.heart-img {
  width: 100%;
  height: 100%;
  object-fit: contain;

  pointer-events: none;
  -webkit-user-drag: none;
}

.heart-picker:active { cursor: grabbing; }

.end-card {
  width: 100%;
  height: 340px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  text-align: center;
  font-family: var(--font-body);

  margin-top: 170px;
  animation: fade-up 2s ease forwards;
}
@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.end-card h2 { font-size: 23px; margin-bottom: 10px; font-weight: 400;}
.end-card p { font-size: 14px; opacity: 0.8; margin-bottom: 24px; }


.btn-continue { 
    width: 240px; 
    margin: 0 auto;
    display: block;
    padding: 14px; 
    
    background: linear-gradient(135px, #ffffff 0%, rgba(255, 255, 255, 0.9) 50%, #ffffff 100%);
    background-size: 200% 200%;
    color: var(--app-canvas-bg);
    
    font-size: 15px; 
    font-weight: 500; 
    letter-spacing: 0.03em; 
    text-transform: uppercase; 
    border: none; 
    border-radius: var(--r-pill); /* 💡 999px 대신 토큰 사용 */
    cursor: pointer; 
    box-sizing: border-box; 
    font-family: var(--font-display); 
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