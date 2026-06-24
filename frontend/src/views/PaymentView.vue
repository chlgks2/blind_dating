<script setup>
    // PaymentView.vue 의 <script setup> 예시
    import { useRoute } from 'vue-router'

    const route = useRoute()
    const targetUser = route.query.userName // 👈 여기에 방금 넘긴 이름이 쏙 들어옵니다!
</script>

<template>
    <div class="payment-card">
        <h2>✨ {{ targetUser }}님과의 시크릿 대화방 열기</h2>
        <p>페르소나 매칭권을 구매하시면 즉시 대화가 시작됩니다.</p>
    </div>
</template>

<style scoped>

</style>