<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="chat-list-container">

        <header class="chat-header">
          <h1 class="page-title">Messages</h1>
        </header>

        <div class="chat-list-items" v-if="matches.length > 0">
          <div
            v-for="m in matches"
            :key="m.match_id"
            class="chat-item-card"
            @click="m.is_chat_open
              ? router.push({ path: '/chat', query: { matchId: m.match_id, userName: m.other_nickname } })
              : router.push({ path: '/payment', query: { matchId: m.match_id, userName: m.other_nickname, userId: m.other_user_id } })"
          >
            <div class="avatar-placeholder">{{ m.other_nickname.slice(0, 2) }}</div>
            <div class="chat-info">
              <h3>{{ m.other_nickname }}</h3>
              <p>{{ m.is_chat_open ? (m.last_message || '대화를 시작해보세요') : '결제 후 채팅 가능' }}</p>
            </div>
            <div class="arrow-icon">➔</div>
          </div>
        </div>

        <div class="empty-state" v-else-if="!loading">
          <p class="empty-text">아직 매칭된 상대가 없어요</p>
          <p class="empty-sub">매칭 화면에서 친구요청을 보내보세요</p>
          <button class="btn-go-match" @click="router.push('/matching')">매칭하러 가기</button>
        </div>

        <nav class="bottom-nav">
          <button class="nav-btn" @click="router.push('/matching')">
            <Sparkles :size="22" :stroke-width="1.5" />
          </button>
          <button class="nav-btn" @click="router.push('/friend-requests')">
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, MessageCircle, User, Sparkles } from 'lucide-vue-next'
import api from '@/api'

const router = useRouter()
const matches = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/matching/my-matches/')
    matches.value = res.data.matches
  } catch (e) {
    console.error('채팅방 목록 로드 실패:', e)
  } finally {
    loading.value = false
  }
})
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

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-bottom: 120px;
  gap: 8px;
}

.empty-text {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.empty-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0 0 16px;
}

.btn-go-match {
  padding: 11px 28px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  color: #fff;
  font-family: var(--font-display);
  font-size: 13px;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-go-match:hover {
  background: rgba(255, 255, 255, 0.22);
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