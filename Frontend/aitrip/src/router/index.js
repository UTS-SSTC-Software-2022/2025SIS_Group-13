import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/__preview', name: 'preview', component: () => import('@/views/travel/ProfilePage.vue') },

  // ✅ 首屏进入 Landing：用你现有的 LoginPage.vue 当宣传页
  { path: '/', name: 'landing', component: () => import('@/views/auth/LoginPage.vue') },

  // 登录/注册/忘记密码（公开）
  { path: '/login-form', name: 'login-form', component: () => import('@/views/auth/LoginFormPage.vue') },
  { path: '/register',    name: 'register',    component: () => import('@/views/auth/RegisterPage.vue') },
  { path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/auth/ForgotPasswordPage.vue') },

  // 登录后页面
  { path: '/home', name: 'home', component: () => import('@/views/HomePage.vue') },
  { path: '/profile', name: 'profile', component: () => import('@/views/ProfilePage.vue') },
  { path: '/travel/plan', name: 'travel-plan', component: () => import('@/views/travel/TravelPlanPage.vue') },
  { path: '/travel/itinerary-result', name: 'travel-itinerary-result', component: () => import('@/views/travel/TravelItineraryResultPage.vue') },

  // 404
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundPage.vue') }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

// 🔒 路由守卫：未登录不可访问受保护页；已登录访问公开页时跳 Home
// router.beforeEach((to, from, next) => {
//   const publicPages = ['/', '/login-form', '/register', '/forgot-password']
//   const token = localStorage.getItem('token')

//   const goingToPublic = publicPages.includes(to.path)
//   const needsAuth = !goingToPublic

//   // 受保护页但没登录 → 回到登录表单（或你也可改成 '/'）
//   if (needsAuth && !token) return next('/login-form')

//   // 已登录又访问公开页（除 '/'，避免循环）→ 直接去首页
//   if (token && goingToPublic && to.path !== '/') return next('/home')

//   next()
// })

export default router
