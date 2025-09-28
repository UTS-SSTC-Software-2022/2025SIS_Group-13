<template>
  <div class="profile-page">
    <!-- 顶部渐变头部，风格与 TravelPlanPage 保持一致 -->
    <div class="hero">
        <el-page-header
        class="page-header"
        @back="() => router.push('/home')"
        title="< Back"
        content="User Profile"
        >
        <template #icon>
          <span />
        </template>
      </el-page-header>

      <div class="container">
        <el-card class="card main-card" shadow="hover">
          <h1 class="title">Manage Your Profile</h1>
          <p class="subtitle">Tell us who you are. We’ll personalize your trip experience.</p>

          <el-divider content-position="left">Basic Information</el-divider>

          <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" class="form-grid">
            <el-form-item label="Email" prop="email">
              <el-input v-model="form.email" placeholder="email@example.com" type="email" />
            </el-form-item>

            <el-form-item label="First Name" prop="firstName">
              <el-input v-model="form.firstName" placeholder="John" />
            </el-form-item>

            <el-form-item label="Last Name" prop="lastName">
              <el-input v-model="form.lastName" placeholder="Doe" />
            </el-form-item>

            <el-form-item label="Phone" prop="phone">
              <el-input v-model="form.phone" placeholder="+61 4xx xxx xxx" />
            </el-form-item>

            <el-form-item label="Avatar" prop="avatar">
              <div class="avatar-field">
                <el-input
                  v-model="form.avatar"
                  placeholder="Image URL"
                  clearable
                  @change="touchAvatarPreview"
                />
                <div class="avatar-preview" v-if="form.avatar">
                  <img :src="form.avatar" alt="avatar preview" @error="onAvatarError" />
                </div>
              </div>
            </el-form-item>

            <el-divider content-position="left">Settings</el-divider>

            <!-- 单一的外观开关：黑夜模式 -->
            <el-form-item label="Dark Mode">
              <el-switch v-model="settings.darkMode" @change="applyDarkMode" />
            </el-form-item>

            <!-- 操作区 -->
            <div class="actions">
              <el-button size="large" @click="goProfileShow" plain>
                View My Profile
              </el-button>
              <el-button size="large" @click="goPlanHistory" type="primary" plain>
                View Plan History
              </el-button>
              <el-button size="large" type="primary" @click="save" :loading="saving">
                Save
              </el-button>
            </div>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const goHome = () => router.push({ name: 'home' })

// 表单数据
const form = reactive({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  avatar: ''
})

const settings = reactive({
  darkMode: false
})

const rules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: 'blur' }
  ],
  firstName: [{ required: true, message: 'First name is required', trigger: 'blur' }],
  lastName: [{ required: true, message: 'Last name is required', trigger: 'blur' }],
  phone: [
    { required: true, message: 'Phone is required', trigger: 'blur' },
    { min: 6, message: 'Too short', trigger: 'blur' }
  ],
  avatar: [{ type: 'url', message: 'Avatar must be a valid URL', trigger: 'blur' }]
}

const formRef = ref()
const saving = ref(false)

onMounted(() => {
  // 恢复数据
  Object.assign(form, JSON.parse(localStorage.getItem('user_profile') || '{}'))
  const savedSettings = JSON.parse(localStorage.getItem('user_settings') || '{}')
  Object.assign(settings, savedSettings)

  // 首次加载根据设置应用暗色
  applyDarkMode(settings.darkMode)
})

const onAvatarError = () => {
  form.avatar = ''
  ElMessage.warning('Avatar preview failed, please check the URL')
}
const touchAvatarPreview = () => {}

const applyDarkMode = (isDark) => {
  const root = document.documentElement
  root.classList.toggle('dark', !!isDark)
}

const save = async () => {
  try {
    await formRef.value?.validate()
    saving.value = true
    localStorage.setItem('user_profile', JSON.stringify(form))
    localStorage.setItem('user_settings', JSON.stringify(settings))
    ElMessage.success('Profile saved successfully')
  } catch (e) {
    // 校验失败无须处理
  } finally {
    saving.value = false
  }
}

const goPlanHistory = () => {
  router.push({ path: '/travel/itinerary-result', query: { from: 'profile' } })
}

const goProfileShow = () => {
  router.push({ name: 'profile-show' })
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #6f73ff 0%, #a855f7 100%) fixed;
}

.hero {
  padding: 32px 0 64px;
}

.page-header {
  width: 1120px;
  margin: 0 auto 8px;
  color: #fff;
}

.container {
  width: 1120px;
  margin: 0 auto;
}

.card.main-card {
  border-radius: 18px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  padding: 28px 28px 8px;
}

.title {
  margin: 0 0 6px;
  font-size: 28px;
  font-weight: 700;
}

.subtitle {
  margin: 0 0 18px;
  color: #606266;
}

.form-grid :deep(.el-form-item) {
  max-width: 720px;
}

.avatar-field {
  display: flex;
  align-items: center;
  gap: 16px;
}
.avatar-preview {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  flex: 0 0 56px;
  border: 1px solid #ebeef5;
}
.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

/* 暗色模式下针对当前页面做一点补充（Element Plus 的暗色变量会生效） */
:global(html.dark) .profile-page {
  background: linear-gradient(135deg, #1f2438 0%, #2b2f3a 100%) fixed;
}
</style>