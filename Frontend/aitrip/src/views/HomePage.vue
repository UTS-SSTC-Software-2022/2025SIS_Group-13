<template>
  <div class="home-page">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="home-header">
        <div class="logo">🌍 Travel App</div>
        <el-menu mode="horizontal" class="menu" :default-active="activeMenu">
          <el-menu-item index="home" @click="go('/home')">Home</el-menu-item>
          <el-menu-item index="plan" @click="go('/travel/plan')">Plan Trip</el-menu-item>
          <el-menu-item index="profile" @click="go('/profile')">Profile</el-menu-item>
          <el-menu-item index="logout" @click="logout">Logout</el-menu-item>
        </el-menu>
      </el-header>

      <!-- 内容区 -->
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { logoutAPI } from '@/apis/auth'

// ✅ 本地图片用 import，Vite 会做打包处理
import tokyoImg from '@/assets/images/destination/Tokyo.bmp'
import parisImg from '@/assets/images/destination/paris.bmp'
import sydneyImg from '@/assets/images/destination/Syndey.bmp'   // 你当前文件名是 Syndey
import newyorkImg from '@/assets/images/destination/newyork.bmp'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'

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

const onImgError = (e) => {
  e.target.onerror = null
  e.target.src = 'https://via.placeholder.com/400x300?text=Image+Unavailable'
}

</script>


<style scoped>
.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  padding: 0 20px;
}
.menu {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}
.home-main {
  padding: 20px;
}
.welcome {
  text-align: center;
  margin-bottom: 40px;
}
.destination-card {
  text-align: center;
}
.card-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
.card-title {
  margin-top: 10px;
  font-weight: bold;
}
</style>
