<script setup>
import { ref, onUnmounted } from "vue";
import api from "./api";

const username = ref("");
const password = ref("");
const message = ref("");
const isLoggedIn = ref(false);

// === 로그인 ===
const login = async () => {
  try {
    const res = await api.post("/accounts/login/", {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem("access", res.data.access);
    isLoggedIn.value = true;
    message.value = "로그인 성공!";
  } catch (e) {
    message.value = "로그인 실패: " + JSON.stringify(e.response?.data);
  }
};

// === 추천 이성 목록 ===
const recommends = ref([]);
const loadRecommends = async () => {
  const res = await api.get("/matching/matches/recommend/");
  recommends.value = res.data.matches;
};

// === 친구요청 보내기 ===
const sendRequest = async (toUserId) => {
  const res = await api.post("/matching/friend-request/send/", {
    to_user: toUserId,
  });
  alert(res.data.message);
};

// === 받은 요청 목록 ===
const receivedReqs = ref([]);
const loadReceived = async () => {
  const res = await api.get("/matching/friend-request/received/");
  receivedReqs.value = res.data.requests;
};

// === 요청 수락/거절 ===
const respond = async (requestId, action) => {
  const res = await api.post("/matching/friend-request/respond/", {
    request_id: requestId,
    action,
  });
  alert(res.data.message);
  loadReceived();
};

// === 내 매칭(채팅방) 목록 ===
const myMatches = ref([]);
const loadMyMatches = async () => {
  const res = await api.get("/matching/my-matches/");
  myMatches.value = res.data.matches;
};

// === 채팅 (WebSocket 버전) ===
const currentMatchId = ref(null);
const messages = ref([]);
const newMessage = ref("");
let socket = null;

const openChat = async (matchId) => {
  currentMatchId.value = matchId;
  messages.value = [];

  // 1) 기존 메시지 히스토리는 HTTP로 먼저 로드
  const res = await api.get(`/matching/matches/${matchId}/messages/`);
  messages.value = res.data.messages;

  // 2) WebSocket 연결 (토큰을 쿼리스트링으로)
  const token = localStorage.getItem("access");
  socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/chat/${matchId}/?token=${token}`,
  );

  socket.onopen = () => console.log("WebSocket 연결됨");

  socket.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    messages.value.push(msg); // 새 메시지 실시간 추가
  };

  socket.onclose = () => console.log("WebSocket 종료");
  socket.onerror = (e) => console.error("WebSocket 에러", e);
};

const sendMessage = () => {
  if (!newMessage.value.trim() || !socket) return;
  socket.send(JSON.stringify({ content: newMessage.value }));
  newMessage.value = "";
  // 주의: 내가 보낸 것도 서버가 브로드캐스트해서 onmessage로 돌아옴
  //       → messages에 자동 추가되므로 여기서 push 안 함
};

const closeChat = () => {
  currentMatchId.value = null;
  if (socket) {
    socket.close();
    socket = null;
  }
};

onUnmounted(() => {
  if (socket) socket.close();
});
</script>

<template>
  <div style="padding: 30px; max-width: 700px; font-family: sans-serif">
    <h2>💕 소개팅 앱 테스트</h2>

    <!-- 로그인 -->
    <section style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px">
      <h3>1. 로그인</h3>
      <input v-model="username" placeholder="username" />
      <input v-model="password" type="password" placeholder="password" />
      <button @click="login">로그인</button>
      <p>{{ message }}</p>
    </section>

    <template v-if="isLoggedIn">
      <!-- 추천 + 친구요청 -->
      <section
        style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px"
      >
        <h3>2. 추천 이성</h3>
        <button @click="loadRecommends">추천 불러오기</button>
        <ul>
          <li v-for="r in recommends" :key="r.user_id">
            {{ r.nickname }} ({{ r.birth_year }}) - 유사도 {{ r.similarity }}%
            <button @click="sendRequest(r.user_id)">친구요청</button>
          </li>
        </ul>
      </section>

      <!-- 받은 요청 -->
      <section
        style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px"
      >
        <h3>3. 받은 친구요청</h3>
        <button @click="loadReceived">받은 요청 불러오기</button>
        <ul>
          <li v-for="req in receivedReqs" :key="req.request_id">
            {{ req.from_nickname }}님의 요청
            <button @click="respond(req.request_id, 'accept')">수락</button>
            <button @click="respond(req.request_id, 'reject')">거절</button>
          </li>
        </ul>
      </section>

      <!-- 내 채팅방 -->
      <section
        style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px"
      >
        <h3>4. 내 매칭 / 채팅방</h3>
        <button @click="loadMyMatches">채팅방 목록</button>
        <ul>
          <li v-for="m in myMatches" :key="m.match_id">
            {{ m.other_nickname }}
            <small>({{ m.last_message || "대화 없음" }})</small>
            <button @click="openChat(m.match_id)">채팅 열기</button>
          </li>
        </ul>
      </section>

      <!-- 채팅창 -->
      <section
        v-if="currentMatchId"
        style="border: 2px solid #f08; padding: 15px"
      >
        <h3>
          💬 채팅 (Match #{{ currentMatchId }})
          <button @click="closeChat" style="float: right">닫기</button>
        </h3>
        <div
          style="
            height: 250px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 10px;
          "
        >
          <div v-for="msg in messages" :key="msg.id" style="margin-bottom: 6px">
            <b>{{ msg.sender_nickname }}:</b> {{ msg.content }}
            <small style="color: #999">{{
              msg.created_at.slice(11, 16)
            }}</small>
          </div>
        </div>
        <div style="margin-top: 10px">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="메시지 입력..."
            style="width: 70%"
          />
          <button @click="sendMessage">전송</button>
        </div>
      </section>
    </template>
  </div>
</template>
