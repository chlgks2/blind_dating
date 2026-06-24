<template>
  <div class="app-shell">
    <div class="mobile-frame">
      
      <div class="main-screen">
        
        <header class="main-header">
        <div class="header-top-bar">
          
          <div class="header-left-space"></div>
          
          <div class="header-right-group">
            
            <button class="icon-btn" @click="goToChatList" aria-label="채팅 목록으로 이동">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </button>
            
            <button class="icon-btn" aria-label="메뉴 열기">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="12" cy="5" r="1"></circle>
                <circle cx="12" cy="19" r="1"></circle>
              </svg>
            </button>

          </div>
        </div>
      </header>

        <main class="main-content-area">
          <div class="empty-placeholder">
            <p class="placeholder-text">Soul Match 완료!</p>
          </div>
        </main>

      </div> </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 채팅 버튼 클릭 시 라우팅 트리거
const goToChatList = () => {
  router.push('/chatlist') 
}
</script>



<style scoped>
/* ── 메인 스크린 전체 프레임 ── */
.main-screen {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* ── 우상단 정렬 헤더 ── */
.main-header {
  width: 100%;
  padding: 52px 24px 0; /* 👈 ChatListView의 상단 여백과 완전히 똑같이 매칭! */
  box-sizing: border-box;
  z-index: 10;
}

/* 내부 정렬 틀 */
.header-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 양끝으로 밀어내기 */
  width: 100%;
  height: 48px;
}

/* 아이콘 2개 나란히 묶는 그룹 */
.header-right-group {
  display: flex;
  align-items: center;
  gap: 12px; /* 아이콘 사이 간격 */
}

/* 둥근 아이콘 버튼 스타일 (기존과 동일) */
.icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.25);
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.25);
}

/* ── 중앙 비어있는 넓은 공간 ── */
.main-content-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

/* 임시 가이드용 플레이스홀더 */
.empty-placeholder {
  text-align: center;
  opacity: 0.3;
}

.placeholder-text {
  font-size: 14px;
  letter-spacing: 0.05em;
  color: #ffffff;
}
</style>