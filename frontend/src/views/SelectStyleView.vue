<template>
  <div class="app-shell">
    <div class="mobile-frame">

      <div class="view-body" :class="animationClass">
        
        <div v-if="currentStep === 1" class="step-wrapper">
          <div class="title-block">
            <h1 class="signin-title">Upload Photo</h1>
            <p class="signin-sub">아바타 생성을 위해 본인 사진을 골라주세요</p>
          </div>

          <div class="upload-container">
            <label class="glass-upload-box" :class="{ 'has-preview': imagePreview }">
              <input type="file" accept="image/*" class="file-hidden" @change="handleFileUpload" />
              
              <div v-if="!imagePreview" class="upload-placeholder">
                <span class="upload-hint">얼굴이 잘 나온 사진이 좋아요</span>
              </div>

              <div v-else class="preview-wrapper">
                <img :src="imagePreview" class="preview-img" alt="Uploaded preview" />
                <div class="preview-overlay">사진 바꾸기</div>
              </div>
            </label>
          </div>

          <div class="action-block" :class="{ 'show-btn': imagePreview }">
            <button 
              class="btn-continue" 
              @click="triggerNextStep(2)"
            >
              Next
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 2" class="step-wrapper">
          <div class="title-block">
            <h1 class="signin-title">Select Style</h1>
            <p class="signin-sub">가장 마음에 드는 스타일은 무엇인가요?</p>
          </div>

          <div class="grid-container">
            <div 
              v-for="style in styleOptions" 
              :key="style.id"
              class="style-card"
              :class="{ active: selectedStyleId === style.id }"
              @click="selectStyle(style.id)"
            >
              <div class="card-image-wrapper">
                <img :src="style.imgUrl" :alt="style.name" class="style-img" />
              </div>
              <div class="card-info">
                <span class="style-name">{{ style.name }}</span>
              </div>
            </div>
          </div>

          <div class="action-block" :class="{ 'show-btn': selectedStyleId !== null }">

            <button 
              class="btn-continue" 
              :disabled="selectedStyleId === null"
              @click="triggerNextStep('questions')"
            >
              Next
            </button>

          </div>
        </div>

      </div>

    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const currentStep = ref(1)
const rawFile = ref(null)
const imagePreview = ref(null)
const selectedStyleId = ref(null)

// ✨ 화면 전활 시 슥- 사라지는 연출을 위한 상태 클래스 관리 변수
const animationClass = ref('fade-in')

const styleOptions = ref([
  { id: 1, name: 'Ghibli', imgUrl: new URL('../assets/style1.png', import.meta.url).href },
  { id: 2, name: 'Pixar', imgUrl: new URL('../assets/style2.png', import.meta.url).href },
  { id: 3, name: 'Cyberpunk', imgUrl: new URL('../assets/style3.png', import.meta.url).href },
  { id: 4, name: 'Dreamy', imgUrl: new URL('../assets/style4.png', import.meta.url).href },
])

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  rawFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

const selectStyle = (id) => {
  selectedStyleId.value = id
}

// 🎬 [Next] 버튼 누르면 스르륵 사라졌다가 부드럽게 나타나게 만드는 제어 함수
const triggerNextStep = (nextTarget) => {
  // 1. 먼저 화면 알맹이를 흐릿하게 밀어버리는 아웃 애니메이션 클래스를 켭니다.
  animationClass.value = 'fade-out'

  // 2. 애니메이션이 끝나는 약 0.4초(400ms) 뒤에 다음 타겟으로 전환!
  setTimeout(() => {
    if (nextTarget === 'questions') {
      router.push('/loading')
    } else {
      currentStep.value = nextTarget
      // 3. 전환된 뒤에는 다시 부드럽게 스르륵 떠오르도록 페이드인 클래스로 초기화
      animationClass.value = 'fade-in'
    }
  }, 400)
}

</script>



<style scoped>
/* ✨ 마이크로 인터랙션용 페이드 인/아웃 스타일 (0.4초 효과) */
.view-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 80px;

  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
  box-sizing: border-box;
  transition: opacity 0.4s ease, transform 0.4s ease; /* 🚀 쫀득한 핵심 트랜지션 */
}

/* 다음 스텝으로 넘어갈 때 왼쪽으로 투명하게 스르륵 밀림 */
.view-body.fade-out {
  opacity: 0;
  transform: translateX(-16px);
}

/* 새로운 스텝이 등장할 때 아래에서 위로 살포시 피어오름 */
.view-body.fade-in {
  opacity: 1;
  transform: translateX(0) translateY(0);
  animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-wrapper { display: flex; flex-direction: column; height: 100%; flex: 1; }

.title-block {
  margin-bottom: 40px;
  text-align: center;
}

.signin-title {
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 400;
  color: var(--white);
  letter-spacing: 0.02em;
  line-height: 1.1;
  text-transform: uppercase;
}

.signin-sub {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-sub);
  line-height: 1.6;
  font-weight: 300;
}

/* 📁 STEP 1: 업로드 디자인 */
.upload-container { flex: 1; display: flex; align-items: center; justify-content: center; max-height: 380px; }

.glass-upload-box {
  width: 240px;
  aspect-ratio: 3 / 4;
  
  border-radius: var(--r-md); /* 💡 디자인 토큰 사용 */
  background: rgba(255, 255, 255, 0.25);

  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);

  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.25), 
              0 8px 32px rgba(252, 138, 180, 0.08); 

  display: flex; align-items: center; justify-content: center; cursor: pointer; overflow: hidden; position: relative; transition: all 0.25s ease;
}
.glass-upload-box:hover { 
    background: rgba(255, 255, 255, 0.2); 
    border-color: rgba(255, 255, 255, 0.7); 
}
.glass-upload-box.has-preview { border-style: solid; border-color: rgba(255,255,255,0.5); }
.file-hidden { display: none; }

