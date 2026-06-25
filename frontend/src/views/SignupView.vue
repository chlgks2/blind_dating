<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../api"

const router = useRouter()
const username = ref("")
const password = ref("")
const nickname = ref("")
const gender = ref("")
const birthYear = ref("")
const matchPref = ref("neutral")
const message = ref("")

const handleSignup = async () => {
  if (!username.value || !password.value || !nickname.value || !gender.value) {
    message.value = "Username, Password, Nickname, 성별은 필수입니다."
    return
  }

  const payload = {
    username: username.value,
    password: password.value,
    nickname: nickname.value,
    gender: gender.value,
    match_preference: matchPref.value,
  }

  if (birthYear.value) {
    const yr = Number(birthYear.value)
    if (yr < 1940 || yr > new Date().getFullYear() - 18) {
      message.value = "올바른 출생연도를 입력해주세요."
      return
    }
    payload.birth_year = yr
  }

  try {
    await api.post("/accounts/signup/", payload)
    message.value = "회원가입 성공!"
    setTimeout(() => router.push("/signin"), 800)
  } catch (e) {
    message.value = "아이디나 닉네임이 이미 사용 중입니다."
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
              <input class="glass-input" v-model="username" type="text"
                placeholder="ID" autocomplete="username" />
            </div>

            <div class="glass-input-wrap">
              <input class="glass-input" v-model="password" type="password"
                placeholder="Password" autocomplete="new-password" />
            </div>

            <div class="glass-input-wrap">
              <input class="glass-input" v-model="nickname" type="text"
                placeholder="Nickname" autocomplete="nickname" />
            </div>

            <div class="field-block">
              <p class="field-label">성별 <span class="required">*</span></p>
              <div class="toggle-group">
                <button type="button" class="toggle-btn"
                  :class="{ active: gender === 'M' }" @click="gender = 'M'">남성</button>
                <button type="button" class="toggle-btn"
                  :class="{ active: gender === 'F' }" @click="gender = 'F'">여성</button>
              </div>
            </div>

            <div class="glass-input-wrap">
              <input class="glass-input" v-model="birthYear" type="number"
                placeholder="출생연도 (예: 1998) — 선택" min="1940"
                :max="new Date().getFullYear() - 18" @keyup.enter="handleSignup" />
            </div>

            <div class="field-block">
              <p class="field-label">매칭 스타일</p>
              <div class="toggle-group three">
                <button type="button" class="toggle-btn"
                  :class="{ active: matchPref === 'similar' }" @click="matchPref = 'similar'">비슷한 사람</button>
                <button type="button" class="toggle-btn"
                  :class="{ active: matchPref === 'neutral' }" @click="matchPref = 'neutral'">반반</button>
                <button type="button" class="toggle-btn"
                  :class="{ active: matchPref === 'complement' }" @click="matchPref = 'complement'">다른 사람</button>
              </div>
            </div>

          </div>

          <button class="btn-continue" @click="handleSignup">Register</button>

          <p v-if="message" class="status-msg"
            :class="message.includes('성공') ? 'status-ok' : 'status-err'">
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
  padding: 0 24px 40px;
  margin-top: 64px;
}

.title-block {
  margin-bottom: 32px;
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
  margin-bottom: 16px;
  width: 100%;
}

.glass-input-wrap {
  width: 80%;
  margin: 0 auto;
  box-sizing: border-box;
  border-radius: var(--r-pill);
  box-shadow: inset 0 1px 2px rgba(255,255,255,0.25), 0 8px 32px rgba(252,138,197,0.08);
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
  color: rgba(255,255,255,0.45);
  font-size: 13.5px;
}

.glass-input[type="number"]::-webkit-inner-spin-button,
.glass-input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
}

.field-block {
  width: 80%;
  margin: 4px auto 0;
}

.field-label {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin: 0 0 7px 4px;
  font-family: var(--font-display);
}

.required {
  color: rgba(255,180,210,0.7);
}

.toggle-group {
  display: flex;
  gap: 8px;
}

.toggle-group.three .toggle-btn {
  font-size: 12px;
  padding: 10px 0;
}

.toggle-btn {
  flex: 1;
  padding: 11px 0;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--r-pill);
  color: rgba(255,255,255,0.5);
  font-family: var(--font-display);
  font-size: 13px;
  letter-spacing: 0.03em;
  cursor: pointer;
  transition: background 0.18s, border-color 0.18s, color 0.18s;
}

.toggle-btn.active {
  background: rgba(255,255,255,0.22);
  border-color: rgba(255,255,255,0.45);
  color: #fff;
}

.toggle-btn:hover:not(.active) {
  background: rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.75);
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
  transition: transform 0.14s, box-shadow 0.14s;
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
