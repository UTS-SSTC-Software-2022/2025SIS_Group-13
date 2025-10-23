<template>
  <div class="travel-itinerary-result">
    <!-- Header Section -->
    <div class="result-header">
      <h2 class="result-title">Your Personalized Australian Adventure</h2>
      <p class="result-subtitle">AI-generated itinerary based on your preferences</p>
      <div class="trip-summary">
        <el-row :gutter="30">
          <el-col :span="6">
            <div class="summary-item">
              <el-icon class="summary-icon"><Calendar /></el-icon>
              <div>
                <div class="summary-label">Duration</div>
                <div class="summary-value">{{ itinerary.duration || '0 days' }}</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <el-icon class="summary-icon"><Location /></el-icon>
              <div>
                <div class="summary-label">Destination</div>
                <div class="summary-value">{{ itinerary.destination }}</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <el-icon class="summary-icon"><User /></el-icon>
              <div>
                <div class="summary-label">Travelers</div>
                <div class="summary-value">{{ itinerary.travelers }} people</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="summary-item">
              <el-icon class="summary-icon"><Money /></el-icon>
              <div>
                <div class="summary-label">Est. Budget</div>
                <div class="summary-value">${{ itinerary.estimatedBudget }}</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>


    <!-- Daily Itinerary Section -->
    <div class="daily-itinerary">
      <h3 class="section-title">Daily Itinerary</h3>
      <div class="itinerary-timeline">
        <div 
          v-for="(day, index) in itinerary.dailyPlans" 
          :key="index"
          class="day-card"
        >
          <!-- Day Header -->
          <div 
            class="day-header" 
            @click="toggleDayDetails(index)"
            :class="{ 'expanded': expandedDays.includes(index) }"
          >
            <div class="day-info">
              <div class="day-number">Day {{ index + 1 }}</div>
              <div class="day-date">{{ formatDate(day.date) }}</div>
              <div class="day-overview">{{ day.overview }}</div>
            </div>
            <div class="day-weather">
              <el-icon class="weather-icon" :class="getWeatherIconClass(day.weather.condition)">
                <component :is="getWeatherIcon(day.weather.condition)" />
              </el-icon>
              <div class="weather-info">
                <div class="temperature">{{ day.weather.temperature }}°C</div>
                <div class="condition">{{ day.weather.condition }}</div>
              </div>
            </div>
            <el-icon class="expand-icon" :class="{ 'rotated': expandedDays.includes(index) }">
              <ArrowDown />
            </el-icon>
          </div>

          <!-- Day Details (Expandable) -->
          <el-collapse-transition>
            <div v-show="expandedDays.includes(index)" class="day-details">
              <!-- Daily Route Map -->
              <DailyRouteMap :day-data="day" />
              
              <div class="activities-timeline">
                <div 
                  v-for="(activity, actIndex) in day.activities" 
                  :key="actIndex"
                  class="activity-item"
                >
                  <div class="activity-time">{{ activity.time }}</div>
                  <div class="activity-content">
                    <div class="activity-header">
                      <h4 class="activity-title">{{ activity.title }}</h4>
                      <el-tag :type="getActivityTypeColor(activity.type)" size="small">
                        {{ activity.type }}
                      </el-tag>
                    </div>
                    <p class="activity-description">{{ activity.description }}</p>
                    
                    <!-- Location Info -->
                    <div v-if="activity.location" class="activity-location">
                      <el-icon><Location /></el-icon>
                      <span>{{ activity.location.name }}</span>
                      <span class="address">{{ activity.location.address }}</span>
                    </div>

                    <!-- Transportation -->
                    <div v-if="activity.transportation" class="activity-transport">
                      <el-icon><Position /></el-icon>
                      <span>{{ activity.transportation.method }}</span>
                      <span class="duration">({{ activity.transportation.duration }})</span>
                      <span v-if="activity.transportation.cost" class="cost">
                        - ${{ activity.transportation.cost }}
                      </span>
                    </div>

                    <!-- Tips -->
                    <div v-if="activity.tips && activity.tips.length > 0" class="activity-tips">
                      <h5>💡 Tips:</h5>
                      <ul>
                        <li v-for="(tip, tipIndex) in activity.tips" :key="tipIndex">
                          {{ tip }}
                        </li>
                      </ul>
                    </div>

                    <!-- Estimated Cost -->
                    <div v-if="activity.estimatedCost" class="activity-cost">
                      <el-icon><Money /></el-icon>
                      <span>Estimated cost: ${{ activity.estimatedCost }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Day Summary -->
              <div class="day-summary">
                <h4 class="summary-title">📊 Day Summary</h4>
                <div class="summary-stats">
                  <div class="stat-item">
                    <div class="stat-icon">🎯</div>
                    <div>
                      <span class="stat-label">Total Activities</span>
                      <span class="stat-value">{{ day.activities.length }}</span>
                    </div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-icon">🚶</div>
                    <div>
                      <span class="stat-label">Estimated Walking</span>
                      <span class="stat-value">{{ day.estimatedWalking }}</span>
                    </div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-icon">💰</div>
                    <div>
                      <span class="stat-label">Daily Budget</span>
                      <span class="stat-value">${{ day.dailyBudget }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-collapse-transition>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <!-- Save按钮：将Temporary状态改为Generated -->
      <el-button 
        v-if="currentItineraryId && itineraryStatus === 'Temporary' && !isFromSaved"
        type="primary" 
        size="large" 
        @click="saveItinerary"
      >
        <el-icon><Check /></el-icon>
        Save to Generated Plan
      </el-button>
      
      <!-- Complete按钮：将Generated状态改为Completed -->
      <el-button 
        v-if="currentItineraryId && itineraryStatus === 'Generated'"
        type="success" 
        size="large" 
        @click="completeItinerary"
      >
        <el-icon><Star /></el-icon>
        Complete
      </el-button>
      
      <!-- 状态显示按钮（已保存或已完成时显示） -->
      <el-button 
        v-if="currentItineraryId && itineraryStatus === 'Generated' && isFromSaved"
        type="info" 
        size="large" 
        disabled
      >
        <el-icon><Check /></el-icon>
        In Generated Plan
      </el-button>
      
      <el-button 
        v-if="currentItineraryId && itineraryStatus === 'Completed'"
        type="success" 
        size="large" 
        disabled
      >
        <el-icon><Star /></el-icon>
        Completed
      </el-button>
      
      <!-- Share按钮 -->
      <el-button type="default" size="large" @click="shareItinerary">
        <el-icon><Share /></el-icon>
        Share
      </el-button>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted, watch} from 'vue'
import { ElMessage } from 'element-plus'
import DailyRouteMap from '@/components/map/DailyRouteMap.vue'
import {
  Calendar,
  Location,
  User,
  Money,
  ArrowDown,
  Position,
  Download,
  Share,
  Sunny,
  Cloudy,
  Check,
  Star
} from '@element-plus/icons-vue'

// Props
const props = defineProps({
  itineraryData: {
    type: Object,
    default: null
  },
  currentItineraryId: {
    type: [String, Number],
    default: null
  },
  itineraryStatus: {
    type: String,
    default: 'Temporary'
  },
  isFromSaved: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['download', 'share', 'save', 'complete'])

// Reactive data
const expandedDays = ref([])
const loading = ref(false)

const itinerary = reactive({
  destination: '',
  duration: 0,
  travelers: 0,
  estimatedBudget: 0,
  dailyPlans: []
})

// Watch for props changes and fully replace reactive object
watch(
  () => props.itineraryData,
  (newData) => {
    if (newData) {
      // 用 JSON 深拷贝，确保 reactive 完全更新
      const copy = JSON.parse(JSON.stringify(newData))
      itinerary.destination = copy.destination || ''
      itinerary.duration = copy.duration || 0
      itinerary.travelers = copy.travelers || 0
      itinerary.estimatedBudget = copy.estimatedBudget || 0
      itinerary.dailyPlans = copy.dailyPlans || []
    }
  },
  { immediate: true }
)

// Toggle day details
const toggleDayDetails = (dayIndex) => {
  const index = expandedDays.value.indexOf(dayIndex)
  if (index > -1) {
    expandedDays.value.splice(index, 1)
  } else {
    expandedDays.value.push(dayIndex)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-AU', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getWeatherIcon = (condition) => {
  const iconMap = {
    'Sunny': Sunny,
    'Partly Cloudy': Cloudy,
    'Cloudy': Cloudy,
    'Rainy': Cloudy,
    'Drizzle': Cloudy
  }
  return iconMap[condition] || Sunny
}

const getWeatherIconClass = (condition) => {
  const classMap = {
    'Sunny': 'weather-sunny',
    'Partly Cloudy': 'weather-cloudy',
    'Cloudy': 'weather-cloudy',
    'Rainy': 'weather-rainy',
    'Drizzle': 'weather-drizzle'
  }
  return classMap[condition] || 'weather-sunny'
}

const getActivityTypeColor = (type) => {
  const colorMap = {
    'Adventure': 'danger',
    'Culture': 'primary',
    'Dining': 'success',
    'Nature': 'info',
    'Shopping': 'warning'
  }
  return colorMap[type] || 'default'
}

const saveItinerary = () => {
  emit('save')
}

const completeItinerary = () => {
  emit('complete')
}

const shareItinerary = () => {
  emit('share')
}

</script>

<style scoped>
.travel-itinerary-result {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 3rem;
}

/* Header Styles */
.result-header {
  text-align: center;
  margin-bottom: 3rem;
}

.result-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #e6edf3;
  margin-bottom: 0.5rem;
}

.result-subtitle {
  font-size: 1.1rem;
  color: #a0aec0;
  margin-bottom: 2rem;
}

.trip-summary {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 20px;
  padding: 2.5rem;
  color: #e5e7eb;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.28);
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(10px);
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.summary-item:hover {
  background: rgba(255, 255, 255, 0.09);
  transform: translateY(-2px);
}

.summary-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.summary-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.summary-value {
  font-size: 1.2rem;
  font-weight: 600;
}

/* Daily Itinerary Styles */
.section-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 1.5rem;
  text-align: center;
}

.day-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22);
  margin-bottom: 2rem;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(148, 163, 184, 0.18);
}

