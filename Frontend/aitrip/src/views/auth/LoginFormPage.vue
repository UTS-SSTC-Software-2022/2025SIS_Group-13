<template>
  <!-- 外层背景：与注册页一致 -->
  <div class="auth-shell">
    <div class="auth-bg"></div>

    <!-- 居中玻璃卡片 -->
    <div class="auth-card">
      <!-- 标题与副标题：文案不变，仅居中显示 -->
      <h1 class="title">Welcome back</h1>
      <p class="subtitle">Please use your email to login</p>

      <!-- 这里就是你提供的表单，原封不动放进来 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="form"
      >
        <el-form-item label=" Email" prop="email">
          <el-input
            v-model="form.email"
            placeholder="Please enter your email address"
            clearable
          />
        </el-form-item>

        <el-form-item label=" Password" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="Please enter your password"
          />
        </el-form-item>

        <div class="row between">
          <el-checkbox v-model="remember">Remember me</el-checkbox>
          <el-link type="primary" @click="$router.push('/forgot-password')">
            Forgot password?
          </el-link>
        </div>

        <el-button
          type="primary"
          size="large"
          class="btn-primary"
          :loading="loading"
          @click="onSubmit"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </el-button>

        <div class="footnote">
          <span>No account?</span>
          <el-link type="primary" @click="$router.push('/register')">
            Register now
          </el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { loginAPI } from '@/apis/auth'

const router = useRouter()

// 表单数据与校验
const formRef = ref()
const loading = ref(false)
const form = reactive({
  email: '',
  password: ''
})
const remember = ref(false)

