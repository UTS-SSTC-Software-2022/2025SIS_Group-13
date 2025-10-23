<template>
  <!-- 背景渐变层：与规划页一致的深色渐变 -->
  <div class="auth-bg"></div>

  <el-container class="layout-container" direction="vertical">
    <el-container class="bottom-container">
      <!-- 左侧侧边栏导航（与整体设计保持一致） -->
      <el-aside class="sidebar" width="200px">
        <el-menu
          mode="vertical"
          class="sidebar-menu"
          :default-active="'itinerary'"
          background-color="#0f0f0f"
          text-color="#e5e7eb"
          active-text-color="#1890ff"
        >
          <el-menu-item index="home" @click="go('/home')">
            <el-icon><House /></el-icon>
            <span>Home</span>
          </el-menu-item>
          <el-menu-item index="plan" @click="go('/travel/plan')">
            <el-icon><MapLocation /></el-icon>
            <span>Plan Trip</span>
          </el-menu-item>
          <el-menu-item index="itinerary" @click="go('/travel/itinerary-result')">
            <el-icon><MapLocation /></el-icon>
            <span>Itinerary</span>
          </el-menu-item>
          <el-menu-item index="profile" @click="go('/profile')">
            <el-icon><User /></el-icon>
            <span>Profile</span>
          </el-menu-item>
          <el-menu-item index="logout" @click="go('/login-form')">
            <el-icon><SwitchButton /></el-icon>
            <span>Logout</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区：与规划页一致的结构与色彩 -->
      <el-main class="home-main">
        <el-page-header
          class="page-header"
          @back="goBack"
          title="< Back"
          content="Your Personalized Travel Itinerary"
        />

        <div class="page-actions">
          <el-button
            type="primary"
            @click="regenerateItinerary"
            :loading="regenerating"
          >
            <el-icon><Refresh /></el-icon>
            Regenerate
          </el-button>
          <el-button
            type="success"
            @click="modifyPreferences"
          >
            <el-icon><Edit /></el-icon>
            Modify Preferences
          </el-button>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="8" animated />
          <div class="loading-text">
            <h3>🤖 AI is crafting your perfect Australian adventure...</h3>
            <p>This may take a few moments while we analyze your preferences and create a personalized itinerary.</p>
          </div>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="error-container">
          <el-result
            icon="error"
            title="Failed to Generate Itinerary"
            :sub-title="error"
          >
            <template #extra>
              <el-button type="primary" @click="retryGeneration">
                Try Again
              </el-button>
              <el-button type="success" @click="useMockData">
                <el-icon><View /></el-icon>
                Use Mock Data for Testing
              </el-button>
              <el-button @click="goBack">
                Back to Home
              </el-button>
            </template>
          </el-result>
        </div>

        <!-- 成功状态：显示行程结果 -->
        <div v-else-if="itineraryData" class="itinerary-container">
          <div class="generation-info">
            <el-alert
              title="✨ Your itinerary has been generated!"
              type="success"
              :description="`Generated on ${formatGenerationTime()} using AI analysis of your preferences.`"
              show-icon
              :closable="false"
            />
          </div>

          <TravelItineraryResult
            :itinerary-data="itineraryData"
            @download="handleDownload"
            @share="handleShare"
          />

          <!-- 反馈区块（深色卡片） -->
          <div class="feedback-section">
            <el-card class="feedback-card">
              <template #header>
                <div class="feedback-header">
                  <h3>How was this itinerary?</h3>
                  <p>Your feedback helps us improve our AI recommendations</p>
                </div>
              </template>

              <div class="feedback-content">
                <div class="rating-section">
                  <span class="rating-label">Overall Rating:</span>
                  <el-rate
                    v-model="feedback.rating"
                    :colors="['#F7BA2A', '#F7BA2A', '#F7BA2A']"
                    show-text
                  />
                </div>

                <el-input
                  v-model="feedback.comment"
                  type="textarea"
                  :rows="3"
                  placeholder="Tell us what you liked or what could be improved..."
                  maxlength="500"
                  show-word-limit
                />

                <div class="feedback-actions">
                  <el-button
                    type="primary"
                    @click="submitFeedback"
                    :loading="submittingFeedback"
                  >
                    Submit Feedback
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-container">
          <el-empty
            description="No itinerary data available"
            :image-size="200"
          >
            <el-button type="primary" @click="goBack">
              Back to Home
            </el-button>
            <el-button type="success" @click="useMockData" style="margin-left: 10px;">
              <el-icon><View /></el-icon>
              Use Mock Data for Testing
            </el-button>
          </el-empty>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Refresh, Edit, House, MapLocation, User, SwitchButton, View } from '@element-plus/icons-vue'
