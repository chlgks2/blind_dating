<template>
  <div class="app-shell">
    <div class="mobile-frame">
      <div class="payment-screen">
        <div class="payment-card">
          <h2 class="payment-title">
            {{ userName }}님과의<br />대화를 위해<br />결제가 필요해요
          </h2>
          <div class="payment-info">
            <p class="payment-sub">상대방도 결제를 하면 대화가 시작됩니다!</p>
            <p class="payment-sub">하지않으면 자동으로 환불됩니다</p>
          </div>

          <div class="payment-btns">
            <button class="btn-pay" @click="handlePayment">결제하기</button>
            <button class="btn-back" @click="router.back()">뒤로가기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "@/api";

const router = useRouter();
const route = useRoute();
const userName = route.query.userName || "상대방";
const userId = Number(route.query.userId);

// ChatListView에서 matchId를 직접 전달받거나, userId로 조회
const matchId = ref(route.query.matchId ? Number(route.query.matchId) : null);

onMounted(async () => {
  // matchId가 이미 있으면 조회 불필요
  if (matchId.value) return;
  if (!userId) return;
  try {
    const res = await api.get("/matching/my-matches/");
    const found = res.data.matches.find((m) => m.other_user_id === userId);
    if (found) matchId.value = found.match_id;
  } catch (e) {
    console.error("매칭 조회 실패:", e);
  }
});

const handlePayment = () => {
  if (!matchId.value) {
    alert("매칭 정보를 찾을 수 없습니다. 먼저 친구요청을 주고받아야 합니다.");
    return;
  }

  // 포트원 V1 SDK (index.html에 iamport.js 로드됨)
  const IMP = window.IMP;
  IMP.init(import.meta.env.VITE_IMP_CODE || "imp07810156");

  IMP.request_pay(
    {
      pg: "kakaopay",
      pay_method: "card",
      merchant_uid: `match_${matchId.value}_${Date.now()}`,
      name: `${userName}님과의 채팅 열기`,
      amount: 100,
      buyer_name: "구매자",
    },
    async (rsp) => {
      if (!rsp.success) {
        alert(`결제 실패: ${rsp.error_msg}`);
        return;
      }
      try {
        const res = await api.post("/matching/payment/verify/", {
          match_id: matchId.value,
          imp_uid: rsp.imp_uid,
        });
        if (res.data.is_chat_open) {
          router.push({
            path: "/chat",
            query: { matchId: matchId.value, userName },
          });
        } else {
          alert("결제 완료! 상대방도 결제하면 채팅이 열립니다.");
          router.push("/chatlist");
        }
      } catch (e) {
        console.error("결제 검증 실패:", e);
        alert("결제 검증 중 오류가 발생했습니다.");
      }
    },
  );
};
</script>

<style scoped>
.payment-screen {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

.payment-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.payment-title {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 400;
  color: #fff;
  line-height: 1.3;
  letter-spacing: 0.01em;
}

.payment-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.562);
  line-height: 1.6;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0px;
}

.payment-btns {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.btn-pay {
  width: 100%;
  padding: 14px;
  background: #fff;
  color: var(--app-canvas-bg);
  border: none;
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: transform 0.14s ease;
}

.btn-pay:active {
  transform: scale(0.97);
}

.btn-back {
  width: 100%;
  padding: 14px;
  background: none;
  color: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--r-pill);
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 5\600;
  cursor: pointer;
  transition:
    border-color 0.2s,
    color 0.2s;
}

.btn-back:hover {
  border-color: rgba(255, 255, 255, 0.4);
  color: #fff;
}
</style>
