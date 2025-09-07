<template>
  <div class="login-container">
    <!-- Desktop Layout -->
    <div class="container-fluid h-100 d-none p-0 d-md-flex">
      <div class="row w-100 h-100 p-0 m-0">
        <!-- Poster Section - 8 columns on desktop -->
        <div class="col-md-8 p-0 poster-section">
          <EarthGlobe />
        </div>
        
        <!-- Login Form Section - 4 columns on desktop -->
        <div class="col-md-4 d-flex align-items-center justify-content-center login-form-section">
          <div class="login-form-container w-100 px-4">
            <LoginForm />
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Layout - Flex Column Layout -->
    <div class="d-block d-md-none mobile-layout">
      <div class="mobile-flex-container">
        <!-- Mobile Poster Section - Takes up most of the space -->
        <div class="mobile-poster-section">
          <div class="poster-placeholder d-flex align-items-center justify-content-center h-100">
            <div class="text-center text-muted">
              <i class="el-icon-picture" style="font-size: 4rem;"></i>
              <h2 class="mt-4 mb-3">AI Trip</h2>
              <p class="poster-subtitle">智能旅行规划助手</p>
            </div>
          </div>
        </div>
        
        <!-- Mobile Button Section - Smaller area at bottom -->
        <div class="mobile-button-section">
          <div class="d-flex align-items-center justify-content-center h-100">
            <el-button 
              type="primary" 
              size="large"
              @click="goToMobileLogin"
              class="login-trigger-btn"
            >
              立即登录
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import LoginForm from '@/components/auth/LoginForm.vue'
import EarthGlobe from '@/components/auth/EarthGlobe.vue'

const router = useRouter()

/**
 * Navigate to mobile login form page
 */
const goToMobileLogin = () => {
  router.push('/mobile-login')
}
</script>

<style scoped>
.login-container {
  height: 100%;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
}


.poster-placeholder {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  color: white;
}

.login-form-section {
  backdrop-filter: blur(10px);
  background: linear-gradient(135deg, #8ea2a2 0%, #4d6871 50%, #243d4c 100%);
}

.login-form-container {
  max-width: 400px;
}

/* Mobile Styles */
.mobile-layout {
  height: 100dvh;
  background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
}

.mobile-flex-container {
  display: flex;
  flex-direction: column;
  height: 100dvh;
}

.mobile-poster-section {
  flex: 3; /* Takes 75% of the height (3/4) */
  position: relative;
}

.mobile-button-section {
  flex: 1; /* Takes 25% of the height (1/4) */
  backdrop-filter: blur(10px);
  padding: 1rem;
  min-height: 120px; /* Ensure minimum height for button area */
}

.mobile-poster-section .poster-placeholder {
  color: white;
  padding: 2rem;
}

.poster-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

.login-trigger-btn {
  border-radius: 25px;
  padding: 15px 40px;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: none;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  transition: all 0.3s ease;
  min-width: 200px;
}

.login-trigger-btn:hover {
  background: linear-gradient(45deg, #5a67d8 0%, #6b4c93 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}
</style>
