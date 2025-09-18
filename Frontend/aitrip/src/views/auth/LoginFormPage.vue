<template>
  <div class="login-form-page">
    <div class="container-fluid h-100">
      <div class="row h-100">
        <div class="col-12 d-flex align-items-center justify-content-center">
          <div class="login-form-wrapper">
            <div class="back-button-container">
              <el-button 
                type="info" 
                plain 
                size="small"
                @click="goBack"
                class="back-btn"
              >
                <el-icon class="me-1"><ArrowLeft /></el-icon>
                Back
              </el-button>
            </div>
            <LoginForm />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import LoginForm from '@/components/auth/LoginForm.vue'

const router = useRouter()

/**
 * Go back to previous page
 */
const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.login-form-page {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 450px;
  width: 100%;
  margin: 2rem;
  position: relative;
}

.back-button-container {
  position: absolute;
  top: 1rem;
  left: 1rem;
}

.back-btn {
  border-radius: 20px;
  border-color: #dcdfe6;
  color: #606266;
  background: rgba(255, 255, 255, 0.8);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #c0c4cc;
  color: #409eff;
}

/* Mobile responsive */
@media (max-width: 576px) {
  .login-form-wrapper {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
  
  .back-button-container {
    top: 0.5rem;
    left: 0.5rem;
  }
}
</style>