.day-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.day-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 2.5rem;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.04);
  transition: all 0.3s ease;
  min-height: 120px;
}

.day-header:hover {
  background: rgba(255, 255, 255, 0.08);
}

.day-header.expanded {
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.28) 0%, rgba(64, 158, 255, 0.22) 100%);
  color: #e6edf3;
}

.day-info {
  flex: 1;
}

.day-number {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #e6edf3;
}

.day-date {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
  color: #a0aec0;
}

.day-overview {
  font-size: 1rem;
  font-weight: 500;
  color: #e6edf3;
}

.day-weather {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-right: 1rem;
}

.weather-icon {
  font-size: 2rem;
}

.weather-sunny {
  color: #f39c12;
}

.weather-cloudy {
  color: #95a5a6;
}

.weather-rainy {
  color: #3498db;
}

.temperature {
  font-size: 1.1rem;
  font-weight: 600;
}

.condition {
  font-size: 0.85rem;
  opacity: 0.8;
}

.expand-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

/* Day Details Styles */
.day-details {
  padding: 0 2.5rem 2rem;
  background: rgba(255, 255, 255, 0.03);
}

/* Route Map Integration */
.day-details .route-map-container {
  margin-bottom: 2rem;
}

.activities-timeline {
  position: relative;
  padding-left: 3rem;
  margin-top: 1rem;
}

