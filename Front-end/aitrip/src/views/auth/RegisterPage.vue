<template>
  <div class="register-container d-flex align-items-center justify-content-center min-vh-100">
    <div class="register-card">
      <div class="text-center mb-4">
        <h2 class="form-title">创建账户</h2>
        <p class="form-subtitle text-muted">加入我们，开始您的智能旅行之旅</p>
      </div>

      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-position="top"
        size="large"
      >
        <el-form-item label="邮箱地址" prop="email">
          <el-input
            v-model="registerForm.email"
            type="email"
            placeholder="请输入您的邮箱地址"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="w-100" size="large">
            注册
          </el-button>
        </el-form-item>

        <div class="text-center">
          <span class="text-muted">已有账户？</span>
          <router-link to="/" class="login-link ms-1">
            立即登录
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const registerFormRef = ref()

const registerForm = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}
</script>

<style scoped>
.register-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
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
