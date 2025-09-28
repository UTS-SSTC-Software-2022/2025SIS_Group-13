<template>
  <div class="travel-plan-page">
    <div class="container-fluid h-100">
      <div class="row h-100">
        <div class="col-12 d-flex align-items-center justify-content-center">
          <div class="travel-plan-wrapper">
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
            <TravelPlanForm @submit="handleFormSubmit" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import TravelPlanForm from '@/components/travel/TravelPlanForm.vue'

const router = useRouter()

/**
 * Go back to previous page
 */
const goBack = () => {
  router.go(-1)
}

/**
 * Handle form submission
 * @param {Object} formData - The travel plan form data
 */
const handleFormSubmit = async (formData) => {
  try {
    console.log('Travel plan data:', formData)

    ElMessage.info('Generating your personalized Australian adventure...')

    // 调用 Django API
    const response = await axios.post('http://localhost:8080/api/ai/generate/', formData)

    const output = response.data.output
    console.log('LLM_API output:', output)

    ElMessage.success('Itinerary generated successfully!')

    // 跳转到结果页面，同时可以传输出内容
    router.push({
      path: '/travel/itinerary-result',
      query: {
        result: encodeURIComponent(JSON.stringify(output))
      }
    })

  } catch (error) {
    console.error('Generate travel plan error:', error)
    ElMessage.error('Failed to generate itinerary, please try again')
  }
}
</script>

<style scoped>
.travel-plan-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.travel-plan-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
  margin: 2rem;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.back-button-container {
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 10;
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

/* Custom scrollbar for the wrapper */
.travel-plan-wrapper::-webkit-scrollbar {
  width: 6px;
}

.travel-plan-wrapper::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.travel-plan-wrapper::-webkit-scrollbar-thumb {
  background: rgba(64, 158, 255, 0.3);
  border-radius: 3px;
}

.travel-plan-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(64, 158, 255, 0.5);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .travel-plan-page {
    padding: 1rem 0;
  }
  
  .travel-plan-wrapper {
    margin: 1rem;
    padding: 2rem 1.5rem;
    max-height: 95vh;
  }
  
  .back-button-container {
    top: 0.5rem;
    left: 0.5rem;
  }
}

@media (max-width: 576px) {
  .travel-plan-wrapper {
    margin: 0.5rem;
    padding: 1.5rem 1rem;
  }
}
</style>