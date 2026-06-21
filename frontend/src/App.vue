<script setup>
import { ref } from "vue";
import api from "./api";

const username = ref("");
const password = ref("");
const questions = ref([]);
const message = ref("");

// 로그인
const login = async () => {
  try {
    const res = await api.post("/accounts/login/", {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
    message.value = "로그인 성공!";
  } catch (e) {
    message.value = "로그인 실패: " + JSON.stringify(e.response?.data);
  }
};

// 질문 목록 불러오기
const loadQuestions = async () => {
  const res = await api.get("/matching/questions/");
  questions.value = res.data;
};

// 매칭 결과 불러오기
const matches = ref([]);
const loadMatches = async () => {
  try {
    const res = await api.get("/matching/matches/");
    matches.value = res.data.matches;
  } catch (e) {
    message.value = JSON.stringify(e.response?.data);
  }
};
</script>

<template>
  <div style="padding: 40px">
    <h2>소개팅 앱 테스트</h2>

    <section>
      <h3>로그인</h3>
      <input v-model="username" placeholder="username" />
      <input v-model="password" type="password" placeholder="password" />
      <button @click="login">로그인</button>
      <p>{{ message }}</p>
    </section>

    <hr />

    <section>
      <h3>질문 목록</h3>
      <button @click="loadQuestions">질문 불러오기</button>
      <div v-for="q in questions" :key="q.id">
        <p>
          <b>[{{ q.category_name }}]</b> {{ q.text }}
        </p>
        <ul>
          <li v-for="c in q.choices" :key="c.id">{{ c.text }}</li>
        </ul>
      </div>
    </section>

    <hr />

    <section>
      <h3>매칭 결과</h3>
      <button @click="loadMatches">매칭 보기</button>
      <ul>
        <li v-for="m in matches" :key="m.user_id">
          {{ m.nickname }} ({{ m.birth_year }}) - 유사도 {{ m.similarity }}%
        </li>
      </ul>
    </section>
  </div>
</template>
