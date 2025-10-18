<template>
  <div class="home-page">
    <el-container class="layout-container" direction="vertical">
      <!-- 顶部Header - 横跨整个页面宽度 -->
      <el-header class="home-header">
        <div class="header-left">
          <img src="@/assets/images/LeisurA logo.svg" alt="LeisurA Logo" class="logo" />
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ userName }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="go('/profile')">Profile</el-dropdown-item>
                <el-dropdown-item divided @click="logout">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 下面部分：左侧菜单 + 右侧内容 -->
      <el-container class="bottom-container">
        <!-- 左侧菜单 -->
        <el-aside class="sidebar" width="200px">
          <el-menu 
            mode="vertical" 
            class="sidebar-menu" 
            :default-active="activeMenu"
            background-color="#0f0f0f"
            text-color="#ccc"
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

        <!-- 右侧主内容区 -->
        <el-main class="home-main">
        <div class="welcome">
          <h1>Welcome, {{ userName }}</h1>
          <p>Start planning your next adventure with AI-powered itineraries!</p>
          <el-button type="primary" size="large" @click="go('/travel/plan')">
            Start Planning
          </el-button>
        </div>

        <!-- 推荐目的地 -->
        <div class="recommend-section">
          <h2>Popular Destinations</h2>
          <el-row :gutter="20">
            <el-col :span="6" v-for="(item, index) in destinations" :key="index">
              <el-card shadow="hover" class="destination-card" @click="openPlan(item.name)">
                <img
                  :src="item.image"
                  :alt="`${item.name} photo`"
                  class="card-img"
                  loading="lazy"
                  @error="onImgError"
                />
                <div class="card-title">{{ item.name }}</div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { House, MapLocation, User, SwitchButton, ArrowDown } from '@element-plus/icons-vue'
import { logoutAPI } from '@/apis/auth'

// ✅ 本地图片用 import，Vite 会做打包处理
import CanberraImg from '@/assets/images/destination/Canberra.bmp'
import MelbourneImg from '@/assets/images/destination/Melbourne.bmp'
import sydneyImg from '@/assets/images/destination/Syndey.bmp'   // 你当前文件名是 Syndey
import BrisbaneImg from '@/assets/images/destination/Brisbane.bmp'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'
const activeMenu = ref('home')

const destinations = ref([
  { name: 'Canberra',     image: CanberraImg },
  { name: 'Melbourne',     image: MelbourneImg },
  { name: 'Sydney',    image: sydneyImg },   // 若你改名为 sydney.bmp，这里也要改
  { name: 'Brisbane',  image: BrisbaneImg }
])

const go = (path) => router.push(path)

const logout = async () => {
  try {
    await logoutAPI()
    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    ElMessage.success('Logged out successfully')
    router.push('/login')
  } catch (e) {
    ElMessage.error('Logout failed')
  }
}

const onImgError = (e) => {
  e.target.onerror = null
  e.target.src = 'https://via.placeholder.com/400x300?text=Image+Unavailable'
}

</script>


<style scoped>
.home-page {
  height: 100vh;
  background-color: #141414;
}

.layout-container {
  height: 100vh;
  background-color: #141414;
}


/* 左侧菜单样式 */
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

/* 下面部分容器样式 */
.bottom-container {
  flex: 1;
  height: calc(100vh - 64px); /* 减去header高度 */
}

/* Header样式 */
.home-header {
  background-color: #1f1f1f;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.logo {
  width: 10rem;
  height:5rem;
  filter: drop-shadow(0 0 10px rgba(4, 108, 184, 0.3));
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
  color: #fff;
}

.user-info:hover {
  background-color: #333;
}

.user-info .el-icon {
  margin-right: 8px;
}

.user-info .el-icon--right {
  margin-left: 8px;
  margin-right: 0;
}

/* 主内容区样式 */
.home-main {
  padding: 24px;
  background-color: #1a1a1a;
  overflow-y: auto;
  height: 100%;
}

.welcome {
  text-align: center;
  margin-bottom: 40px;
  background: #262626;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid #333;
}

.welcome h1 {
  color: #1890ff;
  margin-bottom: 16px;
}

.welcome p {
  color: #ccc;
}

.recommend-section {
  background: #262626;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid #333;
}

.recommend-section h2 {
  margin-bottom: 24px;
  color: #fff;
}

.destination-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: #333;
  border: 1px solid #444;
}

.destination-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  border-color: #1890ff;
}

.card-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.card-title {
  margin-top: 12px;
  font-weight: bold;
  color: #fff;
}
</style>
