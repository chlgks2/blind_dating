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
                <span class="heart-icon">💖</span>
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

// 1. Django 구조 맞춤형 밸런스 게임 덤프 데이터
const mockQuestions = ref([
  { id: 1, text: '붕어빵 먹을 때 당신의 선택은?', choice_A: '머리부터', choice_B: '꼬리부터' },
  { id: 2, text: '면 요리와 밥 요리 중 더 좋아하는 것은?', choice_A: '든든한 밥', choice_B: '호로록 면' },
  { id: 3, text: '주말을 보내는 이상적인 방법은?', choice_A: '집에서 넷플릭스', choice_B: '밖에서 친구들과' },
  { id: 4, text: '과제를 할 때 당신의 스타일은?', choice_A: '미리미리 계획대로', choice_B: '벼락치기 스릴러' },
  { id: 5, text: '더 참을 수 없는 상태는?', choice_A: '배고픈 건 못참아', choice_B: '졸린 건 못참아' },
])

const currentIndex = ref(0)
const userAnswers = ref([])

const progressPercentage = computed(() => {
  return (currentIndex.value / mockQuestions.value.length) * 100
})

// ... 기존 코드 아래에 추가
const startX = ref(0)
const moveX = ref(0)
const isDragging = ref(false)

// 💖 사용자가 드래그하는 만큼 하트 옮기기 (X축만 제어)
const heartStyle = computed(() => {
  if (!isDragging.value && moveX.value === 0) {
    return { transition: 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)' } // 제자리 튕겨올 때 쫀득한 탄성 효과
  }
  return {
    transform: `translate(-50%, -50%) translateX(${moveX.value}px) scale(${isDragging.value ? 1.15 : 1})`,
  }
})

// 하트가 움직인 거리에 따라 어느 쪽 선택지가 켜지는지 감지
const swipeDirection = computed(() => {
  if (moveX.value > 60) return 'right'   // 오른쪽 B 선택
  if (moveX.value < -60) return 'left'   // 왼쪽 A 선택
  return ''
})
// 3. 사용자가 한쪽으로 하트를 던졌을 때 액션 확정
const handleSelect = (choiceCode) => {
  userAnswers.value.push({
    question_id: mockQuestions.value[currentIndex.value].id,
    choice: choiceCode // 'A' 또는 'B' 가 깔끔하게 기록됨
  })

  console.log('현재까지 쌓인 밸런스 결과 데이터:', userAnswers.value)
  
  // 다음 카드로 점프 및 마우스 드래그 리셋
  currentIndex.value++
  moveX.value = 0
  isDragging.value = false
}
// 4. 마우스 & 터치 이벤트 통합 핸들러
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
  
  // 모바일 프레임 범위를 너무 벗어나지 않게 최대 드래그 폭 제한 (-130px ~ 130px)
  let diff = clientX - startX.value
  if (diff > 130) diff = 130
  if (diff < -130) diff = -130
  
  moveX.value = diff
}

const endDrag = () => {
  if (!isDragging.value) return
  isDragging.value = false
  // 손을 뗐을 때 문턱값(80px)을 넘었으면 해당 방향 선택지로 확정
  if (moveX.value > 80) {
    handleSelect('B') // 오른쪽으로 밀었으므로 B 선택
  } else if (moveX.value < -80) {
    handleSelect('A') // 왼쪽으로 밀었으므로 A 선택
  } else {
    moveX.value = 0   // 애매하게 밀다 말았으면 자석처럼 정중앙으로 복귀!
  }
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('touchmove', onDrag)
  window.removeEventListener('mouseup', endDrag)
  window.removeEventListener('touchend', endDrag)
}

const submitResults = async () => {
  try {
    // const res = await api.post('/accounts/save-balance/', { answers: userAnswers.value })

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
  margin-top: 32px; /* 상단 프로그레스바 영역 확보를 위해 살짝 조정 */
  display: flex;
  flex-direction: column;
  height: calc(100vh - 32px);
}

/* 📊 프로그레스 바 스타일 */
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
  transition: width 0.3s ease; /* 게이지 부드럽게 차오르는 애니메이션 */
}
.progress-text {
  font-size: 12px;
  color: #fff;
  font-family: var(--font-display);
  font-weight: 500;
}

.title-block { 
  margin-bottom: 24px; 
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
  font-size: 12px;
  color: var(--text-sub);
  line-height: 1.6;
  font-weight: 300;
}


/* 🎮 게임 보드 메인 플레이 존 */
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

/* 하단 쪼개지는 섹터 카드 인터페이스 */
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
  border: 1px solid rgba(255, 255, 255, 0.35);
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

/* 하트가 한쪽으로 밀릴 때 섹션이 반응하여 하이라이트 효과 (디자이너 픽 포인트) */
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

/* 💖 정중앙 드래그 전용 하트 오버레이 */
.heart-picker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 중심 정렬 */
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



/* 완료 카드 */
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