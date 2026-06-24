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
          <p class="signin-sub">더 끌리는 쪽으로 하트를 밀어보세요!</p>
        </div>

        <div class="game-container">
          <div v-if="currentIndex >= mockQuestions.length" class="end-card">
            <h2>모든 질문 완료!</h2>
            <p>취향 분석 데이터가 준비되었습니다.</p>
            <button class="btn-submit" @click="submitResults">프로필 이미지 확인하기</button>
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

              <div
                class="heart-picker"
                :style="heartStyle"
                @mousedown="startDrag"
                @touchstart="startDrag"
              >
                <span class="heart-icon">❤️</span>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const mockQuestions = ref([
  { id: 1, text: '붕어빵 먹을 때 당신의 선택은?', choice_A: '머리부터', choice_B: '꼬리부터' },
  { id: 2, text: '면 요리와 밥 요리 중 더 좋아하는 것은?', choice_A: '든든한 밥', choice_B: '호로록 면' },
  { id: 3, text: '주말을 보내는 이상적인 방법은?', choice_A: '집에서 넷플릭스', choice_B: '밖에서 친구들과' },
  { id: 4, text: '과제를 할 때 당신의 스타일은?', choice_A: '미리미리 계획대로', choice_B: '벼락치기 스릴러' },
  { id: 5, text: '더 참을 수 없는 상태는?', choice_A: '배고픈 건 못참아', choice_B: '졸린 건 못참아' },
])

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
    console.log('최종 Django 전송 묶음:', userAnswers.value)
    router.push('/my-avatar')
  } catch (err) {
    console.error(err)
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

.heart-picker {
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
}
.end-card h2 { font-size: 24px; margin-bottom: 10px; }
.end-card p { font-size: 14px; opacity: 0.8; margin-bottom: 24px; }
.btn-submit { padding: 14px 28px; background: #fff; color: #e07aa0; border: none; border-radius: 999px; font-weight: 600; cursor: pointer; }

</style>