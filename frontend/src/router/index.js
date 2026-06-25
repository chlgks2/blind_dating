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
import LoadingView from '../views/LoadingView.vue'
import ChatView from '@/views/ChatView.vue'

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
      path: '/loading',
      name: 'loading',
      component: LoadingView
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
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },


  ]
})

// 📄 src/router/index.js 맨 밑에 추가

// 🔒 라우터 가드: 화면이 바뀌기 직전에 로그인 여부를 검사합니다.
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access')

  if (to.path === '/' && !isLoggedIn) {
    next('/signin')
  } else {
    next()
  }
})

// 기존에 있던 내보내기 코드
export default router