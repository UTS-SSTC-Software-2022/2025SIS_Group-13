<template>
  <div class="travel-plan-page">
    
    <div class="container-fluid h-100">
      <div class="row h-100">
        <!-- Desktop layout: Left form, Right map -->
        <div class="col-lg-6 col-md-12 d-flex align-items-center justify-content-center desktop-form-section">
          <div class="travel-plan-wrapper">
            <TravelPlanForm @submit="handleFormSubmit" />
          </div>
        </div>
        
        <!-- Desktop map section (hidden on mobile) -->
        <div class="col-lg-6 d-none d-lg-block desktop-map-section">
          <div class="map-placeholder">
            <div class="map-content">
              <el-icon class="map-icon"><Location /></el-icon>
              <h3>Interactive Map</h3>
              <p>Map will be displayed here</p>
            </div>
          </div>
        </div>
        
        <!-- Mobile layout: Only form -->
        <div class="col-12 d-lg-none mobile-form-section">
          <div class="travel-plan-wrapper">
            <TravelPlanForm @submit="handleFormSubmit" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowLeft, Location } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import TravelPlanForm from '@/components/travel/TravelPlanForm.vue'

const router = useRouter()

/**
 * Go back to home page
 */
const goBack = () => {
  router.push('/home')
}

/**
 * Handle form submission
 * @param {Object} formData - The travel plan form data
 */
const handleFormSubmit = async (formData) => {
  try {
    console.log('Travel plan data (will be forwarded to results page):', formData)

    // Inform user and navigate to result page; result page will call /generate.
    ElMessage.info('Opening itinerary results...')

    await router.push({
      path: '/travel/itinerary-result',
      query: {
        result: encodeURIComponent(JSON.stringify(output))
      }
    })
  } catch (error) {
    console.error('Failed to navigate to results page:', error)
    ElMessage.error('Failed to open itinerary results, please try again')
  }
}
</script>

<style scoped>
.travel-plan-page {
  min-height: 100vh;
}
/* Desktop layout styles */

.travel-plan-wrapper {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

/* Desktop specific styles - no padding, no border radius */
@media (min-width: 992px) {
  .desktop-form-section {
    padding: 0;
  }
  
  .desktop-map-section {
    padding: 0;
  }
  
  .desktop-form-section .travel-plan-wrapper {
    border-radius: 0;
    box-shadow: none;
    background: rgba(255, 255, 255, 1);
    padding: 2rem;
    height: 100vh;
    max-height: 100vh;
  }
  
  .map-placeholder {
    border-radius: 0;
    box-shadow: none;
    background: rgba(248, 249, 250, 1);
    height: 100vh;
    min-height: 100vh;
  }
}

/* Map placeholder styles */
.map-placeholder {
  height: 100%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
}

.map-content {
  text-align: center;
  color: #666;
}

.map-icon {
  font-size: 4rem;
  color: #409eff;
  margin-bottom: 1rem;
}

.map-content h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

.map-content p {
  margin: 0;
  font-size: 0.9rem;
}

/* Mobile layout styles */
.mobile-form-section {
  padding: 1rem;
}

.mobile-form-section .travel-plan-wrapper {
  margin: 0;
  padding: 2rem 1.5rem;
  max-height: 95vh;
  /* Keep original mobile styles */
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
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

/* Responsive adjustments */
@media (max-width: 992px) {
  .desktop-form-section {
    padding: 1rem;
  }
}

@media (max-width: 576px) {
  .mobile-form-section .travel-plan-wrapper {
    padding: 1.5rem 1rem;
  }
  
  .back-button-container {
    top: 0.5rem;
    left: 0.5rem;
  }
}
</style>