<template>
  <div class="login-form">
    <!-- Header -->
    <div class="text-center mb-4">
      <h2 class="form-title">Welcome back</h2>
      <p class="form-subtitle text-muted">Please use your email to login</p>
      

    </div>

    <!-- Login Form -->
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      class="login-form-content"
      label-position="top"
      size="large"
    >
      <!-- Email Field -->
      <el-form-item label="Email" prop="email">
        <el-input
          v-model="loginForm.email"
          type="email"
          placeholder="Please enter your email address"
          prefix-icon="el-icon-message"
          :disabled="loading"
          clearable
        />
      </el-form-item>

      <!-- Password Field -->
      <el-form-item label="Password" prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="Please enter your password"
          prefix-icon="el-icon-lock"
          :disabled="loading"
          show-password
          clearable
        />
      </el-form-item>

      <!-- Remember Me & Forgot Password -->
      <div class="form-options d-flex justify-content-between align-items-center mb-3">
        <el-checkbox v-model="loginForm.rememberMe" :disabled="loading">
          Remember me
        </el-checkbox>
        <router-link 
          to="/forgot-password" 
          class="forgot-password-link"
          :class="{ disabled: loading }"
        >
          Forgot password?
        </router-link>
      </div>

      <!-- Login Button -->
      <el-form-item class="mb-3">
        <el-button
          type="primary"
          class="login-btn w-100"
          :loading="loading"
          @click="handleLogin"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </el-button>
      </el-form-item>

      <!-- Register Link -->
      <div class="text-center">
        <span class="text-muted">No account? </span>
        <router-link 
          to="/register" 
          class="register-link ms-1"
          :class="{ disabled: loading }"
        >
          Register now
        </router-link>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { loginAPI } from '@/apis/auth'

// No props or emits needed for this component

// Router
const router = useRouter()

// Form ref
const loginFormRef = ref()

// Loading state
const loading = ref(false)

// Form data
const loginForm = reactive({
  email: '',
  password: '',
  rememberMe: false
})

// Form validation rules
const loginRules = {
  email: [
    { required: true, message: 'Please enter your email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter your password', trigger: 'blur' },
    { min: 6, message: 'Password length must be at least 6 characters', trigger: 'blur' }
  ]
}

/**
 * Handle login form submission
 */
const handleLogin = async () => {
  try {
    // Validate form
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // Call login API
    const response = await loginAPI({
      email: loginForm.email,
      password: loginForm.password,
      rememberMe: loginForm.rememberMe
    })

    // Handle successful login
    console.log('=== LOGIN API RESPONSE DEBUG ===')
    console.log('Response status:', response.status)
    console.log('Response headers:', response.headers)
    console.log('Full response object:', response)
    console.log('Login response:', response)
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
.login-form {
  position: relative;
}

.form-title {
  color: #E5E7EB;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 14px;
  margin-bottom: 0;
  color: #9CA3AF;
}



.login-form-content {
  margin-top: 2rem;
}

.form-options {
  font-size: 14px;
}

.forgot-password-link,
.register-link {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.forgot-password-link:hover,
.register-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.forgot-password-link.disabled,
.register-link.disabled {
  color: #c0c4cc;
  pointer-events: none;
  cursor: not-allowed;
}

.login-btn {
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
}

/* Mobile specific styles */
@media (max-width: 576px) {
  .form-title {
    font-size: 1.5rem;
  }
  
  .login-form-content {
    margin-top: 1.5rem;
  }
}
</style>