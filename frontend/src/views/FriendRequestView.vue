<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="fr-screen">

        <header class="fr-header">
          <button class="btn-back" @click="router.back()">
            <ChevronLeft :size="22" :stroke-width="1.5" />
          </button>
          <h1 class="page-title">받은 요청</h1>
          <div class="header-right"></div>
        </header>

        <div class="fr-list" v-if="requests.length > 0">
          <div
            v-for="req in requests"
            :key="req.request_id"
            class="fr-card"
          >
            <div class="fr-avatar">{{ req.from_nickname.slice(0, 2) }}</div>
            <div class="fr-info">
              <p class="fr-name">{{ req.from_nickname }}</p>
              <p class="fr-sub">나에게 친구요청을 보냈어요</p>
            </div>
            <div class="fr-actions">
              <button class="btn-accept" @click="respond(req.request_id, 'accept')">
                <Check :size="16" :stroke-width="2" />
              </button>
              <button class="btn-reject" @click="respond(req.request_id, 'reject')">
                <X :size="16" :stroke-width="2" />
              </button>
            </div>
          </div>
        </div>

        <div class="empty-state" v-else-if="!loading">
          <p class="empty-text">받은 친구요청이 없어요</p>
        </div>

        <div class="empty-state" v-if="loading">
          <p class="empty-text">불러오는 중...</p>
        </div>

        <div class="toast" :class="{ show: toast.show }">{{ toast.msg }}</div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Check, X } from 'lucide-vue-next'
import api from '@/api'

const router = useRouter()
const requests = ref([])
const loading = ref(true)
const toast = ref({ show: false, msg: '' })

const showToast = (msg) => {
  toast.value = { show: true, msg }
  setTimeout(() => { toast.value.show = false }, 2000)
}

const loadRequests = async () => {
  loading.value = true
  try {
    const res = await api.get('/matching/friend-request/received/')
    requests.value = res.data.requests
  } catch (e) {
    console.error('친구요청 목록 로드 실패:', e)
  } finally {
    loading.value = false
  }
}

const respond = async (requestId, action) => {
  try {
    const res = await api.post('/matching/friend-request/respond/', {
      request_id: requestId,
      action,
    })

    if (action === 'accept') {
      showToast(`매칭 성립! 채팅방이 열렸어요 🎉`)
    } else {
      showToast('요청을 거절했어요')
    }

    // 처리된 요청 목록에서 제거
    requests.value = requests.value.filter(r => r.request_id !== requestId)
  } catch (e) {
    console.error('요청 처리 실패:', e)
    showToast('처리 중 오류가 발생했어요')
  }
}

onMounted(loadRequests)
</script>

<style scoped>
.fr-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.fr-header {
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

.page-title {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.02em;
  margin: 0;
}

.header-right {
  width: 22px;
}

.fr-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 20px 40px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.fr-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.fr-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(255, 180, 210, 0.25);
  border: 1px solid rgba(255, 180, 210, 0.3);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.fr-info {
  flex: 1;
}

.fr-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  margin: 0 0 3px;
  font-family: var(--font-display);
}

.fr-sub {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.fr-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-accept,
.btn-reject {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, background 0.2s ease;
}

.btn-accept {
  background: rgba(255, 180, 210, 0.35);
  color: #fff;
}

.btn-accept:hover {
  background: rgba(255, 180, 210, 0.55);
  transform: scale(1.08);
}

.btn-reject {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}

.btn-reject:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.08);
}

.btn-accept:active,
.btn-reject:active {
  transform: scale(0.93);
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-text {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.4);
  text-align: center;
}

.toast {
  position: fixed;
  bottom: 48px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  padding: 10px 22px;
  font-size: 13px;
  font-family: var(--font-display);
  color: #fff;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
  white-space: nowrap;
  z-index: 100;
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}
</style>
