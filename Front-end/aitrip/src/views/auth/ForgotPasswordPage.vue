<template>
  <div class="forgot-password-container d-flex align-items-center justify-content-center min-vh-100">
    <div class="forgot-password-card">
      <div class="text-center mb-4">
        <h2 class="form-title">重置密码</h2>
        <p class="form-subtitle text-muted">请输入您的邮箱地址，我们将发送重置链接给您</p>
      </div>

      <el-form
        ref="forgotPasswordFormRef"
        :model="forgotPasswordForm"
        :rules="forgotPasswordRules"
        label-position="top"
        size="large"
      >
        <el-form-item label="邮箱地址" prop="email">
          <el-input
            v-model="forgotPasswordForm.email"
            type="email"
            placeholder="请输入您的邮箱地址"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="w-100" size="large">
            发送重置链接
          </el-button>
        </el-form-item>

        <div class="text-center">
          <span class="text-muted">想起密码了？</span>
          <router-link to="/" class="login-link ms-1">
            返回登录
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
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
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
