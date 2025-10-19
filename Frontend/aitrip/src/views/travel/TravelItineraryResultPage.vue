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
            @save="handleSave"
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
import { ArrowLeft, Refresh, Edit, House, MapLocation, User, SwitchButton } from '@element-plus/icons-vue'
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

const handleSave = async () => {
  try {
    // TODO: Implement save to user account
    ElMessage.success('Itinerary saved to your account!')
  } catch (err) {
    ElMessage.error('Failed to save itinerary')
  }
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