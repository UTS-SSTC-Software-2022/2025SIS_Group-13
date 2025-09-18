<template>
  <div class="forgot-password-container d-flex align-items-center justify-content-center min-vh-100">
    <div class="forgot-password-card">
      <div class="text-center mb-4">
        <h2 class="form-title">Reset Password</h2>
        <p class="form-subtitle text-muted">Please enter your email address, we will send a reset link to you</p>
      </div>

      <el-form
        ref="forgotPasswordFormRef"
        :model="forgotPasswordForm"
        :rules="forgotPasswordRules"
        label-position="top"
        size="large"
      >
        <el-form-item label="Email Address" prop="email">
          <el-input
            v-model="forgotPasswordForm.email"
            type="email"
            placeholder="Please enter your email address"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="w-100" size="large">
            Send Reset Link
          </el-button>
        </el-form-item>

        <div class="text-center">
          <span class="text-muted">Remember your password?</span>
          <router-link to="/" class="login-link ms-1">
            Back to Login
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const forgotPasswordFormRef = ref()

const forgotPasswordForm = reactive({
  email: ''
})

const forgotPasswordRules = {
  email: [
    { required: true, message: 'Please enter your email address', trigger: 'blur' },
    { type: 'email', message: 'Please enter a valid email address', trigger: 'blur' }
  ]
}
</script>

<style scoped>
.forgot-password-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.forgot-password-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 1rem;
}

.form-title {
  color: #303133;
  font-weight: 600;
}

.login-link {
  color: #409eff;
  text-decoration: none;
  font-weight: 500;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
