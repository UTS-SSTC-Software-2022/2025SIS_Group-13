<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Header Section -->
      <div class="header-section">
        <img class="logo-icon" src="@/assets/images/LeisurA logo.svg" alt="logo">
        <h2 class="form-title">Create an Account</h2>
        <p class="form-subtitle">✈ Join us and start your AI journey</p>
      </div>

      <!-- Form Section -->
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        size="large"
        class="register-form"
      >
        <el-form-item label="Username" prop="username" class="form-item">
          <el-input
            v-model="registerForm.username"
            placeholder="Please enter your username"
            prefix-icon="User"
            class="custom-input"
          />
        </el-form-item>

        <div class="name-row">
          <el-form-item label="First Name" prop="firstname" class="form-item name-field">
            <el-input 
              v-model="registerForm.firstname"
              placeholder="Please enter your first name"
              prefix-icon="User"
              class="custom-input"
            />
          </el-form-item>
          <el-form-item label="Last Name" prop="lastname" class="form-item name-field">
            <el-input
              v-model="registerForm.lastname"
              placeholder="Please enter your last name"
              prefix-icon="User"
              class="custom-input"
            />
          </el-form-item>
        </div>

        <el-form-item label="Email" prop="email" class="form-item">
          <el-input
            v-model="registerForm.email"
            type="email"
              placeholder="Please enter your email address"
            prefix-icon="Message"
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password" class="form-item">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="Please enter your password (at least 6 characters)"
            prefix-icon="Lock"
            show-password
            class="custom-input"
          />
        </el-form-item>

        <el-form-item label="Confirm Password" prop="confirmPassword" class="form-item">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="Please enter your password again"
            prefix-icon="Lock"
            show-password
            class="custom-input"
          />
        </el-form-item>

        <el-form-item class="submit-section">
          <el-button type="primary" class="register-btn" size="large" @click="handleRegister">
            <span class="btn-text">Create Account</span>
          </el-button>
        </el-form-item>

        <div class="login-link-section">
          <span class="login-text">Already have an account?</span>
          <router-link to="/login-form" class="login-link">
            Login now
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { registerAPI } from '@/apis/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const registerFormRef = ref()

const registerForm = reactive({
  username: '',
  firstname: '',
  lastname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Validate password confirmation
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('The passwords do not match'))
  } else {
    callback()
  }
}

// Validate username - only allow letters, numbers, underscores, and hyphens
const validateUsername = (rule, value, callback) => {
  const usernameRegex = /^[a-zA-Z0-9_-]+$/
  if (!value) {
    callback(new Error('Please enter your username'))
  } else if (!usernameRegex.test(value)) {
    callback(new Error('Username can only contain letters, numbers, underscores, and hyphens'))
  } else {
    callback()
  }
}

// Validate first name - only allow letters
const validateFirstName = (rule, value, callback) => {
  const nameRegex = /^[a-zA-Z\u4e00-\u9fa5]+$/
  if (!value) {
    callback(new Error('Please enter your first name'))
  } else if (!nameRegex.test(value)) {
    callback(new Error('First name can only contain letters or Chinese characters'))
  } else {
    callback()
  }
}

// Validate last name - only allow letters
const validateLastName = (rule, value, callback) => {
  const nameRegex = /^[a-zA-Z\u4e00-\u9fa5]+$/
  if (!value) {
    callback(new Error('Please enter your last name'))
  } else if (!nameRegex.test(value)) {
    callback(new Error('Last name can only contain letters or Chinese characters'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { validator: validateUsername, trigger: 'blur' }
  ],
  firstname: [
    { validator: validateFirstName, trigger: 'blur' }
  ],
  lastname: [
    { validator: validateLastName, trigger: 'blur' }
  ],
  email: [
    {  message: 'Please enter your email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ],
  password: [
    {  message: 'Please enter your password', trigger: 'blur' },
    { min: 6, message: 'Password length must be at least 6 characters', trigger: 'blur' }
  ],
  confirmPassword: [
    {  message: 'Please confirm your password', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// Handle register form submission
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    const response = await registerAPI(registerForm)
    if (response.success) {
      ElMessage.success('Registration successful')
      router.push('/login-form')
    } else {
      ElMessage.error('Registration failed')
    }
  } catch (error) {
    console.error('Form validation failed:', error)
  }
}
</script>

<style scoped>
/* Container and Layout */
.register-container {
  height: 100dvh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  position: relative;
  overflow: hidden;
  overflow-y: auto;
}

.register-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(147, 51, 234, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.register-card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(148, 163, 184, 0.1);
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 1;
}

/* Header Section */
.header-section {
  text-align: center;
  margin-bottom: 2rem;
}


.logo-icon {
  width: 10rem;
  height:5rem;
  filter: drop-shadow(0 0 10px rgba(4, 108, 184, 0.3));
  }

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #f8fafc;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.form-subtitle {
  color: #94a3b8;
  font-size: 1rem;
  margin: 0;
  line-height: 1.5;
}

/* Form Styling */
.register-form {
  margin-top: 1.5rem;
}

.form-item {
  margin-bottom: 2rem;
}

.name-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.name-field {
  flex: 1;
  margin-bottom: 0;
}

/* Custom Input Styling */
:deep(.el-form-item__label) {
  color: #e2e8f0 !important;
  font-weight: 500;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  line-height: 1.25rem;
}

:deep(.el-input) {
  --el-input-bg-color: rgba(51, 65, 85, 0.5);
  --el-input-border-color: rgba(148, 163, 184, 0.2);
  --el-input-hover-border-color: rgba(59, 130, 246, 0.5);
  --el-input-focus-border-color: #3b82f6;
  --el-input-text-color: #f8fafc;
  --el-input-placeholder-color: #64748b;
}

:deep(.el-input__wrapper) {
  background-color: rgba(51, 65, 85, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  box-shadow: none;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.el-input.is-focus .el-input__wrapper) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

:deep(.el-input__inner) {
  color: #f8fafc;
  font-size: 0.875rem;
  height: 44px;
}

:deep(.el-input__inner::placeholder) {
  color: #64748b;
}

:deep(.el-input__prefix-inner) {
  color: #94a3b8;
}

:deep(.el-input__suffix-inner) {
  color: #94a3b8;
}

/* Submit Button */
.submit-section {
  margin: 2rem 0 1.5rem 0;
}

.register-btn {
  width: 100%;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.025em;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.register-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.register-btn:hover::before {
  left: 100%;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.register-btn:active {
  transform: translateY(0);
}

.btn-text {
  position: relative;
  z-index: 1;
}

/* Login Link Section */
.login-link-section {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.login-text {
  color: #94a3b8;
  font-size: 0.875rem;
}

.login-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.875rem;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #60a5fa;
  text-decoration: underline;
}

/* Error Message Styling */
:deep(.el-form-item__error) {
  color: #f87171 !important;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .register-container {
    padding: 1rem 0.5rem;
  }
  
  .register-card {
    padding: 2rem 1.5rem;
    border-radius: 16px;
    margin: 0;
  }
  
  .form-title {
    font-size: 1.5rem;
  }
  
  .name-field {
    margin-bottom: 1.5rem;
  }
}
/* Loading state */
:deep(.el-button.is-loading) {
  position: relative;
}

:deep(.el-button.is-loading .el-icon) {
  color: rgba(255, 255, 255, 0.8);
}
</style>
