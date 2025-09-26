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
    if (response && (response.success || response.code === 200)) {
      // Save token and user info
      if (response.data?.token) {
        localStorage.setItem('token', response.data.token)
      }
      if (response.data?.user) {
        localStorage.setItem('userName', response.data.user.firstName || 'User')
      }

      ElMessage.success('Login successful!')

      // Redirect to homepage after login
      router.push('/home')
    } else {
      throw new Error(response.message || 'Login failed')
    }
    
  } catch (error) {
    console.error('Login error:', error)

    let errorMessage = 'Login failed, please try again'
    if (error.response?.status === 401) {
      errorMessage = 'Invalid email or password'
    } else if (error.response?.status === 403) {
      errorMessage = 'Account has been disabled, please contact support'
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
