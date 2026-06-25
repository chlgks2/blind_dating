<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="chat-list-container">

        <header class="chat-header">
          <h1 class="page-title">Messages</h1>
        </header>

        <div class="chat-list-items">
          <div class="chat-item-card" @click="router.push({ path: '/chat', query: { userName: '나는야최한' } })">
            <div class="avatar-placeholder">최한</div>
            <div class="chat-info">
              <h3>나는야최한</h3>
              <p>온라인 • 최근 대화 없음</p>
            </div>
            <div class="arrow-icon">➔</div>
          </div>

          <div class="chat-item-card" @click="router.push({ path: '/chat', query: { userName: '최영우' } })">
            <div class="avatar-placeholder">영우</div>
            <div class="chat-info">
              <h3>최영우</h3>
              <p>오프라인</p>
            </div>
            <div class="arrow-icon">➔</div>
          </div>
        </div>

        <nav class="bottom-nav">
          <button class="nav-btn" @click="router.push('/')">
            <Heart :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn active" @click="router.push('/chatlist')">
            <MessageCircle :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" @click="router.push('/profile')">
            <User :size="22" :stroke-width="1.5" />
          </button>
        </nav>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Heart, MessageCircle, User } from 'lucide-vue-next'

const router = useRouter()
</script>

<style scoped>
.chat-list-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 52px 24px 0;
  box-sizing: border-box;
}

.chat-header {
  margin-bottom: 30px;
}

.page-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 8px 0;
  letter-spacing: 0.02em;
  line-height: 1;
}

.chat-list-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-item-card {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.chat-item-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.avatar-placeholder {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 231, 189, 0.2);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  margin-right: 14px;
}

.chat-info {
  flex: 1;
}

.chat-info h3 {
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 4px 0;
}

.chat-info p {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.arrow-icon {
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
}

.bottom-nav {
  position: fixed;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  padding: 6px 10px;
  z-index: 50;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  width: 52px;
  height: 40px;
  border-radius: 999px;
  transition: background 0.25s ease, color 0.25s ease;
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  width: 64px;
}

.nav-btn:hover {
  color: #fff;
}
</style>