import TravelItineraryResult from '@/components/travel/TravelItineraryResult.vue'

// Router
const router = useRouter()
const route = useRoute()

// 新增：通用导航函数（与规划页一致）
const go = (path) => router.push(path)

// Reactive data
const loading = ref(false)
const regenerating = ref(false)
const submittingFeedback = ref(false)
const error = ref('')
const itineraryData = ref(null)
const generationTime = ref(new Date())

// Keep the last form data we used to generate the itinerary
const lastFormData = ref(null)

// Feedback data
const feedback = reactive({
  rating: 0,
  comment: ''
})

// Methods
const goBack = () => {
  router.push('/home')
}

const formatGenerationTime = () => {
  return generationTime.value.toLocaleString('en-AU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * generateItinerary
 * - 接收 formData（对象），向后端 POST /api/ai/generate/
 * - 后端应返回 { output: { destination, duration, travelers, estimatedBudget, generatedAt, dailyPlans: [...] } }
 * - 解析后设置 itineraryData
 */
const generateItinerary = async (formData = null) => {
  // helper: try to strip code fences like ```json ... ``` and parse JSON
  const tryParseJsonFromString = (s) => {
    if (!s || typeof s !== 'string') return null;
    let candidate = s.trim();
    // remove triple-backtick fences and leading language tag like ```json
    candidate = candidate.replace(/^```(?:\w+)?\s*/i, '').replace(/\s*```$/i, '').trim();
    try {
      return JSON.parse(candidate);
    } catch (e) {
      return null;
    }
  };

  try {
    loading.value = true;
    error.value = '';

    // choose payload and save for regenerate
    const payload = formData || lastFormData.value || {};
    lastFormData.value = payload;

    // call backend
    const response = await axios.post('http://localhost:8080/api/ai/generate/', payload, {
      headers: { 'Content-Type': 'application/json' },
      // optional timeout here
      // timeout: 120000
    });

    console.log('API full response:', response);

    // get candidate output: response.data.output or response.data
    let outputCandidate = response?.data?.output ?? response?.data;

    // If outputCandidate is object and contains raw_text or text, try to parse that
    if (outputCandidate && typeof outputCandidate === 'object') {
      const textField = outputCandidate.raw_text ?? outputCandidate.text ?? null;
      if (textField) {
        const parsed = tryParseJsonFromString(textField);
        if (parsed) {
          outputCandidate = parsed;
        } else {
          // If not parseable, leave it as object (but likely won't contain dailyPlans)
          console.warn('Could not parse JSON from output.raw_text/text; content preview:', (textField.slice ? textField.slice(0, 300) : textField));
        }
      }
    }

    // If outputCandidate is string, try to parse it
    if (typeof outputCandidate === 'string') {
      const parsed = tryParseJsonFromString(outputCandidate) || (() => { try { return JSON.parse(outputCandidate); } catch { return null; } })();
      if (parsed) {
        outputCandidate = parsed;
      } else {
        throw new Error('AI returned text but it could not be parsed as JSON.');
      }
    }

    console.log('Normalized parsed output:', outputCandidate);

    // Now require the field the frontend expects: dailyPlans (strict)
    if (!outputCandidate || typeof outputCandidate !== 'object' || !Array.isArray(outputCandidate.dailyPlans)) {
      console.error('AI response missing required field dailyPlans:', outputCandidate);
      throw new Error('AI response missing dailyPlans');
    }

    // success -> assign
    itineraryData.value = outputCandidate;
    generationTime.value = new Date(outputCandidate.generatedAt || outputCandidate.generated_at || Date.now());
    ElMessage.success('Itinerary generated successfully!');
  } catch (err) {
    console.error('Failed to generate itinerary:', err);
    error.value = err.response?.data?.error || err.message || 'Failed to generate itinerary. Please try again.';
    ElMessage.error(error.value);
  } finally {
    loading.value = false;
  }
};

const regenerateItinerary = async () => {
  try {
    const confirmed = await ElMessageBox.confirm(
      'This will generate a new itinerary with the same preferences. Continue?',
      'Regenerate Itinerary',
      {
        confirmButtonText: 'Yes, Regenerate',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    if (confirmed) {
      regenerating.value = true
      await generateItinerary(lastFormData.value)
      regenerating.value = false
    }
  } catch {
    // User cancelled
    regenerating.value = false
  }
}

const modifyPreferences = () => {
  router.push({
    path: '/travel/plan',
    query: { modify: 'true', ...route.query }
  })
}

const retryGeneration = () => {
  // retry using lastFormData (if none, try to parse route again)
  if (lastFormData.value) {
    generateItinerary(lastFormData.value)
  } else {
    initFromRoute()
    if (lastFormData.value) generateItinerary(lastFormData.value)
  }
}

const handleDownload = () => {
  ElMessage.success('Download started!')
  // TODO: Implement actual download functionality
}

const handleShare = () => {
  ElMessage.info('Share functionality coming soon!')
  // TODO: Implement share functionality
}

const submitFeedback = async () => {
  if (feedback.rating === 0) {
    ElMessage.warning('Please provide a rating')
    return
  }

  try {
    submittingFeedback.value = true

    // TODO: Submit feedback to API
    ElMessage.success('Thank you for your feedback!')

    // Reset feedback form
    feedback.rating = 0
    feedback.comment = ''
  } catch (err) {
    console.error('Failed to submit feedback:', err)
    ElMessage.error('Failed to submit feedback')
  } finally {
    submittingFeedback.value = false
  }
}

// Mock data for testing display
const generateMockData = () => {
  return {
    destination: "Sydney, Australia",
    duration: 5,
    travelers: 2,
    estimatedBudget: 2500,
    generatedAt: new Date().toISOString(),
    dailyPlans: [
      {
        day: 1,
        date: "2024-01-15",
        overview: "Arrival & City Exploration",
        weather: {
          temperature: 28,
          condition: "Sunny"
        },
        activities: [
          {
            time: "09:00",
            title: "Arrive at Sydney Airport",
            description: "Check into hotel and freshen up",
            type: "Transportation",
            location: {
              name: "Sydney Airport",
              address: "Sydney Airport, NSW 2020"
            },
            transportation: {
              method: "Airport Shuttle",
              duration: "30 minutes",
              cost: 25
            },
            estimatedCost: 0,
            tips: ["Arrive early to avoid queues", "Have hotel confirmation ready"]
          },
          {
            time: "11:00",
            title: "Circular Quay & Opera House",
            description: "Visit the iconic Sydney Opera House and take photos",
            type: "Culture",
            location: {
              name: "Sydney Opera House",
              address: "Bennelong Point, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "15 minutes",
              cost: 0
            },
            estimatedCost: 50,
            tips: ["Best photo spots are from Circular Quay", "Book tours in advance"]
          },
          {
            time: "14:00",
            title: "Lunch at The Rocks",
            description: "Traditional Australian lunch with harbor views",
            type: "Dining",
            location: {
              name: "The Rocks",
              address: "The Rocks, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "10 minutes",
              cost: 0
            },
            estimatedCost: 80,
            tips: ["Try local seafood", "Book waterfront tables"]
          },
          {
            time: "16:00",
            title: "Harbor Bridge Walk",
            description: "Walk across the Sydney Harbour Bridge",
            type: "Adventure",
            location: {
              name: "Sydney Harbour Bridge",
              address: "Sydney Harbour Bridge, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "5 minutes",
              cost: 0
            },
            estimatedCost: 0,
            tips: ["Free walkway available", "Best views at sunset"]
          }
        ],
        estimatedWalking: "8 km",
        dailyBudget: 130
      },
      {
        day: 2,
        date: "2024-01-16",
        overview: "Beach Day & Wildlife",
        weather: {
          temperature: 26,
          condition: "Partly Cloudy"
        },
        activities: [
          {
            time: "08:00",
            title: "Bondi Beach",
            description: "Morning surf lesson and beach time",
            type: "Adventure",
            location: {
              name: "Bondi Beach",
              address: "Bondi Beach, NSW 2026"
            },
            transportation: {
              method: "Bus",
              duration: "45 minutes",
              cost: 8
            },
            estimatedCost: 120,
            tips: ["Book surf lessons early", "Bring sunscreen"]
          },
          {
            time: "12:00",
            title: "Taronga Zoo",
            description: "Visit Australia's native wildlife",
            type: "Nature",
            location: {
              name: "Taronga Zoo",
              address: "Bradleys Head Rd, Mosman NSW 2088"
            },
            transportation: {
              method: "Ferry",
              duration: "30 minutes",
              cost: 15
            },
            estimatedCost: 90,
            tips: ["Take the cable car", "Don't miss the koala encounter"]
          },
          {
            time: "17:00",
            title: "Manly Beach Sunset",
            description: "Ferry to Manly and sunset viewing",
            type: "Nature",
            location: {
              name: "Manly Beach",
              address: "Manly Beach, NSW 2095"
            },
            transportation: {
              method: "Ferry",
              duration: "30 minutes",
              cost: 15
            },
            estimatedCost: 30,
            tips: ["Perfect sunset views", "Try local fish and chips"]
          }
        ],
        estimatedWalking: "6 km",
        dailyBudget: 240
      },
      {
        day: 3,
        date: "2024-01-17",
        overview: "Blue Mountains Adventure",
        weather: {
          temperature: 22,
          condition: "Cloudy"
        },
        activities: [
          {
            time: "07:00",
            title: "Blue Mountains Tour",
            description: "Full day tour to Blue Mountains National Park",
            type: "Adventure",
            location: {
              name: "Blue Mountains",
              address: "Blue Mountains National Park, NSW"
            },
            transportation: {
              method: "Tour Bus",
              duration: "2 hours",
              cost: 0
            },
            estimatedCost: 200,
            tips: ["Wear comfortable shoes", "Bring a jacket"]
          },
          {
            time: "18:00",
            title: "Return to Sydney",
            description: "Back to hotel for rest",
            type: "Transportation",
            location: {
              name: "Sydney CBD",
              address: "Sydney CBD, NSW 2000"
            },
            transportation: {
              method: "Tour Bus",
              duration: "2 hours",
              cost: 0
            },
            estimatedCost: 0,
            tips: ["Rest well for tomorrow"]
          }
        ],
        estimatedWalking: "12 km",
        dailyBudget: 200
      },
      {
        day: 4,
        date: "2024-01-18",
        overview: "Cultural & Shopping Day",
        weather: {
          temperature: 25,
          condition: "Sunny"
        },
        activities: [
          {
            time: "09:00",
            title: "Art Gallery of NSW",
            description: "Explore Australian and international art",
            type: "Culture",
            location: {
              name: "Art Gallery of NSW",
              address: "Art Gallery Rd, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "20 minutes",
              cost: 0
            },
            estimatedCost: 20,
            tips: ["Free general admission", "Check special exhibitions"]
          },
          {
            time: "12:00",
            title: "Queen Victoria Building",
            description: "Shopping and lunch in historic building",
            type: "Shopping",
            location: {
              name: "Queen Victoria Building",
              address: "455 George St, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "15 minutes",
              cost: 0
            },
            estimatedCost: 100,
            tips: ["Beautiful architecture", "Great for souvenirs"]
          },
          {
            time: "15:00",
            title: "Darling Harbour",
            description: "Waterfront dining and entertainment",
            type: "Dining",
            location: {
              name: "Darling Harbour",
              address: "Darling Harbour, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "10 minutes",
              cost: 0
            },
            estimatedCost: 150,
            tips: ["Great waterfront views", "Many dining options"]
          }
        ],
        estimatedWalking: "5 km",
        dailyBudget: 270
      },
      {
        day: 5,
        date: "2024-01-19",
        overview: "Departure Day",
        weather: {
          temperature: 27,
          condition: "Sunny"
        },
        activities: [
          {
            time: "09:00",
            title: "Final Shopping",
            description: "Last minute souvenirs and gifts",
            type: "Shopping",
            location: {
              name: "Pitt Street Mall",
              address: "Pitt St, Sydney NSW 2000"
            },
            transportation: {
              method: "Walking",
              duration: "10 minutes",
              cost: 0
            },
            estimatedCost: 100,
            tips: ["Popular shopping district", "Many souvenir shops"]
          },
          {
            time: "12:00",
            title: "Airport Transfer",
            description: "Check out and head to airport",
            type: "Transportation",
            location: {
              name: "Sydney Airport",
              address: "Sydney Airport, NSW 2020"
            },
            transportation: {
              method: "Airport Shuttle",
              duration: "30 minutes",
              cost: 25
            },
            estimatedCost: 50,
            tips: ["Allow extra time for check-in", "Check flight status"]
          }
        ],
        estimatedWalking: "3 km",
        dailyBudget: 150
      }
    ]
  }
}

const useMockData = () => {
  try {
    const mockData = generateMockData()
    itineraryData.value = mockData
    generationTime.value = new Date(mockData.generatedAt)
    error.value = ''
    ElMessage.success('Using mock data for testing display!')
  } catch (err) {
    console.error('Failed to load mock data:', err)
    ElMessage.error('Failed to load mock data')
  }
}

/**
 * Parse route.query.formData and set lastFormData then call generateItinerary
 */
const initFromRoute = () => {
  error.value = ''
  loading.value = true
  try {
    if (route.query.formData) {
      const parsed = JSON.parse(decodeURIComponent(route.query.formData))
      lastFormData.value = parsed
    } else {
      lastFormData.value = {}
    }
  } catch (err) {
    console.error('Failed to parse formData from route:', err)
    error.value = 'Invalid form data passed from planner.'
    lastFormData.value = {}
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  // parse route and trigger generation
  initFromRoute()
  // start generation (use lastFormData, even if it's empty)
  generateItinerary(lastFormData.value)
  
  // For testing purposes: if there's an error after 3 seconds, show mock data option
  setTimeout(() => {
    if (error.value && !itineraryData.value) {
      console.log('Error detected, mock data option available for testing')
    }
  }, 3000)
})

// Cleanup
onBeforeUnmount(() => {
  // Cancel any pending requests if needed (axios cancel token) - optional
})
</script>

<style scoped>
/* Sidebar + main layout to match management/plan page */
.layout-container {
  height: 100vh;
  background-color: transparent;
}

.bottom-container {
  flex: 1;
  height: 100vh;
}

.sidebar {
  background-color: #0f0f0f;
  height: 100%;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
}

.sidebar-menu .el-menu-item:hover {
  background-color: #1890ff !important;
}

.home-main {
  padding: 24px;
  background: transparent;
  position: relative;
  z-index: 1;
  overflow-y: auto;
  height: 100%;
}

/* 背景渐变（复用 auth 页的样式） */
.auth-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(60rem 60rem at 10% 10%, rgba(99, 102, 241, .25), transparent 60%),
    radial-gradient(60rem 60rem at 90% 90%, rgba(236, 72, 153, .22), transparent 60%),
    linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
  filter: saturate(110%);
  z-index: 0;
}

.page-header {
  margin-bottom: 12px;
  color: #e6edf3;
}
:deep(.el-page-header__title) { color: #e6edf3; }
:deep(.el-page-header__content) { color: #a0aec0; }

.page-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 16px;
}

/* Loading State */
.loading-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 0;
}

.loading-text {
  text-align: center;
  margin-top: 1rem;
}

.loading-text h3 {
  color: #8ab4f8;
  margin-bottom: 0.75rem;
}

.loading-text p {
  color: #a0aec0;
}

/* Skeleton dark theme override */
:deep(.el-skeleton) {
  --el-skeleton-color: rgba(148, 163, 184, 0.12);
  --el-skeleton-to-color: rgba(148, 163, 184, 0.18);
}
:deep(.el-skeleton__item) {
  background-color: rgba(255, 255, 255, 0.08) !important;
}

/* Error State */
.error-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  color: #e5e7eb;
}

/* Success State */
.itinerary-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 0 3rem 0;
  color: #e5e7eb;
}

.generation-info {
  margin-bottom: 2rem;
}

/* 调整 el-alert 在深色主题下的表现 */
:deep(.el-alert) {
  border-radius: 12px;
}
:deep(.el-alert--success) {
  background: rgba(16, 185, 129, 0.12);
  color: #d1fae5;
}

/* Feedback Section */
.feedback-section {
  margin-top: 2rem;
}

.feedback-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.32);
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(10px);
}

.feedback-header h3 {
  margin: 0 0 0.5rem 0;
  color: #e6edf3;
}

.feedback-header p {
  margin: 0;
  color: #a0aec0;
  font-size: 0.9rem;
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 0.5rem 0 1rem 0;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-label {
  font-weight: 500;
  color: #e6edf3;
}

.feedback-actions {
  display: flex;
  justify-content: flex-end;
}

/* Empty State */
.empty-container {
  max-width: 600px;
  margin: 3rem auto;
  padding: 2rem;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .page-actions {
    width: 100%;
    justify-content: center;
  }

  .itinerary-container,
  .loading-container {
    padding: 0.5rem;
  }

  .rating-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>