<template>
  <div class="login-container">
    <!-- Login Button in top right corner -->
    <div class="login-header">
      <img src="@/assets/images/LeisurA logo.svg" alt="LeisurA Logo" class="logo" />
      <el-button type="primary" size="large" class="top-login-btn" @click="goToLoginForm">
        Login
      </el-button>
    </div>

    <!-- Full Screen Earth Globe -->
    <div class="full-screen-globe">
      <EarthGlobe />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import EarthGlobe from '@/components/auth/EarthGlobe.vue'

const router = useRouter()

/**
 * Navigate to login form page
 */
const goToLoginForm = () => {
  router.push('/login-form')
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.login-header {
  position: absolute;
  top: 1rem;
  width: 100%;
  display: flex;
  padding: 0 2rem;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
}

.logo {
  width: 10rem;
  height:5rem;
  filter: drop-shadow(0 0 10px rgba(4, 108, 184, 0.3));
}

.top-login-btn {
  border-radius: 25px;
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border: none;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.top-login-btn:hover {
  background: linear-gradient(45deg, #5a67d8 0%, #6b4c93 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.full-screen-globe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .login-button-container {
    top: 1rem;
    right: 1rem;
  }
  
  .top-login-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
}
</style>
