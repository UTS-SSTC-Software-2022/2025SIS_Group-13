<template>
  <div class="auth-shell">
    <!-- 背景：与注册页一致 -->
    <div class="auth-bg"></div>

    <!-- 磨砂卡片 -->
    <div class="auth-card">
      <!-- 顶部返回 -->
      <el-page-header
        class="page-header"
        @back="$router.push('/login-form')"
        title="Back"
      />

      <!-- 这里保留原页面的标题和灰色提示，格式与布局保持不变（居中） -->
      <div class="head">
        <h1 class="title">Reset Password</h1>
        <p class="subtitle">
          Please enter your email address, we will<br />
          send a reset link to you
        </p>
      </div>

      <!-- 表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="form"
      >
        <el-form-item label=" Email Address" prop="email">
          <el-input
            v-model="form.email"
            placeholder="Please enter your email address"
            clearable
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="btn-primary"
          @click="onSubmit"
        >
          Send Reset Link
        </el-button>

        <div class="footnote">
          <span>Remember your password? </span>
          <el-link type="primary" @click="$router.push('/login-form')">
            Back to Login
          </el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

const formRef = ref()
const form = reactive({
  email: ''
})

const rules = {
  email: [
    { required: true, message: 'Email is required', trigger: 'blur' },
    { type: 'email', message: 'Please input valid email', trigger: ['blur', 'change'] }
  ]
}

const onSubmit = () => {
  formRef.value?.validate((valid) => {
    if (!valid) return
    // TODO: 调用你们后端接口发送重置邮件
    ElMessage.success('If this email exists, a reset link has been sent.')
  })
}
</script>

<style scoped>
/* ===== 页面骨架（与注册页一致） ===== */
.auth-shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 深色渐变背景（可与注册页保持一致） */
.auth-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(1200px 600px at 10% -10%, #1e293b, transparent 60%),
    radial-gradient(1200px 600px at 110% 110%, #1f144a, transparent 60%),
    linear-gradient(135deg, #0b1220, #1a1f2b 40%, #141c2f 70%, #0b1220);
}

/* 磨砂玻璃卡片容器 */
.auth-card {
  position: relative;
  width: min(880px, 92%);
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px) saturate(1.3);
  -webkit-backdrop-filter: blur(16px) saturate(1.3);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
  padding: 28px 24px 34px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
  color: #e6edf3;
}

.page-header {
  max-width: 1100px;
  margin: 0 auto 8px;
}

/* 保留原页面的标题与副标题样式（居中、灰色提示） */
.head {
  text-align: center;
  margin: 6px auto 18px;
}
.title {
  margin: 0;
  font-weight: 700;
  font-size: 36px;
  line-height: 1.25;
  color: #e6edf3; /* 亮色标题 */
}
.subtitle {
  margin: 8px 0 0;
  font-size: 16px;
  line-height: 1.6;
  color: #a0aec0; /* 灰色提示，接近原效果 */
  opacity: 0.95;
}

.form {
  max-width: 720px;
  margin: 12px auto 0;
}

/* 主按钮（与注册页一致的蓝紫渐变） */
.btn-primary {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.2px;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  border: none;
}
.btn-primary:hover {
  filter: brightness(1.06);
}

.footnote {
  margin-top: 14px;
  text-align: center;
  opacity: 0.92;
}

/* 暗色模式下卡片（如果项目有 .dark 切换） */
:root.dark .auth-card {
  background: rgba(17, 24, 39, 0.6);
  border-color: rgba(148, 163, 184, 0.2);
}
</style>
