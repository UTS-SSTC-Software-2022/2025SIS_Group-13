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
                  <div class="plan-list">
                    <div
                      v-for="(plan, idx) in generatedPlans"
                      :key="plan.id"
                      class="plan-item"
                      @click="openItinerary(plan)"
                    >
                      <div class="plan-title">{{ plan.title }}</div>
                      <div class="plan-meta">{{ plan.destination }} · {{ plan.duration }} · {{ plan.date }}</div>
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
                    <div v-if="generatedPlans.length === 0" class="empty-hint">No generated plans yet</div>
                  </div>
                </div>

                <el-divider class="divider-light" />

                <div class="subsection">
                  <h3 class="sub-title">Completed Plans</h3>
                  <div class="plan-list">
                    <div
                      v-for="(plan, idx) in finishedPlans"
                      :key="plan.id"
                      class="plan-item"
                      @click="openItinerary(plan)"
                    >
                      <div class="plan-title">{{ plan.title }}</div>
                      <div class="plan-meta">{{ plan.destination }} · {{ plan.duration }} · {{ plan.date }}</div>
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
                    <div v-if="finishedPlans.length === 0" class="empty-hint">No completed plans yet</div>
                  </div>
                </div>
              </div>
            </el-col>

            <!-- Right: Google Map -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
              <RecordMap 
                :plans="generatedPlans" 
                :finished-plans="finishedPlans"
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, MapLocation, User, SwitchButton, ArrowDown, MoreFilled } from '@element-plus/icons-vue'
import RecordMap from '@/components/map/RecordMap.vue'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'
const activeMenu = ref('plan')

const generatedPlans = ref([])
const finishedPlans = ref([])

const go = (path) => router.push(path)

const logout = async () => {
  try {
    // 保持与 HomePage 一致的退出逻辑（若有 API 可替换）
    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    ElMessage.success('Logged out successfully')
    router.push('/login')
  } catch (e) {
    ElMessage.error('Logout failed')
  }
}

// 模拟从本地加载计划（后期可替换为后端数据）
const loadMockPlans = () => {
  generatedPlans.value = [
    { id: 'g1', title: '悉尼三日游', destination: 'Sydney', duration: '3天', date: '2025-04-15', formData: { destination: 'Sydney', duration: 3 } },
    { id: 'g2', title: '墨尔本亲子行', destination: 'Melbourne', duration: '5天', date: '2025-05-02', formData: { destination: 'Melbourne', duration: 5 } },
  ]
  finishedPlans.value = [
    { id: 'f1', title: '堪培拉文化之旅', destination: 'Canberra', duration: '2天', date: '2025-03-28', formData: { destination: 'Canberra', duration: 2 } },
  ]
}

const openItinerary = (plan) => {
  const payload = encodeURIComponent(JSON.stringify(plan.formData || {}))
  router.push({ path: '/travel/itinerary-result', query: { formData: payload } })
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
    if (type === 'generated') {
      generatedPlans.value = generatedPlans.value.filter(p => p.id !== plan.id)
    } else {
      finishedPlans.value = finishedPlans.value.filter(p => p.id !== plan.id)
    }
    ElMessage.success('Plan deleted')
  } catch (e) {
    // cancelled
  }
}

onMounted(() => {
  loadMockPlans()
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