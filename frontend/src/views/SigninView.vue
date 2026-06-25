<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const username = ref('')
const password = ref('')
const message = ref('')

const login = async () => {
  if (!username.value || !password.value) {
    message.value = '이메일과 비밀번호를 모두 입력해주세요.'
    return
  }

  try {
    const res = await api.post('/accounts/login/', {
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('access', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)
    message.value = '로그인 성공!'
    setTimeout(() => router.push('/loading?type=signin'), 800)
  } catch (e) {
    message.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
  }
}
</script>

<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="login-screen">
        <div class="login-body">
          <div class="title-block">
            <h1 class="signin-title">Sign in</h1>
            <p class="signin-sub">
              반가워요! 다시 만났네요.<br/>
              <span class="link-text">처음이신가요? 
                <router-link to="/signup" class="signup-link">회원가입</router-link>
              </span>
            </p>
          </div>

          <div class="form-group">
            <div class="glass-input-wrap">
              <input
                class="glass-input"
                v-model="username"
                type="text"
                placeholder="Username"
                autocomplete="username"
              />
            </div>
            <div class="glass-input-wrap">
              <input
                class="glass-input"
                v-model="password"
                type="password"
                placeholder="Password"
                autocomplete="current-password"
                @keyup.enter="login"
              />
            </div>
          </div>

          <button class="btn-continue" @click="login">
            Continue
          </button>

          <p
            v-if="message"
            class="status-msg"
            :class="message.includes('성공') ? 'status-ok' : 'status-err'"
          >
            {{ message }}
          </p>

          <div class="or-row">
            <span class="or-line"></span>
            <span class="or-text">or</span>
            <span class="or-line"></span>
          </div>

          <div class="social-group">
            <button class="btn-social">
              <svg class="social-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="white"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="white"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="white"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="white"/>
              </svg>
            </button>

            <button class="btn-social btn-kakao">
              <svg class="social-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 3.6C6.923 3.6 2.8 6.92 2.8 11c0 2.56 1.56 4.817 3.926 6.197l-.99 3.676 4.3-2.835c.642.09 1.3.138 1.964.138 5.077 0 9.2-3.32 9.2-7.4S17.077 3.6 12 3.6z" fill="white"/>
              </svg>
            </button>
          </div>

          <button class="forgot-btn">Forgot password?</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>



.logo-mark {
  font-size: 20px;
  color: var(--white);
  line-height: 1;
}

.logo-name {
  font-family: var(--font-display);
  font-size: 20px;
  letter-spacing: 0.18em;
  color: var(--white);
  text-transform: uppercase;
}

/* ══════════════════════
   로그인 본문
══════════════════════ */
.login-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 80px;
}

/* 타이틀 */
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

.signup-link {
  color: var(--white);
  text-decoration: underline 0.3px;
  text-underline-offset: 2px;
}

/* ── 인풋 ── */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 10px;
  width: 100%;
}

.glass-input-wrap {
  width: 80%;
  margin: 0 auto;
  box-sizing: border-box;
  border-radius: var(--r-pill);
  transition: border-color 0.2s, box-shadow 0.2s;

  box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.25), 
              0 8px 32px rgba(252, 138, 197, 0.08);
}


.glass-input {
  width: 100%;
  padding: 13px 22px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 14.5px;
  font-family: var(--font-body);
  font-weight: 500;
  color: var(--white);
  letter-spacing: 0.01em;

  caret-color: var(--white);
  animation: slowCaret 1.6s infinite;
}

.glass-input::placeholder {
  color: rgba(255,255,255,0.55);
}

/* ── Continue 버튼 ── */
.btn-continue {
  width: 80%;
  display: block;
  margin: 0 auto;
  box-sizing: border-box;
  padding: 14px;
  background: var(--white);
  color: var(--app-canvas-bg);

  font-size: 14.5px;
  font-weight: 600;
  font-family: var(--font-display);
  
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: none;
  border-radius: var(--r-pill);
  cursor: pointer;
  transition: transform 0.14s, box-shadow 0.14s, background 0.14s;
  margin-bottom: 0px;
}
.btn-continue:active {
  transform: scale(0.97);
  box-shadow: 0 2px 8px rgba(200,80,120,0.15);
}


/* ── 상태 메시지 ── */
.status-msg {
  margin-top: 14px;
  font-size: 10px;
  line-height: 1.5;
  font-weight: 500;
  text-align: center;
}

.status-ok {
  color: #ffffff;
}
.status-err {
  color: #ffffff;
  font-size: 10px;
  font-weight: 200;
}

/* ── or 구분선 ── */
.or-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 18px auto;
  width: 80%;
}
.or-line {
  flex: 1;
  height: 1px;
  background:  var(--text-muted);
}
.or-text {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-sub);
  letter-spacing: 0.04em;
}

/* ── 소셜 버튼 ── */
.social-group {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 16px;
}

.btn-social {
  width: 52px;
  height: 52px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 50%;
  cursor: pointer;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition: background 0.18s, border-color 0.18s, transform 0.12s;
}
.btn-social:active {
  transform: scale(0.94);
}
.btn-social:hover {
  background: rgba(255,255,255,0.22);
  border-color: rgba(255,255,255,0.45);
}

.btn-kakao {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.25);
}

.social-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

/* ── Forgot ── */
.forgot-btn {
  display: block;
  width: 100%;
  margin-top: 22px;
  background: none;
  border: none;
  color: var(--text-sub);
  font-size: 13px;
  font-family: inherit;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  letter-spacing: 0.01em;
  padding-bottom: 36px;
}
.forgot-btn:hover { color: var(--white-60); }

</style>