const rules = {
  email: [
    { required: true, message: 'Please enter your email', trigger: 'blur' },
    { type: 'email', message: 'Invalid email address', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter your password', trigger: 'blur' },
    { min: 6, message: 'At least 6 characters', trigger: 'blur' }
  ]
}

// 登录提交逻辑
const onSubmit = async () => {
  try {
    // Validate form
    const valid = await formRef.value.validate()
    if (!valid) return

    loading.value = true

    // Call login API
    const response = await loginAPI({
      email: form.email,
      password: form.password,
      rememberMe: remember.value
    })

    // Handle successful login
    console.log('=== LOGIN API RESPONSE DEBUG ===')
    console.log('Response status:', response.status)
    console.log('Full response object:', response)
    console.log('Full response structure:', JSON.stringify(response, null, 2))
    
    // 检查响应是否成功
    if (response.status && response.status !== 200) {
      console.error('Login API returned non-200 status:', response.status)
      ElMessage.error(`Login failed: Server returned status ${response.status}`)
      return
    }
    
    // 检查响应数据结构
    if (!response.data) {
      console.error('No response data received')
      ElMessage.error('Login failed: No data returned from server')
      return
    }
    
    if (response.success || response.data) {
      // Store user info and token if provided
      console.log('Response data structure:', response.data)
      console.log('Response.data type:', typeof response.data)
      console.log('Response.data keys:', Object.keys(response.data || {}))
      console.log('Tokens:', response.data?.data?.tokens)
      console.log('Direct tokens:', response.data?.tokens)
      console.log('Access token path 1:', response.data?.data?.tokens?.access)
      console.log('Access token path 2:', response.data?.tokens?.access)
      console.log('Access token path 3:', response.data?.access_token)
      console.log('Access token path 4:', response.data?.token)
      
      // 尝试多种可能的token路径
      const tokenPath1 = response.data?.data?.tokens?.access
      const tokenPath2 = response.data?.tokens?.access
      const tokenPath3 = response.data?.access_token
      const tokenPath4 = response.data?.token
      
      // 尝试多种可能的用户信息路径
      const userPath1 = response.data?.data?.user
      const userPath2 = response.data?.user
      
      console.log('User path 1 (response.data?.data?.user):', userPath1)
      console.log('User path 2 (response.data?.user):', userPath2)
      
      const accessToken = tokenPath1 || tokenPath2 || tokenPath3 || tokenPath4
      const userInfo = userPath1 || userPath2
      
      if (accessToken) {
        localStorage.setItem('token', accessToken)
        console.log('Token stored in localStorage:', accessToken)
        console.log('Token verification from localStorage:', localStorage.getItem('token'))
      } else {
        console.error('No access token found in response')
        console.error('Available response data structure:', JSON.stringify(response.data, null, 2))
      }
      
      if (userInfo) {
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
        localStorage.setItem('userName', userInfo.username || userInfo.first_name || 'User')
        console.log('User info stored:', userInfo)
      } else {
        console.error('No user info found in response')
        console.error('Available response data structure:', JSON.stringify(response.data, null, 2))
      }

      ElMessage.success('Login successful!')
      
      // Navigate to home page after successful login
      router.push('/home')
    } else {
      throw new Error(response.message || 'Login failed')
    }
    
  } catch (error) {
    console.error('Login error:', error)
    
    // Handle different error types
    let errorMessage = 'Login failed, please try again'
    
    if (error.response?.status === 401) {
      errorMessage = 'Incorrect email or password'
    } else if (error.response?.status === 403) {
      errorMessage = 'Account has been disabled, please contact administrator'
    } else if (error.response?.status === 422) {
      errorMessage = 'Invalid request parameters'
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 外层和注册页相同的网格布局，垂直水平居中 */
.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  position: relative;
  overflow: hidden;
}

/* 渐变背景：与注册页一致（可直接复制你项目 RegisterPage.vue 的背景） */
.auth-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(60rem 60rem at 10% 10%, rgba(99, 102, 241, .25), transparent 60%),
    radial-gradient(60rem 60rem at 90% 90%, rgba(236, 72, 153, .22), transparent 60%),
    linear-gradient(135deg, #0b1220 0%, #1a2250 50%, #2a1f6a 100%);
  filter: saturate(110%);
  z-index: 0;
}

.auth-card {
  position: relative;
  z-index: 1;
  width: min(860px, 92vw);
  border-radius: 16px;
  padding: 40px 48px;
  background: rgba(16, 24, 40, 0.82);              /* 深色半透明 */
  border: 1px solid rgba(148, 163, 184, 0.18);     /* 微边框 */
  backdrop-filter: blur(24px);                     /* 毛玻璃 */
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
}

/* 标题/副标题与注册页的排版风格 */
.title {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  color: #E5E7EB;
  text-align: center;
  margin: 4px 0 8px;
}
.subtitle {
  text-align: center;
  margin: 0 0 24px;
  color: #9CA3AF;
}

/* Element Plus 输入框在深色卡片里的皮肤（和注册页一致） */
.auth-card :deep(.el-form-item__label) {
  color: #CBD5E1;
}
.auth-card :deep(.el-input__wrapper) {
  background: #0f172a;                             /* 深色输入框 */
  box-shadow: 0 0 0 1px rgba(148,163,184,.18) inset;
  border-radius: 10px;
}
.auth-card :deep(.el-input__inner) {
  color: #E5E7EB;
}
.auth-card :deep(.el-input__suffix) {
  color: #9CA3AF;
}

/* 行内辅助布局 */
.row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 6px 0 18px;
}
.between {
  justify-content: space-between;
}

/* 主按钮与注册页统一（你们项目里蓝色主色） */
.btn-primary {
  width: 100%;
  height: 44px;
  margin: 10px 0 18px;
  font-weight: 600;
}

/* 页脚提示 */
.footnote {
  text-align: center;
  color: #A7B0BF;
}
.footnote :deep(.el-link) {
  margin-left: 6px;
}

/* 让页面在窄屏下更舒服 */
@media (max-width: 640px) {
  .auth-card {
    padding: 28px 20px;
    border-radius: 14px;
  }
  .title { font-size: 26px; }
}
</style>