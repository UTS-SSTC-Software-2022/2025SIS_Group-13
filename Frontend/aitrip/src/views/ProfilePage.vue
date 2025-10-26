<template>
  <el-container class="layout-container" direction="vertical">
    <el-container class="bottom-container">
      <el-aside class="sidebar" width="200px">
        <el-menu 
          mode="vertical" 
          class="sidebar-menu" 
          :default-active="'profile'"
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
          <el-menu-item index="logout" @click="go('/login-form')">
            <el-icon><SwitchButton /></el-icon>
            <span>Logout</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-main class="home-main">
        <div class="auth-card">
          <el-page-header
            class="page-header"
            @back="$router.back()"
            title="< Back"
            content="User Profile"
          />

          <h1 class="title">Manage Your Profile</h1>
          <p class="subtitle">Tell us who you are. We’ll personalize your trip experience.</p>

          <el-divider>
            <span class="section-name">Basic Information</span>
          </el-divider>

          <el-form
            ref="formRef"
            :model="profile"
            label-position="top"
            class="form"
          >
            <el-form-item label="* Email">
              <el-input v-model="profile.email" placeholder="email@example.com" :disabled="true" />
            </el-form-item>

            <el-form-item label="* First Name">
              <el-input v-model="profile.firstName" placeholder="John" clearable />
            </el-form-item>

            <el-form-item label="* Last Name">
              <el-input v-model="profile.lastName" placeholder="Doe" clearable />
            </el-form-item>

            <el-form-item label="* Phone">
              <el-input v-model="profile.phone" placeholder="+61 4xx xxx xxx" clearable />
            </el-form-item>

            <el-form-item label="Avatar">
              <el-input v-model="profile.avatar" placeholder="Image URL" clearable />
            </el-form-item>

            <el-divider>
              <span class="section-name">Settings</span>
            </el-divider>

            <el-form-item label="Dark Mode">
              <el-switch v-model="darkMode" />
            </el-form-item>

            <div class="actions">
              <el-button type="primary" class="btn-primary" @click="onSave">Save</el-button>
            </div>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { House, MapLocation, User, SwitchButton } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getUserProfileAPI, updateUserProfileAPI } from '@/apis/auth'

const router = useRouter()
const go = (path) => router.push(path)

// 用户资料数据结构
const profile = reactive({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  avatar: ''
})
const darkMode = ref(false)
const formRef = ref(null)

// Load user profile data
const loadProfile = async () => {
  try {
    const response = await getUserProfileAPI()
    if (response && response.data) {
      const userData = response.data
      profile.email = userData.email || ''
      profile.firstName = userData.first_name || userData.firstName || ''
      profile.lastName = userData.last_name || userData.lastName || ''
      profile.phone = userData.phone || ''
      profile.avatar = userData.avatar || ''
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
    ElMessage.error('Failed to load user profile')
  }
}

// Save user profile
const onSave = async () => {
  try {
    const response = await updateUserProfileAPI({
      first_name: profile.firstName,
      last_name: profile.lastName,
      phone: profile.phone,
      avatar: profile.avatar
    })
    
    if (response) {
      ElMessage.success('Profile updated successfully!')
    }
  } catch (error) {
    console.error('Failed to update profile:', error)
    ElMessage.error('Failed to update profile. Please try again.')
  }
}


// Load profile on component mount
onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
/* ===== 页面框架 ===== */
.profile-shell {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.auth-bg {
  position: fixed;
  inset: 0;
  /* 与注册页一致的深色渐变背景 */
  background:
    radial-gradient(1200px 600px at 10% 10%, rgba(99, 102, 241, 0.25), transparent 60%),
    radial-gradient(1000px 600px at 90% 80%, rgba(168, 85, 247, 0.22), transparent 60%),
    linear-gradient(135deg, #0b1220 0%, #121a2b 45%, #121b2e 100%);
}

/* 主要卡片容器（深色毛玻璃，与注册页一致） */
.auth-card {
  width: min(1100px, 92vw);
  margin: 64px auto;
  padding: 28px 28px 32px;
  border-radius: 18px;
  background: rgba(17, 24, 39, 0.65);
  border: 1px solid rgba(148, 163, 184, 0.15);
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.45),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #e5e7eb;
}

/* 顶部标题与副标题（保持原文案与格式） */
.title {
  margin: 8px 0 4px;
  font-size: 32px;
  line-height: 1.25;
  font-weight: 800;
  letter-spacing: 0.2px;
  color: #e8edf7;
}

.subtitle {
  margin: 0 0 10px;
  color: #9aa4b2;
  font-size: 15px;
}

/* 分段标题 */
.section-name {
  color: #cbd5e1;
  font-weight: 600;
}

/* Element Plus 分隔线颜色在深色背景下的微调 */
:deep(.el-divider) {
  border-color: rgba(148, 163, 184, 0.18);
}

/* 表单控件深色适配（与注册页风格一致） */
.form {
  margin-top: 8px;
}

/* 输入框外观（深色半透明 + 轻描边） */
:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.035) !important;
  box-shadow: none !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  color: #e5e7eb !important;
}

/* placeholder */
:deep(.el-input__inner::placeholder),
:deep(.el-textarea__inner::placeholder) {
  color: #9aa4b2 !important;
}

/* focus 态 */
:deep(.el-input.is-focus .el-input__wrapper),
:deep(.el-textarea.is-focus .el-textarea__inner),
:deep(.el-select .el-input.is-focus .el-input__wrapper) {
  border-color: #7c8cf8 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.22) !important;
  background: rgba(255, 255, 255, 0.06) !important;
}

/* 标签颜色微调 */
:deep(.el-form-item__label) {
  color: #cdd6e3 !important;
}

/* 开关在深色背景下的对比度 */
:deep(.el-switch .el-switch__core) {
  background: rgba(255,255,255,0.08);
  border-color: rgba(148, 163, 184, 0.28);
}

/* 底部按钮区域 */
.actions {
  margin-top: 18px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 主按钮：与注册页一致的渐变主色（蓝紫） */
.btn-primary {
  border: none !important;
  background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
  color: #fff !important;
}

.btn-primary:hover {
  filter: brightness(1.05);
  box-shadow: 0 8px 22px rgba(99, 102, 241, 0.28);
}

/* 顶部 PageHeader 在深色下的对比度 */
.page-header {
  margin-bottom: 6px;
  color: #cbd5e1;
}
:deep(.el-page-header__title) { color: #cbd5e1; }
:deep(.el-page-header__content) { color: #e5e7eb; }

/* 响应式 */
@media (max-width: 768px) {
  .auth-card {
    width: min(100%, 94vw);
    padding: 20px 16px 24px;
    margin: 24px auto 40px;
  }
  .title { font-size: 26px; }
}
/* === 让分隔标题（Basic Information / Settings）透明底 + 白字 === */
:deep(.el-divider__text) {
  background-color: transparent !important; /* 去掉白色药丸背景 */
  color: #ffffff !important;               /* 标题文字为白色 */
  font-weight: 700;
  letter-spacing: .2px;
  padding: 0 6px;                           /* 轻微留白，避免紧贴线条 */
}

/* 分隔线在深色背景下的线条颜色微调（更柔和） */
:deep(.el-divider--horizontal) {
  border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
}

/* 如果你给 divider 包了 <span class="section-name">，统一为白色 */
.section-name {
  color: #ffffff !important;
}

/* Sidebar + main layout to match overall design */
.layout-container {
  height: 100vh;
  background-color: #141414;
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
  background-color: #1a1a1a;
  overflow-y: auto;
  height: 100%;
}

</style>
