<template>
  <div class="plan-manage-page">
    <el-container class="layout-container" direction="vertical">
      <!-- 顶部Header，与 HomePage 保持一致 -->
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

      <!-- 左侧菜单 + 右侧内容 -->
      <el-container class="bottom-container">
        <!-- 左侧菜单（与 HomePage 一致） -->
        <el-aside class="sidebar" width="200px">
          <el-menu 
            mode="vertical" 
            class="sidebar-menu" 
            :default-active="activeMenu"
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

        <!-- 右侧主内容：左右两栏 -->
        <el-main class="home-main">
          <div class="manage-header">
            <h1>Trip Plan Management</h1>
            <el-button type="primary" @click="go('/travel/plan/create')">Create Plan</el-button>
          </div>

          <el-row :gutter="20" class="content-row">
            <!-- Left: Plans (single card with two sections) -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
              <div class="section-card">
                <div class="section-header">
                  <h2>Trip Plans</h2>
                </div>

                <div class="subsection">
                  <h3 class="sub-title">Generated Plans</h3>
                  <div class="plan-list" v-loading="loading">
                    <div
                      v-for="(plan, idx) in generatedPlans"
                      :key="plan.id"
                      class="plan-item"
                      @click="openItinerary(plan)"
                    >
                      <div class="plan-title">{{ plan.title }}</div>
                      <div class="plan-meta">
                        <span>{{ plan.destination }}</span>
                        <span>·</span>
                        <span>{{ plan.duration }}</span>
                        <span>·</span>
                        <span>{{ plan.date }}</span>
                      </div>
                      <div class="plan-actions" @click.stop>
                        <el-popover trigger="click" placement="bottom-end">
                          <div class="popover-actions">
                            <el-button type="danger" text size="small" @click.stop="confirmDelete('generated', plan)">Delete</el-button>
                          </div>
                          <template #reference>
                            <el-icon class="more-icon"><MoreFilled /></el-icon>
                          </template>
                        </el-popover>
                      </div>
                    </div>
                    <div v-if="!loading && generatedPlans.length === 0" class="empty-hint">No generated plans yet</div>
                  </div>
                </div>

                <el-divider class="divider-light" />

                <div class="subsection">
                  <h3 class="sub-title">Completed Plans</h3>
                  <div class="plan-list" v-loading="loading">
                    <div
                      v-for="(plan, idx) in finishedPlans"
                      :key="plan.id"
                      class="plan-item"
                      @click="openItinerary(plan)"
                    >
                      <div class="plan-title">{{ plan.title }}</div>
                      <div class="plan-meta">
                        <span>{{ plan.destination }}</span>
                        <span>·</span>
                        <span>{{ plan.duration }}</span>
                        <span>·</span>
                        <span>{{ plan.date }}</span>
                      </div>
                      <div class="plan-actions" @click.stop>
                        <el-popover trigger="click" placement="bottom-end">
                          <div class="popover-actions">
                            <el-button type="danger" text size="small" @click.stop="confirmDelete('finished', plan)">Delete</el-button>
                          </div>
                          <template #reference>
                            <el-icon class="more-icon"><MoreFilled /></el-icon>
                          </template>
                        </el-popover>
                      </div>
                    </div>
                    <div v-if="!loading && finishedPlans.length === 0" class="empty-hint">No completed plans yet</div>
                  </div>
                </div>
              </div>
            </el-col>

            <!-- Right: Google Map -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
              <RecordMap 
                :plans="generatedPlans" 
                :finishedPlans="finishedPlans"
                class="map-container"
              />
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, MapLocation, User, SwitchButton, ArrowDown, MoreFilled } from '@element-plus/icons-vue'
import RecordMap from '@/components/map/RecordMap.vue'
import request from '@/apis/request'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'
const activeMenu = ref('plan')

const generatedPlans = ref([])
const finishedPlans = ref([])
const loading = ref(false)

const go = (path) => router.push(path)

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

