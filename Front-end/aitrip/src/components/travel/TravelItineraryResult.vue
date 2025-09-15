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
                <div class="summary-value">{{ itinerary.duration }} days</div>
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
      <el-button type="primary" size="large" @click="downloadItinerary">
        <el-icon><Download /></el-icon>
        Download Itinerary
      </el-button>
      <el-button type="default" size="large" @click="shareItinerary">
        <el-icon><Share /></el-icon>
        Share
      </el-button>
      <el-button type="success" size="large" @click="saveItinerary">
        <el-icon><Star /></el-icon>
        Save to Favorites
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Calendar,
  Location,
  User,
  Money,
  ArrowDown,
  Position,
  Download,
  Share,
  Star,
  Sunny,
  Cloudy
} from '@element-plus/icons-vue'

// Props
const props = defineProps({
  itineraryData: {
    type: Object,
    default: null
  }
})

// Reactive data
const expandedDays = ref([])
const loading = ref(false)

// Sample itinerary data (will be replaced by API call)
const itinerary = reactive({
  destination: 'Sydney, NSW',
  duration: 5,
  travelers: 2,
  estimatedBudget: 2500,
  dailyPlans: [
    {
      date: '2024-03-15',
      overview: 'Explore Sydney CBD and Harbour Bridge',
      weather: {
        condition: 'Sunny',
        temperature: 24
      },
      activities: [
        {
          time: '09:00',
          title: 'Sydney Harbour Bridge Climb',
          type: 'Adventure',
          description: 'Experience breathtaking 360-degree views of Sydney from the top of the iconic Harbour Bridge.',
          location: {
            name: 'Sydney Harbour Bridge',
            address: '5 Cumberland St, The Rocks NSW 2000'
          },
          transportation: {
            method: 'Walk from hotel',
            duration: '15 minutes'
          },
          estimatedCost: 174,
          tips: [
            'Book in advance for better rates',
            'Wear comfortable shoes and clothes',
            'Bring a camera for stunning photos'
          ]
        },
        {
          time: '13:00',
          title: 'Lunch at The Rocks',
          type: 'Dining',
          description: 'Enjoy fresh seafood and local Australian cuisine at one of The Rocks historic restaurants.',
          location: {
            name: 'The Rocks Markets',
            address: 'Jack Mundey Pl, The Rocks NSW 2000'
          },
          transportation: {
            method: 'Walk',
            duration: '5 minutes'
          },
          estimatedCost: 45,
          tips: [
            'Try the famous meat pies',
            'Weekend markets have more food options'
          ]
        },
        {
          time: '15:30',
          title: 'Sydney Opera House Tour',
          type: 'Culture',
          description: 'Take a guided tour inside the world-famous Sydney Opera House and learn about its fascinating architecture.',
          location: {
            name: 'Sydney Opera House',
            address: 'Bennelong Point, Sydney NSW 2000'
          },
          transportation: {
            method: 'Ferry from Circular Quay',
            duration: '10 minutes',
            cost: 8
          },
          estimatedCost: 43,
          tips: [
            'Book the 1-hour guided tour',
            'Check for evening performance schedules'
          ]
        }
      ],
      estimatedWalking: '3.2 km',
      dailyBudget: 270
    },
    {
      date: '2024-03-16',
      overview: 'Bondi Beach and Coastal Walk',
      weather: {
        condition: 'Partly Cloudy',
        temperature: 22
      },
      activities: [
        {
          time: '08:30',
          title: 'Bondi to Coogee Coastal Walk',
          type: 'Nature',
          description: 'Scenic 6km coastal walk featuring stunning ocean views, beaches, and clifftop paths.',
          location: {
            name: 'Bondi Beach',
            address: 'Bondi Beach NSW 2026'
          },
          transportation: {
            method: 'Bus from city',
            duration: '45 minutes',
            cost: 4
          },
          estimatedCost: 0,
          tips: [
            'Start early to avoid crowds',
            'Bring water and sunscreen',
            'Wear comfortable walking shoes'
          ]
        },
        {
          time: '12:00',
          title: 'Lunch at Coogee Beach',
          type: 'Dining',
          description: 'Relax and enjoy fresh seafood with ocean views at Coogee Beach.',
          location: {
            name: 'Coogee Pavilion',
            address: '169 Dolphin St, Coogee NSW 2034'
          },
          estimatedCost: 38,
          tips: [
            'Try the fish and chips',
            'Great spot for people watching'
          ]
        }
      ],
      estimatedWalking: '6.5 km',
      dailyBudget: 80
    }
  ]
})

// Methods
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

const downloadItinerary = () => {
  ElMessage.success('Itinerary download started!')
  // TODO: Implement PDF download functionality
}

const shareItinerary = () => {
  ElMessage.info('Share functionality coming soon!')
  // TODO: Implement share functionality
}

const saveItinerary = () => {
  ElMessage.success('Itinerary saved to favorites!')
  // TODO: Implement save to user favorites
}

// Lifecycle
onMounted(() => {
  // TODO: Replace with actual API call
  // if (props.itineraryData) {
  //   Object.assign(itinerary, props.itineraryData)
  // } else {
  //   fetchItineraryFromAPI()
  // }
})

// TODO: API call function
const fetchItineraryFromAPI = async () => {
  try {
    loading.value = true
    // const response = await fetch('/api/travel/itinerary/generate', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify(travelFormData)
    // })
    // const data = await response.json()
    // Object.assign(itinerary, data)
  } catch (error) {
    console.error('Failed to fetch itinerary:', error)
    ElMessage.error('Failed to load itinerary')
  } finally {
    loading.value = false
  }
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
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.result-subtitle {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.trip-summary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 2.5rem;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.summary-item:hover {
  background: rgba(255, 255, 255, 0.2);
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
  color: #2c3e50;
  margin-bottom: 1.5rem;
  text-align: center;
}

.day-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
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
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transition: all 0.3s ease;
  min-height: 120px;
}

.day-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.day-header.expanded {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.day-info {
  flex: 1;
}

.day-number {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.day-date {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 0.5rem;
}

.day-overview {
  font-size: 1rem;
  font-weight: 500;
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
  background: #fafbfc;
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
  color: #2c3e50;
  margin: 0;
}

.activity-description {
  color: #5a6c7d;
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
  color: #6c757d;
}

.address,
.duration,
.cost {
  opacity: 0.8;
}

.activity-tips {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.activity-tips h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #495057;
}

.activity-tips ul {
  margin: 0;
  padding-left: 1.2rem;
}

.activity-tips li {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

/* Day Summary Styles */
.day-summary {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 16px;
  padding: 2rem;
  margin-top: 2rem;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.summary-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
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
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-weight: 700;
  color: #2c3e50;
  font-size: 1.1rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 4rem;
  padding: 2.5rem 0;
  border-top: 2px solid #f0f2f5;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 20px;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
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