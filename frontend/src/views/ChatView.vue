<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="chat-screen">

        <header class="chat-header">
          <button class="btn-back" @click="router.back()">
            <ChevronLeft :size="22" :stroke-width="1.5" />
          </button>
          <h2 class="chat-partner-name">{{ userName }}</h2>
          <div class="header-right"></div>
        </header>

        <div class="messages-area">
          <div class="msg msg-other">
            <div class="bubble bubble-other">안녕하세요 😊</div>
            <span class="msg-time">10:09 PM</span>
          </div>
          <div class="msg msg-me">
            <div class="bubble bubble-me">안녕하세요!</div>
            <span class="msg-time">10:10 PM</span>
          </div>
          <div class="msg msg-other">
            <div class="bubble bubble-other">반가워요 ✨</div>
            <span class="msg-time">10:11 PM</span>
          </div>
        </div>

        <div class="input-area">
          <input
            v-model="inputText"
            class="msg-input"
            placeholder="메시지를 입력하세요..."
            @keyup.enter="sendMessage"
          />
          <button class="btn-send" @click="sendMessage">
            <Send :size="16" :stroke-width="1.5" />
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ChevronLeft, Send } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const userName = route.query.userName || '상대방'
const inputText = ref('')

const sendMessage = () => {
  if (!inputText.value.trim()) return
  console.log('전송:', inputText.value)
  inputText.value = ''
}
</script>

<style scoped>
.chat-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 52px 20px 16px;
  flex-shrink: 0;
}

.btn-back {
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0;
}

.chat-partner-name {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.02em;
}

.header-right {
  width: 22px;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.messages-area::-webkit-scrollbar {
  display: none;
}

.msg {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.msg-other { align-items: flex-start; }
.msg-me    { align-items: flex-end; }

.bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 18px;
  font-size: 13px;
  line-height: 1.5;
}

.bubble-other {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  border-top-left-radius: 4px;
}

.bubble-me {
  background: rgba(255, 180, 210, 0.35);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 180, 210, 0.3);
  color: #fff;
  border-top-right-radius: 4px;
}

.msg-time {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.35);
}

.input-area {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px 36px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.msg-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 999px;
  padding: 10px 18px;
  color: #fff;
  font-size: 13px;
  font-family: var(--font-body);
  outline: none;
}

.msg-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.btn-send {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.2s ease;
}

.btn-send:hover {
  background: rgba(255, 255, 255, 0.4);
}
</style>