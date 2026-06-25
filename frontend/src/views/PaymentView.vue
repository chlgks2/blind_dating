<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="payment-screen">

        <div class="payment-card">
          <h2 class="payment-title">{{ userName }}님과의<br/>대화를 위해<br/>결제가 필요해요</h2>
          <div class="payment-info">
            <p class="payment-sub">상대방도 결제를 하면 대화가 시작됩니다!</p>
            <p class="payment-sub">하지않으면 자동으로 환불됩니다</p>
          </div>

          <div class="payment-btns">
            <button class="btn-pay" @click="handlePayment">결제하기</button>
            <button class="btn-back" @click="router.back()">뒤로가기</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const userName = route.query.userName || '상대방'

const handlePayment = () => {
  // 결제 SDK 연결 자리
  console.log('결제 시작:', userName)
}
</script>

<style scoped>
.payment-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

.payment-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.payment-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 400;
  color: #fff;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

.payment-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.562);
  line-height: 1.6;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0px;
} 

.payment-btns {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.btn-pay {
  width: 100%;
  padding: 14px;
  background: #fff;
  color: var(--app-canvas-bg);
  border: none;
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: transform 0.14s ease;
}

.btn-pay:active {
  transform: scale(0.97);
}

.btn-back {
  width: 100%;
  padding: 14px;
  background: none;
  color: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 5\600;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}

.btn-back:hover {
  border-color: rgba(255, 255, 255, 0.4);
  color: #fff;
}
</style>