<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="loading-screen">

        <transition name="txt-fade" mode="out-in">
          <p class="loading-text" :key="currentText">{{ currentText }}</p>
        </transition>

        <div class="dots">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'

const router = useRouter()
const route = useRoute()

const configs = {
  signin: {
    texts: ['시작해볼까요?'],
    next: '/select-style'
  },
  questions: {
    texts: ['이미지 생성 중이에요', '예쁘게 만들고 있어요', '기다리는동안 간단한 질문들을 준비했어요'],
    next: '/questions'
  }
}

const type = route.query.type || 'questions'
const config = configs[type]
const currentText = ref(config.texts[0])

let pollTimer = null
let navigated = false   // 중복 이동 방지

const goNext = () => {
  if (navigated) return
  navigated = true
  if (pollTimer) clearTimeout(pollTimer)
  router.push(config.next)
}

// AI 작업 상태 폴링: 2초 간격으로 done/failed 확인
const pollJobStatus = async () => {
  if (navigated) return

  const jobId = localStorage.getItem('ai_job_id')
  if (!jobId) {
    goNext()
    return
  }

  try {
    const res = await api.get(`/accounts/ai/status/${jobId}/`)
    const { status, generated_url } = res.data

    if (status === 'done') {
      if (generated_url) localStorage.setItem('ai_generated_url', generated_url)
      goNext()
    } else if (status === 'failed') {
      goNext()
    } else {
      // pending / processing → 2초 후 재시도
      pollTimer = setTimeout(pollJobStatus, 2000)
    }
  } catch (e) {
    console.error('AI 상태 조회 실패:', e)
    pollTimer = setTimeout(pollJobStatus, 2000)
  }
}

// 텍스트 3개를 1.8s + 3s + 3s = 7.8s 후 마지막 텍스트 표시 완료
// 그 후 3초(=총 최대 ~11초) 추가 대기 후 AI 미완료여도 강제 이동
const TEXT_ANIMATION_DURATION = 1800 + 3000 + 3000 + 3000  // 마지막 텍스트 표시 후 3s
const MAX_WAIT_MS = TEXT_ANIMATION_DURATION   // ~10.8초

onMounted(() => {
  if (type === 'signin') {
    // 로그인 후 로딩은 텍스트 1개 → 3.5초 후 이동
    setTimeout(() => goNext(), 3500)
    return
  }

  // 텍스트 순환 애니메이션
  let i = 0
  const nextText = () => {
    i++
    if (i < config.texts.length) {
      currentText.value = config.texts[i]
      setTimeout(nextText, 3000)
    }
  }
  setTimeout(nextText, 1800)

  // AI 폴링 시작 (텍스트 애니메이션과 병렬)
  pollTimer = setTimeout(pollJobStatus, 1800)

  // 최대 대기 시간 초과 시 AI 완료 여부와 무관하게 이동
  // (AI 워커 미실행 환경에서도 설문 화면으로 넘어갈 수 있도록)
  setTimeout(() => goNext(), MAX_WAIT_MS)
})

onUnmounted(() => {
  navigated = true   // 언마운트 시 폴링 중단
  if (pollTimer) clearTimeout(pollTimer)
})
</script>

<style scoped>
.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  gap: 32px;
}

.loading-text {
  font-family: var(--font-display);
  font-size: 21px;
  font-weight: 300;
  color: var(--white);
  text-align: center;
  padding: 0 40px;
  line-height: 1.6;
  letter-spacing: 0.02em;
}

.dots {
  display: flex;
  gap: 10px;
  margin-top: 32px;
  align-items: flex-end;
  height: 50px;
}

.dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;  /* 원형으로 */
  background: rgba(255, 255, 255, 0.8);
  animation: squish-bounce 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
}

.dots span:nth-child(1) { animation-delay: 0.0s; }
.dots span:nth-child(2) { animation-delay: 0.3s; }
.dots span:nth-child(3) { animation-delay: 0.6s; }
.dots span:nth-child(4) { animation-delay: 0.9s; }
.dots span:nth-child(5) { animation-delay: 1.2s; }

@keyframes squish-bounce {
  0%   { transform: translateY(0); }
  15%  { transform: translateY(-36px); }
  50%  { transform: translateY(0); }
  100% { transform: translateY(0); }
}

.txt-fade-enter-active,
.txt-fade-leave-active {
  transition: opacity 1s ease, transform 0.5s ease;
}
.txt-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.txt-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>