// 从后端API加载行程数据
const loadItineraries = async () => {
  loading.value = true
  try {
    // 确保token存在
    const token = localStorage.getItem('token')
    console.log('Token from localStorage:', token ? 'exists' : 'not found')
    
    if (!token) {
      ElMessage.error('Please login first')
      router.push('/login-form')
      return
    }

    console.log('Making API request to /itinerary/itineraries/')
    const response = await request.get('/itinerary/itineraries/')
    console.log('API response:', response)
    console.log('Response type:', typeof response)
    console.log('Response.data type:', typeof response.data)
    console.log('Response.data:', response.data)
    
    // 更健壮的响应解析逻辑
    let itineraries = []
    if (Array.isArray(response.data)) {
      // 如果response.data直接是数组
      itineraries = response.data
      console.log('Using response.data as direct array')
    } else if (response.data && Array.isArray(response.data.results)) {
      // 如果response.data.results是数组
      itineraries = response.data.results
      console.log('Using response.data.results')
    } else if (response.data && Array.isArray(response.data.data)) {
      // 如果response.data.data是数组
      itineraries = response.data.data
      console.log('Using response.data.data')
    } else if (Array.isArray(response)) {
      // 如果response本身是数组
      itineraries = response
      console.log('Using response as direct array')
    } else {
      console.warn('Unexpected response format:', response)
      itineraries = []
    }
    
    console.log('Parsed itineraries:', itineraries)
    
    // 使用nextTick确保DOM更新完成
    await nextTick()
    
    // 根据isCompleted状态分类
    generatedPlans.value = itineraries
      .filter(item => item.isCompleted === 'Generated')
      .map(item => ({
        id: item.itinerary_id,
        title: item.title || '未命名行程',
        destination: item.destination || '未知目的地',
        duration: item.duration || '0 days',
        date: item.start_time ? new Date(item.start_time).toLocaleDateString() : new Date(item.create_time).toLocaleDateString(),
        start_time: item.start_time,
        itinerary_id: item.itinerary_id,
        isCompleted: item.isCompleted
      }))
    
    finishedPlans.value = itineraries
      .filter(item => item.isCompleted === 'Completed')
      .map(item => ({
        id: item.itinerary_id,
        title: item.title || '未命名行程',
        destination: item.destination || '未知目的地',
        duration: item.duration || '0 days',
        date: item.start_time ? new Date(item.start_time).toLocaleDateString() : new Date(item.create_time).toLocaleDateString(),
        start_time: item.start_time,
        itinerary_id: item.itinerary_id,
        isCompleted: item.isCompleted
      }))
      
    console.log('Loaded itineraries:', { generatedPlans: generatedPlans.value, finishedPlans: finishedPlans.value })
      
  } catch (error) {
    console.error('Failed to load itineraries:', error)
    console.error('Error details:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    })
    
    if (error.response?.status === 401) {
      ElMessage.error('Login expired, please login again')
      router.push('/login-form')
    } else {
      ElMessage.error('Failed to load itinerary list: ' + (error.message || 'Unknown error'))
    }
  } finally {
    loading.value = false
  }
}

const openItinerary = (plan) => {
  router.push({ 
    path: '/travel/itinerary-result', 
    query: { 
      itinerary_id: plan.itinerary_id || plan.id 
    } 
  })
}

const confirmDelete = async (type, plan) => {
  try {
    await ElMessageBox.confirm(
      `Delete "${plan.title}"?`,
      'Confirm Deletion',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    // 调用后端API删除行程
    await request.delete(`/itinerary/itineraries/${plan.itinerary_id || plan.id}/`)
    
    // 从本地列表中移除
    if (type === 'generated') {
      generatedPlans.value = generatedPlans.value.filter(p => p.id !== plan.id)
    } else {
      finishedPlans.value = finishedPlans.value.filter(p => p.id !== plan.id)
    }
    ElMessage.success('Plan deleted')
  } catch (error) {
    if (error.name !== 'cancel') {
      console.error('Failed to delete itinerary:', error)
      ElMessage.error('Failed to delete itinerary')
    }
  }
}

onMounted(async () => {
  // 等待DOM完全渲染
  await nextTick()
  // 添加小延迟确保所有组件都已初始化
  setTimeout(() => {
    loadItineraries()
  }, 100)
})
</script>

<style scoped>
.plan-manage-page {
  height: 100vh;
  background-color: #141414;
}

.layout-container {
  height: 100vh;
  background-color: #141414;
}

/* 左侧菜单样式复用 */
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

/* 顶部与主区域样式复用 */
.bottom-container {
  flex: 1;
  height: calc(100vh - 64px);
}

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

.home-main {
  padding: 24px;
  background-color: #1a1a1a;
  overflow-y: auto;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.manage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #262626;
  padding: 16px 20px;
  border-radius: 8px;
  border: 1px solid #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 20px;
}

.manage-header h1 {
  color: #fff;
  font-size: 20px;
  margin: 0;
}

.section-card {
  background: #262626;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.section-header h2 {
  color: #fff;
  margin: 0 0 12px;
}

.plan-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.plan-item {
  background: #333;
  border: 1px solid #444;
  border-radius: 6px;
  padding: 12px 14px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  position: relative;
}

.plan-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  border-color: #1890ff;
}

.plan-title {
  color: #fff;
  font-weight: 600;
}

.plan-meta {
  color: #bbb;
  font-size: 12px;
  margin-top: 4px;
}

.empty-hint {
  color: #888;
  text-align: center;
  padding: 10px;
}

.mt-20 { margin-top: 20px; }

/* Stretch row to allow the map to occupy full right-side space */
.content-row {
  flex: 1;
  align-items: stretch;
}

.sub-title {
  color: #ddd;
  font-size: 14px;
  margin: 0 0 8px;
}

.divider-light {
  --el-border-color: rgba(255, 255, 255, 0.12);
}

.map-container {
  height: 100%;
  min-height: 500px;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .manage-header {
    flex-direction: column;
    gap: 12px;
  }

  .map-container {
    min-height: 300px;
  }
}
.more-icon {
  color: #bbb;
  cursor: pointer;
  transition: color 0.2s ease;
}
.more-icon:hover {
  color: #fff;
}

.plan-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  align-items: center;
}

.popover-actions {
  display: flex;
  flex-direction: column;
}
</style>