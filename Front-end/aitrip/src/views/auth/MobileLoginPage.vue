<template>
  <div class="mobile-login-container">
    <!-- Header with back button -->
    <div class="mobile-login-header">
      <el-button 
        type="text" 
        class="back-btn"
        @click="router.back()"
      >
        <i class="el-icon-arrow-left"></i>
        返回
      </el-button>
    </div>

    <!-- Login Form Content -->
    <div class="mobile-login-content">
      <div class="login-form-wrapper">
        <LoginForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()

</script>

<style scoped>
.mobile-login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
}

.mobile-login-header {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.back-btn {
  color: white;
  font-size: 16px;
  font-weight: 500;
}

.back-btn:hover {
  color: rgba(255, 255, 255, 0.8);
}

.mobile-login-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-form-wrapper {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
}

/* Ensure form looks good on mobile */
@media (max-width: 576px) {
  .login-form-wrapper {
    margin: 0.5rem;
    padding: 1.5rem;
  }
}
</style>
