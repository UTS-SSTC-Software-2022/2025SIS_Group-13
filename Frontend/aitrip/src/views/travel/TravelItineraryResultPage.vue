<template>
  <div class="travel-itinerary-result-page">
    <!-- Navigation Bar -->
    <div class="page-header">
      <el-button
        type="text"
        @click="goBack"
        class="back-button"
      >
        <el-icon><ArrowLeft /></el-icon>
        Back to Home
      </el-button>

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
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
      <div class="loading-text">
        <h3>🤖 AI is crafting your perfect Australian adventure...</h3>
        <p>This may take a few moments while we analyze your preferences and create a personalized itinerary.</p>
      </div>
    </div>

    <!-- Error State -->
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

    <!-- Success State - Show Itinerary -->
    <div v-else-if="itineraryData" class="itinerary-container">
      <!-- Generation Info -->
      <div class="generation-info">
        <el-alert
          title="✨ Your itinerary has been generated!"
          type="success"
          :description="`Generated on ${formatGenerationTime()} using AI analysis of your preferences.`"
          show-icon
          :closable="false"
        />
      </div>

      <!-- Itinerary Component -->
      <TravelItineraryResult
        :itinerary-data="itineraryData"
        @download="handleDownload"
        @share="handleShare"
        @save="handleSave"
      />

      <!-- Feedback Section -->
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

    <!-- Empty State -->
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Refresh, Edit } from '@element-plus/icons-vue'
import TravelItineraryResult from '@/components/travel/TravelItineraryResult.vue'

// Router
const router = useRouter()
const route = useRoute()

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
.travel-itinerary-result-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 3rem;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.back-button {
  font-size: 1rem;
  color: #409eff;
  padding: 0;
}

.back-button:hover {
  color: #66b1ff;
}

.page-actions {
  display: flex;
  gap: 1rem;
}

/* Loading State */
.loading-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem;
}

.loading-text {
  text-align: center;
  margin-top: 2rem;
}

.loading-text h3 {
  color: #409eff;
  margin-bottom: 1rem;
}

.loading-text p {
  color: #6c757d;
}

/* Error State */
.error-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}

/* Success State */
.itinerary-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem;
}

.generation-info {
  margin-bottom: 3rem;
}

/* Feedback Section */
.feedback-section {
  margin-top: 4rem;
}

.feedback-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.feedback-header h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.feedback-header p {
  margin: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.feedback-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 1rem 0;
}

.rating-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-label {
  font-weight: 500;
  color: #2c3e50;
}

.feedback-actions {
  display: flex;
  justify-content: flex-end;
}

/* Empty State */
.empty-container {
  max-width: 600px;
  margin: 4rem auto;
  padding: 2rem;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .page-actions {
    width: 100%;
    justify-content: center;
  }

  .itinerary-container,
  .loading-container {
    padding: 1rem;
  }

  .rating-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
