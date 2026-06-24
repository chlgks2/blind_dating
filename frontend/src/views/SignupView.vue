<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const username = ref('')
const nickname = ref('')
const password = ref('')
const message = ref('')

const handleSignup = async () => {
  if (!username.value || !nickname.value || !password.value) {
    message.value = '모든 칸을 입력해주세요.'
    return
  }

  try {
    await api.post('/accounts/signup/', {
      username: username.value,
      nickname: nickname.value,
      password: password.value,
    })
    message.value = '회원가입 성공!'
    setTimeout(() => router.push('/signin'), 800)
  } catch (e) {
    message.value = '아이디나 닉네임이 이미 사용 중입니다.'
  }
}
</script>

<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="login-screen">
        <div class="bg-orbs">
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="orb orb-3"></div>
        </div>

        <div class="login-body">
          <div class="title-block">
            <h1 class="signin-title">Sign up</h1>
            <p class="signin-sub">
              처음 오셨군요, 환영해요!<br/>
              <span class="link-text">이미 계정이 있으신가요?
                <router-link to="/signin" class="signup-link">로그인</router-link>
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
                v-model="nickname"
                type="text"
                placeholder="Nickname"
                autocomplete="nickname"
              />
            </div>
            <div class="glass-input-wrap">
              <input
                class="glass-input"
                v-model="password"
                type="password"
                placeholder="Password"
                autocomplete="new-password"
                @keyup.enter="handleSignup"
              />
            </div>
          </div>

          <button class="btn-continue" @click="handleSignup">
            Register
          </button>

          <p
            v-if="message"
            class="status-msg"
            :class="message.includes('성공') ? 'status-ok' : 'status-err'"
          >
            {{ message }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.login-screen {
  position: relative;
  min-height: 100vh;
}

.bg-orbs {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
}
.orb-1 {
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(255,180,210,0.65) 0%, transparent 70%);
  top: -80px; left: -60px;
  animation: drift 12s ease-in-out infinite alternate;
}
.orb-2 {
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(240,130,170,0.50) 0%, transparent 70%);
  top: 60px; right: -50px;
  animation: drift 15s ease-in-out infinite alternate-reverse;
}
.orb-3 {
  width: 180px; height: 180px;
  background: radial-gradient(circle, rgba(255,210,230,0.55) 0%, transparent 70%);
  top: 260px; left: 60px;
  animation: drift 10s ease-in-out infinite alternate;
}

@keyframes drift {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(18px, 22px) scale(1.06); }
}

.login-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 52px;
}

.title-block {
  margin-bottom: 32px;
}

.signin-title {
  font-size: 40px;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.02em;
  line-height: 1.1;
  text-transform: uppercase;
}

.signin-sub {
  margin-top: 10px;
  font-size: 14px;
  color: rgba(255,255,255,0.72);
  line-height: 1.6;
  font-weight: 300;
}

.signup-link {
  color: #fff;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.glass-input-wrap {
  border-radius: 999px;
  background: rgba(255,255,255,0.28);
  border: 1px solid rgba(255,255,255,0.50);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.glass-input-wrap:focus-within {
  border-color: rgba(255,255,255,0.80);
  box-shadow: 0 0 0 3px rgba(255,255,255,0.18);
}

.glass-input {
  width: 100%;
  padding: 13px 22px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 14.5px;
  font-weight: 400;
  color: #fff;
  letter-spacing: 0.01em;
  box-sizing: border-box;
}
.glass-input::placeholder {
  color: rgba(255,255,255,0.55);
}

.btn-continue {
  width: 80%;
  display: block;
  margin: 0 auto;
  box-sizing: border-box;
  padding: 14px;
  background: #fff;
  color: #c85080;
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: transform 0.14s, background 0.14s;
  margin-bottom: 4px;
}
.btn-continue:active { transform: scale(0.97); }
.btn-continue:hover { background: rgba(255,255,255,0.92); }

.status-msg {
  margin-top: 10px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  line-height: 1.5;
  font-weight: 500;
  word-break: break-all;
  backdrop-filter: blur(10px);
}
.status-ok {
  background: rgba(255,255,255,0.22);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.4);
}
.status-err {
  background: rgba(200,50,80,0.18);
  color: #fff;
  border: 1px solid rgba(255,120,140,0.35);
}
</style>