.upload-placeholder { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 20px; }

.upload-icon { font-size: 40px; margin-bottom: 12px; }

/* 💡 [폰트 중복 삭제] font-family 제거 완료 */
.upload-hint { font-size: 12px; color: rgba(255,255,255,0.5); }

.preview-wrapper { width: 100%; height: 100%; position: relative; }
.preview-img { width: 100%; height: 100%; object-fit: cover; }

/* 💡 [폰트 중복 삭제] font-family 제거 완료 */
.preview-overlay { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.4); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 500; opacity: 0; transition: opacity 0.2s ease; }
.preview-wrapper:hover .preview-overlay { opacity: 1; }


/* 📊 STEP 2: 2*2 세로형 카드 레이아웃 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 14px; 
  width: 100%;
  margin-bottom: auto;
}
.style-card {
  position: relative; 
  border-radius: var(--r-md);
  overflow: hidden; 


  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  width: 100%;
  aspect-ratio: 4 / 4.5;
}

.style-card.active {
  border: 0.2px solid #ffffff;
  transform: scale(1.03);
  box-shadow: 
    0 0 30px rgba(255, 255, 255, 0.8), 
    0 0 50px rgba(255, 255, 255, 0.2);
}

.card-image-wrapper { width: 100%; height: 100%; }
.style-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.style-card:hover .style-img { transform: scale(1.06); }

.card-info {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 20px 12px 14px 12px; 
  background: linear-gradient(to top, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 100%);
  text-align: center;
  box-sizing: border-box;
}

/* 💡 [폰트 중복 삭제] font-family 제거 완료 */
.style-name {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 500; 
  color: #ffffff;   
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.4); 
}


/* 🚀 하단 공통 버튼 */
.action-block { 
  padding: 16px 0 32px 0; 
  overflow: visible !important;

  opacity: 0;
  transform: translateY(20px); /* 아래에 살짝 내려놓기 */
  pointer-events: none; 
  
  transition: all 1.8s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 🔥 [핵심] 사진이 업로드되면(show-btn 클래스가 붙으면) 스르륵 피어오름! */
.action-block.show-btn {
  opacity: 1;
  transform: translateY(0) scale(1); /* 제자리로 슬라이드 업 */
  pointer-events: auto;
}

.btn-continue { 
    width: 240px; 
    margin: 0 auto;
    display: block;
    padding: 14px; 
    
    background: linear-gradient(135px, #ffffff 0%, rgba(255, 255, 255, 0.9) 50%, #ffffff 100%);
    background-size: 200% 200%;
    color: var(--app-canvas-bg);
    
    font-size: 14.5px; 
    font-weight: 600; 
    letter-spacing: 0.08em; 
    text-transform: uppercase; 
    border: none; 
    border-radius: var(--r-pill); /* 💡 999px 대신 토큰 사용 */
    cursor: pointer; 
    box-sizing: border-box; 
    font-family: var(--font-display); 
    position: relative;
    z-index: 1;
    
    animation: glow-aurora 4s ease infinite;
    box-shadow: 
      0 0 20px rgba(255, 255, 255, 0.4),  /* 내부 광채 */
      0 0 40px rgba(255, 255, 255, 0.2),  /* 중간 광채 */
      0 0 80px rgba(255, 255, 255, 0.1);  /* 외부 확산 광채 */
    
    transition: all 0.3s ease;
}

/* 🔥 [핵심] 버튼이 활성화(:not(:disabled))되었을 때만 일렁임과 오라 발동! */
.btn-continue:not(:disabled) {
    animation: glow-aurora 4s ease infinite;
    box-shadow: 
      0 0 30px rgba(255, 255, 255, 0.5), 
      0 0 60px rgba(255, 255, 255, 0.3),
      0 0 100px rgba(255, 255, 255, 0.1);
}

/* 호버했을 때 살짝 떠오르는 텐션 */
.btn-continue:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 
      0 0 40px rgba(255, 255, 255, 0.6), 
      0 0 80px rgba(255, 255, 255, 0.4);
}

/* ❌ 비활성화 상태일 때는 일렁임도 끄고 투명하게 */
.btn-continue:disabled { 
    background: rgba(255, 255, 255, 0.3); 
    color: rgba(255, 255, 255, 0.6); 
    cursor: not-allowed; 
    box-shadow: none;
    animation: none;
}


/* 💡 활성화된 버튼의 뒤쪽에 가짜 복사본을 만들어 흐릿하게(blur) 만들고 숨쉬듯 키워줍니다 */
.btn-continue:not(:disabled)::before {
    content: '';
    position: absolute;
    inset: -2px; /* 버튼보다 살짝 크게 */
    border-radius: var(--r-pill);
    background: linear-gradient(90deg, rgba(255,255,255,0.8), rgba(255, 186, 212, 0.609), rgba(255, 255, 255, 0.8));
    background-size: 200%;
    z-index: -1; /* 버튼 글씨 뒤로 숨기 */
    filter: blur(10px);
    opacity: 0.7;
    animation: glow-aurora 3s linear infinite, pulse-glow 2s ease-in-out infinite alternate;
}

@keyframes pulse-glow {
    from { transform: scale(0.98); opacity: 0.5; }
    to { transform: scale(1.03); opacity: 0.9; }
}

</style>
