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

// No props or emits needed for this component

// Router (will be used when implementing navigation after login)
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
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
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

    // TODO: Replace with actual API call
    await simulateLogin()

    ElMessage.success('登录成功！')
    
    // TODO: Navigate to dashboard or home page after successful login
    // router.push('/dashboard')
    console.log('Login successful, navigation will be implemented here', router)
    
  } catch (error) {
    console.error('Login error:', error)
    ElMessage.error(error.message || '登录失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * Simulate login API call (replace with actual implementation)
 */
const simulateLogin = () => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Simulate successful login
      if (loginForm.email && loginForm.password) {
        resolve({ success: true })
      } else {
        reject(new Error('登录信息不完整'))
      }
    }, 1500)
  })
}
</script>

<style scoped>
.login-form {
  position: relative;
}

.form-title {
  color: #303133;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 14px;
  margin-bottom: 0;
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
