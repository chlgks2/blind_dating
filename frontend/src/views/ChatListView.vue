<template>
  <div class="app-shell">
    <div class="mobile-frame">
      
      <div class="chat-list-container">
        <header class="chat-header">
            <div class="header-top-bar">
                <h1 class="page-title">Messages</h1>
                
                <div class="header-right-group">
                
                <button class="icon-btn" @click="goToHome" aria-label="홈으로 이동">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
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
            <p class="page-sub">활성화된 페르소나와의 대화 목록입니다.</p>
            </header>

        <div class="chat-list-items">
          
          <div class="chat-item-card">
            <div class="avatar-placeholder">최한</div>
            <div class="chat-info">
              <h3>나는야최한</h3>
              <p>온라인 • 최근 대화 없음</p>
            </div>
            <div class="arrow-icon">➔</div>
          </div>

          <div class="chat-item-card">
            <div class="avatar-placeholder">영우</div>
            <div class="chat-info">
              <h3>최영우</h3>
              <p>오프라인</p>
            </div>
            <div class="arrow-icon">➔</div>
          </div>

        </div>
      </div> </div>
  </div>
</template>

<script setup>
// 📄 ChatListView.vue script 내부
import { useRouter } from 'vue-router'

const router = useRouter()

// 홈 버튼 클릭 시 메인뷰로 이동
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
/* 전체 컨테이너 정렬 및 패딩 */
.chat-list-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 52px 24px 0;
  box-sizing: border-box;
}

/* 헤더 텍스트 디자인 */
.chat-header {
  margin-bottom: 30px;
}

.page-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 500;
  color: #ffffff; /* 💡 글씨를 흰색으로 선언해서 절대 안 묻히게! */
  margin: 0 0 8px 0;
  letter-spacing: 0.02em;

  line-height: 1;
}

.page-sub {
  font-size: 13px;
  color: var(--text-muted, rgba(255, 255, 255, 0.6));
  margin: 0;
}

/* 채팅 아이템 리스트 정렬 구역 */
.chat-list-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 🛡️ 레퍼런스와 톤앤매너를 맞춘 은은한 투명 글라스모피즘 카드 */
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

/* 임시 프로필 이미지 원형 */
.avatar-placeholder {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(167, 139, 250, 0.2);
  border: 1px solid rgba(167, 139, 250, 0.4);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  margin-right: 14px;
}

/* 텍스트 정보 구역 */
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

/* 우측 화살표 */
.arrow-icon {
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
}

/* 📄 ChatListView.vue style 내부 */

/* 타이틀과 오른쪽 버튼 그룹을 한 줄에 정렬 */
.header-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 타이틀은 왼쪽, 버튼은 오른쪽 */
  width: 100%;
  height: 48px;
}

/* 우상단 버튼 묶음 */
.header-right-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 메인뷰와 무드를 맞춘 글라스 동그라미 버튼 */
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

/* 기존 h1 마진 수정 */
.page-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 500;
  color: #ffffff;
  margin: 0; /* 마진 초기화 */
  letter-spacing: 0.02em;
}
</style>