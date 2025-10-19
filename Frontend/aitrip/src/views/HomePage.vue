<template>
  <div class="home-page">
    <!-- 顶部Header -->
    <header class="home-header">
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
    </header>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="container-fluid">
        <div class="row">
          <!-- 桌面端左侧菜单 -->
          <div class="col-auto d-none d-md-block sidebar-col">
            <nav class="sidebar">
              <div class="sidebar-menu">
                <div class="menu-item" :class="{ active: activeMenu === 'home' }" @click="go('/home')">
                  <el-icon><House /></el-icon>
                  <span>Home</span>
                </div>
                <div class="menu-item" :class="{ active: activeMenu === 'plan' }" @click="go('/travel/plan')">
                  <el-icon><MapLocation /></el-icon>
                  <span>Plan Trip</span>
                </div>
                <div class="menu-item" :class="{ active: activeMenu === 'profile' }" @click="go('/profile')">
                  <el-icon><User /></el-icon>
                  <span>Profile</span>
                </div>
                <div class="menu-item" @click="logout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>Logout</span>
                </div>
              </div>
            </nav>
          </div>

          <!-- 主内容区 -->
          <div class="col home-main">
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
              <div class="row">
                <div class="col-lg-3 col-md-6 col-sm-6 col-12 mb-3" v-for="(item, index) in destinations" :key="index">
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
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 手机端底部导航栏 -->
    <nav class="bottom-nav d-md-none">
      <div class="nav-item" :class="{ active: activeMenu === 'home' }" @click="go('/home')">
        <el-icon><House /></el-icon>
        <span>Home</span>
      </div>
      <div class="nav-item" :class="{ active: activeMenu === 'plan' }" @click="go('/travel/plan')">
        <el-icon><MapLocation /></el-icon>
        <span>Plan</span>
      </div>
      <div class="nav-item" :class="{ active: activeMenu === 'profile' }" @click="go('/profile')">
        <el-icon><User /></el-icon>
        <span>Profile</span>
      </div>
      <div class="nav-item" @click="logout">
        <el-icon><SwitchButton /></el-icon>
        <span>Logout</span>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { House, MapLocation, User, SwitchButton, ArrowDown } from '@element-plus/icons-vue'
import { logoutAPI } from '@/apis/auth'

// ✅ 本地图片用 import，Vite 会做打包处理
import tokyoImg from '@/assets/images/destination/Tokyo.bmp'
import parisImg from '@/assets/images/destination/paris.bmp'
import sydneyImg from '@/assets/images/destination/Syndey.bmp'   // 你当前文件名是 Syndey
import newyorkImg from '@/assets/images/destination/newyork.bmp'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'
const activeMenu = ref('home')

const destinations = ref([
  { name: 'Tokyo',     image: tokyoImg },
  { name: 'Paris',     image: parisImg },
  { name: 'Sydney',    image: sydneyImg },   // 若你改名为 sydney.bmp，这里也要改
  { name: 'New York',  image: newyorkImg }
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

const openPlan = (destination) => {
  // Navigate to travel plan page with destination pre-filled
  router.push('/travel/plan')
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
  display: flex;
  flex-direction: column;
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
  flex-shrink: 0;
}

.logo {
  width: 10rem;
  height: 5rem;
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

/* 主要内容区域 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 80px; /* 为底部导航栏留出空间 */
}

/* 桌面端左侧菜单样式 */
.sidebar-col {
  width: 180px;
  max-width: 200px;
  flex: 0 0 200px;
}

.sidebar {
  background-color: #0f0f0f;
  height: 100%;
  padding: 0;
  width: 200px;
}

.sidebar-menu {
  padding: 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  color: #ccc;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.menu-item:hover {
  background-color: #1890ff;
  color: #fff;
}

.menu-item.active {
  background-color: #1890ff;
  color: #fff;
  border-left-color: #fff;
}

.menu-item .el-icon {
  margin-right: 12px;
  font-size: 18px;
}

.menu-item span {
  font-size: 14px;
}

/* 主内容区样式 */
.home-main {
  padding: 24px;
  background-color: #1a1a1a;
  min-height: calc(100vh - 64px);
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
  height: 100%;
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

/* 手机端底部导航栏样式 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #1f1f1f;
  border-top: 1px solid #333;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  z-index: 1000;
  height: 60px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 8px 12px;
  transition: all 0.3s;
  color: #ccc;
  flex: 1;
  min-width: 0;
}

.nav-item:hover {
  color: #1890ff;
}

.nav-item.active {
  color: #1890ff;
}

.nav-item .el-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.nav-item span {
  font-size: 10px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 响应式调整 */
@media (min-width: 768px) {
  .main-content {
    padding-bottom: 0;
  }
}

@media (max-width: 767px) {
  .home-main {
    padding: 16px;
    min-height: calc(100vh - 64px - 60px);
  }
  
  .welcome {
    padding: 24px;
    margin-bottom: 24px;
  }
  
  .welcome h1 {
    font-size: 1.5rem;
  }
  
  .recommend-section {
    padding: 16px;
  }
  
  .recommend-section h2 {
    font-size: 1.25rem;
  }
}
</style>
