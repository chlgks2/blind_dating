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
.login-body {
  position: relative;
  z-index: 1;
  padding: 0 24px;
  margin-top: 80px;
}

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

.status-msg {
  margin-top: 14px;
  font-size: 10px;
  line-height: 1.5;
  font-weight: 500;
  text-align: center;
}

.status-ok { color: #ffffff; }
.status-err { color: #ffffff; font-size: 10px; font-weight: 200; }
</style>