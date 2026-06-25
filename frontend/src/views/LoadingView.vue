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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

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

onMounted(() => {
  let i = 0
  const next = () => {
    i++
    if (i < config.texts.length) {
      currentText.value = config.texts[i]
      setTimeout(next, 3000)
    } else {
      router.push(config.next)
    }
  }
  setTimeout(next, type === 'signin' ? 3500 : 1800)
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