.activities-timeline::before {
  content: '';
  position: absolute;
  left: 0.75rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, #409eff, #66b1ff);
}

.activity-item {
  position: relative;
  display: flex;
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
  gap: 2rem;
}

.activity-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.activity-item::before {
  content: '';
  position: absolute;
  left: -2.25rem;
  top: 0.25rem;
  width: 12px;
  height: 12px;
  background: #409eff;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-time {
  min-width: 100px;
  font-weight: 700;
  color: #409eff;
  font-size: 1rem;
  background: rgba(64, 158, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 12px;
  text-align: center;
  height: fit-content;
}

.activity-content {
  flex: 1;
  margin-left: 0;
}

.activity-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.activity-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.activity-description {
  color: #a0aec0;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.activity-location,
.activity-transport,
.activity-cost {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #a0aec0;
}

.address,
.duration,
.cost {
  opacity: 0.8;
}

.activity-tips {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.activity-tips h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #e6edf3;
}

.activity-tips ul {
  margin: 0;
  padding-left: 1.2rem;
}

.activity-tips li {
  font-size: 0.85rem;
  color: #a0aec0;
  margin-bottom: 0.25rem;
}

/* Day Summary Styles */
.day-summary {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  padding: 2rem;
  margin-top: 2rem;
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
  backdrop-filter: blur(8px);
}

.summary-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6edf3;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(64, 158, 255, 0.05);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: rgba(64, 158, 255, 0.1);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-label {
  display: block;
  font-size: 0.85rem;
  color: #a0aec0;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 700;
  color: #e6edf3;
  font-size: 1.1rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 4rem;
  padding: 2.5rem 0;
  border-top: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(255, 255, 255, 0.04);
  border-radius: 20px;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.22);
  backdrop-filter: blur(8px);
}

/* Dark theme buttons inside action section */
:deep(.action-buttons .el-button) {
  color: #e6edf3;
}
:deep(.action-buttons .el-button--default) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(148, 163, 184, 0.18);
}
:deep(.action-buttons .el-button--default:hover) {
  background: rgba(255, 255, 255, 0.12);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .travel-itinerary-result {
    padding: 1rem;
  }
  
  .result-title {
    font-size: 2rem;
  }
  
  .trip-summary {
    padding: 1.5rem;
  }
  
  .summary-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .day-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .day-weather {
    margin-right: 0;
  }
  
  /* Route Map mobile styles */
  .day-details .route-map-container {
    margin-bottom: 1.5rem;
  }
  
  .activity-item {
    flex-direction: column;
  }
  
  .activity-content {
    margin-left: 0;
    margin-top: 0.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>