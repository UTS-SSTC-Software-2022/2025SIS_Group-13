<template>
  <!-- 背景渐变层：与登录/注册页一致的柔和深色渐变 -->
  <div class="auth-bg"></div>

  <el-container class="layout-container" direction="vertical">
    <el-container class="bottom-container">
      <!-- Sidebar consistent with overall design -->
      <el-aside class="sidebar" width="200px">
        <el-menu 
          mode="vertical" 
          class="sidebar-menu" 
          :default-active="'plan'"
          background-color="#0f0f0f"
          text-color="#e5e7eb"
          active-text-color="#1890ff"
        >
          <el-menu-item index="home" @click="go('/home')">
            <el-icon><House /></el-icon>
            <span>Home</span>
          </el-menu-item>
          <el-menu-item index="plan" @click="go('/travel/plan')">
            <el-icon><MapLocation /></el-icon>
            <span>Plan Trip</span>
          </el-menu-item>
          <el-menu-item index="profile" @click="go('/profile')">
            <el-icon><User /></el-icon>
            <span>Profile</span>
          </el-menu-item>
          <el-menu-item index="logout" @click="logout">
            <el-icon><SwitchButton /></el-icon>
            <span>Logout</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- Main: full-width form, no card wrapper -->
      <el-main class="home-main">
        <el-page-header
          class="page-header"
          @back="goBack"
          title="Back"
          content="Create Your Personalized Travel Itinerary"
        />
        <div class="form-container">
          <TravelPlanForm @submit="handleFormSubmit" />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { House, MapLocation, User, SwitchButton } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import TravelPlanForm from '@/components/travel/TravelPlanForm.vue'

const router = useRouter()
const go = (path) => router.push(path)

/**
 * Go back to management page
 */
const goBack = () => {
  router.push('/travel/plan')
}

/**
 * Handle form submission
 * @param {Object} formData - The travel plan form data
 */
const handleFormSubmit = async (formData) => {
  try {
    console.log('Travel plan data (will be forwarded to results page):', formData)

    // Inform user and navigate to result page; result page will call /generate.
    ElMessage.info('Opening itinerary results...')

    await router.push({
      path: '/travel/itinerary-result',
      query: {
        formData: encodeURIComponent(JSON.stringify(formData))
      }
    })
  } catch (error) {
    console.error('Failed to navigate to results page:', error)
    ElMessage.error('Failed to open itinerary results, please try again')
  }
}

const logout = async () => {
  try {
    // 保持与 HomePage 一致的退出逻辑（若有 API 可替换）
    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    ElMessage.success('Logged out successfully')
    router.push('/login-form')
  } catch (e) {
    ElMessage.error('Logout failed')
  }
}

</script>

<style scoped>
/* Sidebar + main layout to match management page */
.layout-container {
  height: 100vh;
  background-color: transparent;
}

.bottom-container {
  flex: 1;
  height: 100vh;
}

.sidebar {
  background-color: #0f0f0f;
  height: 100%;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
}

.sidebar-menu .el-menu-item:hover {
  background-color: #1890ff !important;
}

.home-main {
  padding: 24px;
  /* 使用登录/注册页一致的深色渐变作为页面底色 */
  background: transparent;
  position: relative;
  z-index: 1;
  overflow-y: auto;
  height: 100%;
}

/* 背景渐变（复用 auth 页的样式） */
.auth-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(60rem 60rem at 10% 10%, rgba(99, 102, 241, .25), transparent 60%),
    radial-gradient(60rem 60rem at 90% 90%, rgba(236, 72, 153, .22), transparent 60%),
    linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
  filter: saturate(110%);
  z-index: 0;
}

.page-header {
  margin-bottom: 12px;
  color: #e6edf3; /* 深色背景下的浅色标题 */
}
:deep(.el-page-header__title) { color: #e6edf3; }
:deep(.el-page-header__content) { color: #a0aec0; }

.form-container {
  background: transparent; /* full-width form, no card */
}
</style>