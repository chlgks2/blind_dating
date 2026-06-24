<script setup>
import { ref, onUnmounted } from "vue";
import api from "./api";

const username = ref("");
const password = ref("");
const message = ref("");
const isLoggedIn = ref(false);

// === 설문 ===
const questions = ref([]);
const currentIdx = ref(0);
const myAnswers = ref([]);

const loadSurvey = async () => {
  const res = await api.get("/matching/questions/");
  questions.value = res.data;
  currentIdx.value = 0;
  myAnswers.value = [];
};

// A=왼쪽 스와이프, B=오른쪽 스와이프
const choose = (selected) => {
  const q = questions.value[currentIdx.value];
  myAnswers.value.push({ question: q.id, selected });
  currentIdx.value++;

  // 다 풀면 제출
  if (currentIdx.value >= questions.value.length) {
    submitSurvey();
  }
};

const submitSurvey = async () => {
  await api.post("/matching/answers/", { answers: myAnswers.value });
  alert("설문 완료! 이제 매칭을 볼 수 있어요 🎉");
};

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

// === 결제 ===
const payForMatch = async (matchId) => {
  const IMP = window.IMP;
  IMP.init("imp07810156"); // 가맹점 식별코드

  IMP.request_pay(
    {
      pg: "kakaopay.TC0ONETIME", // 카카오페이 테스트
      pay_method: "card",
      merchant_uid: `order_${matchId}_${Date.now()}`,
      name: "소개팅 채팅 오픈",
      amount: 100, // 테스트용 100원
    },
    async (rsp) => {
      console.log("포트원 결제 응답:", rsp); // ① 포트원 응답 확인
      if (rsp.success) {
        try {
          const res = await api.post("/matching/payment/verify/", {
            match_id: matchId,
            imp_uid: rsp.imp_uid,
          });
          console.log("백엔드 검증 응답:", res.data);
          if (res.data.is_chat_open) {
            alert("양쪽 결제 완료! 채팅이 열렸습니다 🎉");
          } else {
            alert("결제 완료! 상대방 결제를 기다리는 중입니다.");
          }
          loadMyMatches();
        } catch (e) {
          // ② 백엔드 400 에러 내용을 그대로 출력!
          console.error("검증 실패:", e.response?.data);
          alert("검증 실패: " + JSON.stringify(e.response?.data));
        }
      } else {
        alert("결제 실패: " + rsp.error_msg);
      }
    },
  );
};
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
    <div style="padding: 30px; max-width: 400px">
      <h3>취향 스와이프</h3>
      <button @click="loadSurvey">설문 시작</button>

      <div
        v-if="questions.length && currentIdx < questions.length"
        style="margin-top: 20px; text-align: center"
      >
        <p>{{ currentIdx + 1 }} / {{ questions.length }}</p>
        <div
          style="
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 30px;
          "
        >
          <button
            @click="choose('A')"
            style="flex: 1; height: 120px; font-size: 20px; background: #fdd"
          >
            ⬅️<br />{{ questions[currentIdx].option_a }}
          </button>
          <button
            @click="choose('B')"
            style="flex: 1; height: 120px; font-size: 20px; background: #ddf"
          >
            {{ questions[currentIdx].option_b }}<br />➡️
          </button>
        </div>
      </div>
    </div>
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
            <template v-if="m.is_chat_open">
              <button @click="openChat(m.match_id)">채팅 열기</button>
            </template>
            <template v-else>
              <button @click="payForMatch(m.match_id)">
                💳 결제하고 채팅 열기
              </button>
              <small>(서로 결제해야 열려요)</small>
            </template>
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
