<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="profile-screen">

        <header class="profile-header">
          <button class="btn-back" @click="router.back()">
            <ChevronLeft :size="22" :stroke-width="1.5" />
          </button>
          <h1 class="page-title">My Profile</h1>
          <div class="header-right"></div>
        </header>

        <div v-if="user" class="profile-body">

          <!-- 아바타 카드 -->
          <div class="avatar-wrap">
            <div class="avatar-card">
              <img :src="avatarUrl" alt="AI Avatar" class="avatar-img" />
            </div>
            <h2 class="nickname">{{ user.nickname }}</h2>
            <p class="username-tag">@{{ user.username }}</p>
          </div>

          <!-- 정보 카드 -->
          <div class="info-card">
            <div class="info-row">
              <span class="info-label">나이</span>
              <span class="info-value">{{ user.birth_year ? `${new Date().getFullYear() - user.birth_year}세 (${user.birth_year}년생)` : '미입력' }}</span>
            </div>
            <div class="divider"></div>
            <div class="info-row">
              <span class="info-label">성별</span>
              <span class="info-value">{{ user.gender === 'M' ? '남성' : user.gender === 'F' ? '여성' : '미입력' }}</span>
            </div>
            <div class="divider"></div>
            <div class="info-row">
              <span class="info-label">매칭 스타일</span>
              <span class="info-value">{{ prefLabel }}</span>
            </div>
            <div class="divider"></div>
            <div class="info-row">
              <span class="info-label">설문</span>
              <span class="info-value" :class="user.is_survey_done ? 'badge-done' : 'badge-pending'">
                {{ user.is_survey_done ? '완료' : '미완료' }}
              </span>
            </div>
          </div>

          <!-- 로그아웃 -->
          <button class="btn-logout" @click="logout">로그아웃</button>

        </div>

        <div v-else class="loading-wrap">
          <p class="loading-text">불러오는 중...</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft } from 'lucide-vue-next'
import api from '@/api'
import defaultAvatar from '@/assets/result.png'

const router = useRouter()
const user = ref(null)
const avatarUrl = ref(localStorage.getItem('ai_generated_url') || defaultAvatar)

const prefLabel = computed(() => {
  const map = { similar: '비슷한 사람', complement: '다른 사람', neutral: '반반' }
  return map[user.value?.match_preference] || '미설정'
})

onMounted(async () => {
  try {
    const res = await api.get('/accounts/me/')
    user.value = res.data
    // 백엔드에서 받은 AI 이미지를 우선 사용 (localStorage보다 신뢰도 높음)
    if (res.data.ai_image_url) {
      avatarUrl.value = res.data.ai_image_url
      localStorage.setItem('ai_generated_url', res.data.ai_image_url)
    }
  } catch (e) {
    console.error('프로필 로드 실패:', e)
  }
})

const logout = () => {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  localStorage.removeItem('ai_job_id')
  localStorage.removeItem('ai_generated_url')
  router.push('/signin')
}
</script>

<style scoped>
.profile-screen {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.profile-header {
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

.header-right { width: 22px; }

/* ── 아바타 영역 ── */
.profile-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 24px 48px;
  gap: 24px;
}

.avatar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-card {
  width: 140px;
  aspect-ratio: 3 / 4;
  border-radius: 22px;
  overflow: hidden;
  border: 1.5px solid rgba(255, 255, 255, 0.35);
  box-shadow:
    0 0 24px rgba(255, 255, 255, 0.25),
    0 0 60px rgba(255, 180, 210, 0.15);
  animation: float 4s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-6px); }
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.nickname {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.02em;
  margin: 0;
}

.username-tag {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  letter-spacing: 0.02em;
}

/* ── 정보 카드 ── */
.info-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  overflow: hidden;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
}

.info-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.45);
  font-family: var(--font-body);
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  font-family: var(--font-body);
}

.badge-done {
  color: rgba(180, 255, 200, 0.9);
}

.badge-pending {
  color: rgba(255, 200, 150, 0.9);
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.07);
  margin: 0 20px;
}

/* ── 로그아웃 ── */
.btn-logout {
  width: 100%;
  padding: 14px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--r-pill);
  color: rgba(255, 255, 255, 0.5);
  font-family: var(--font-display);
  font-size: 14px;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

/* ── 로딩 ── */
.loading-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-text {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.4);
}
</style>
