import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/MainView.vue'
import SigninView from '../views/SigninView.vue'
import QuestionsView from '../views/QuestionsView.vue'
import SignupView from '../views/SignupView.vue'
import SelectStyleView from '../views/SelectStyleView.vue'
import MyAvatarView from '../views/MyAvatarView.vue'
import MatchingView from '../views/MatchingView.vue'
import PaymentView from '../views/PaymentView.vue'
import ChatListView from '../views/ChatListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/signin',
      name: 'signin',
      component: SigninView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/select-style',
      name: 'select-style',
      component: SelectStyleView
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsView
    },
    {
      path: '/my-avatar',
      name: 'my-avatar',
      component: MyAvatarView
    },
    {
      path: '/matching',
      name: 'matching',
      component: MatchingView
    },
    {
      path: '/payment',
      name: 'payment',
      component: PaymentView
    },
    {
      path: '/chatlist',
      name: 'chatlist',
      component: ChatListView
    },


  ]
})

// 📄 src/router/index.js 맨 밑에 추가

// 🔒 라우터 가드: 화면이 바뀌기 직전에 로그인 여부를 검사합니다.
router.beforeEach((to, from, next) => {
  
  // 💡 [임시 설정] 로그인 상태 변수 (false로 바꾸면 로그인 화면으로 튕깁니다!)
  // 나중에 전역 상태(Pinia)나 localStorage 토큰 확인 로직으로 대체할 자리입니다.
  const isLoggedIn = false 

  // 1. 가려는 목적지(to.path)가 메인('/')인데 로그인이 안 되어 있다면?
  if (to.path === '/' && !isLoggedIn) {
    alert('로그인이 필요한 서비스입니다!') // 임시 알림창 (생략 가능)
    next('/signin') // 👈 강제로 로그인 페이지('/signin')로 튕겨버리기
  } 
  // 2. 로그인 상태이거나, 로그인/회원가입 페이지 등 다른 곳으로 갈 때는 정상 통과
  else {
    next() 
  }
})

// 기존에 있던 내보내기 코드
export default router