<template>
  <div class="travel-plan-form">
    <!-- Header -->
    <div class="text-center mb-4">
      <h2 class="form-title">Create Your Personalized Travel Itinerary</h2>
      <p class="form-subtitle text-muted">Tell us your preferences and we'll craft the perfect Australian adventure for you</p>
    </div>

    <!-- Travel Plan Form -->
    <el-form
      ref="travelFormRef"
      :model="travelForm"
      :rules="travelRules"
      class="travel-form-content"
      label-position="top"
      size="large"
    >
      <!-- Basic Information Section -->
      <div class="form-section">
        <h3 class="section-title">Basic Information</h3>
        
        <!-- Number of Travelers -->
        <el-form-item label="Number of Travelers" prop="peopleCount">
          <el-select
            v-model="travelForm.peopleCount"
            placeholder="Select number of travelers"
            class="w-100"
            :disabled="loading"
          >
            <el-option
              v-for="num in 10"
              :key="num"
              :label="`${num} ${num === 1 ? 'person' : 'people'}`"
              :value="num"
            />
          </el-select>
        </el-form-item>

        <!-- Traveler Information -->
        <el-form-item label="Traveler Information" prop="members">
          <div class="members-container">
            <div
              v-for="(member, index) in travelForm.members"
              :key="index"
              class="member-item"
            >
              <div class="member-inputs">
                <el-input
                  v-model="member.age"
                  type="number"
                  placeholder="Age"
                  class="age-input"
                  :disabled="loading"
                  min="1"
                  max="120"
                />
                <el-select
                  v-model="member.gender"
                  placeholder="Gender"
                  class="gender-select"
                  :disabled="loading"
                >
                  <el-option label="Male" value="male" />
                  <el-option label="Female" value="female" />
                </el-select>
                <el-button
                  v-if="travelForm.members.length > 1"
                  type="danger"
                  size="small"
                  plain
                  @click="removeMember(index)"
                  :disabled="loading"
                >
                  Remove
                </el-button>
              </div>
            </div>
            <el-button
              type="primary"
              plain
              size="small"
              @click="addMember"
              :disabled="loading || travelForm.members.length >= 10"
              class="add-member-btn"
            >
              <el-icon class="me-1"><Plus /></el-icon>
              Add Traveler
            </el-button>
          </div>
        </el-form-item>

        <!-- Trip Duration -->
        <el-form-item label="Trip Duration" prop="days">
          <el-input-number
            v-model="travelForm.days"
            :min="1"
            :max="30"
            placeholder="Enter trip duration"
            class="w-100"
            :disabled="loading"
          />
        </el-form-item>
      </div>

      <!-- Travel Preferences -->
      <div class="form-section">
        <h3 class="section-title">Travel Preferences</h3>
        
        <!-- Destination Selection -->
        <el-form-item label="Travel Destination" prop="destination">
          <el-cascader
            v-model="travelForm.destination"
            :options="destinationOptions"
            placeholder="Select state/city/region"
            class="w-100"
            :disabled="loading"
            clearable
            filterable
          />
        </el-form-item>

        <!-- Must-Visit Attractions -->
        <el-form-item label="Must-Visit Attractions">
          <div class="attractions-container">
            <el-input
              v-model="currentAttraction"
              placeholder="Enter attraction name, press Enter to add"
              class="attraction-input"
              :disabled="loading"
              @keyup.enter="addAttraction"
            >
              <template #append>
                <el-button @click="addAttraction" :disabled="loading">
                  Add
                </el-button>
              </template>
            </el-input>
            <div class="attractions-tags mt-2">
              <el-tag
                v-for="(attraction, index) in travelForm.attractions"
                :key="index"
                closable
                @close="removeAttraction(index)"
                class="me-2 mb-2"
              >
                {{ attraction }}
              </el-tag>
            </div>
          </div>
        </el-form-item>

        <!-- Travel Themes -->
        <el-form-item label="Travel Themes" prop="themes">
          <el-checkbox-group v-model="travelForm.themes" :disabled="loading">
            <el-checkbox label="Culture & Heritage">Culture & Heritage</el-checkbox>
            <el-checkbox label="Nature & Wildlife">Nature & Wildlife</el-checkbox>
            <el-checkbox label="Food & Wine">Food & Wine</el-checkbox>
            <el-checkbox label="Relaxation & Beaches">Relaxation & Beaches</el-checkbox>
            <el-checkbox label="Adventure & Exploration">Adventure & Exploration</el-checkbox>
            <el-checkbox label="Shopping & Entertainment">Shopping & Entertainment</el-checkbox>
            <el-checkbox label="Family Fun">Family Fun</el-checkbox>
            <el-checkbox label="Photography">Photography</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </div>

      <!-- Additional Requirements -->
      <div class="form-section">
        <h3 class="section-title">Special Requirements</h3>
        
        <el-form-item label="Additional Requirements">
          <el-input
            v-model="travelForm.description"
            type="textarea"
            :rows="4"
            placeholder="Describe your special requirements, preferences or other ideas..."
            maxlength="200"
            show-word-limit
            :disabled="loading"
          />
        </el-form-item>
      </div>

      <!-- Submit Button -->
      <el-form-item class="mb-3">
        <el-button
          type="primary"
          class="submit-btn w-100"
          :loading="loading"
          @click="handleSubmit"
        >
          {{ loading ? 'Generating...' : 'Generate Travel Itinerary' }}
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// Props and emits
const emit = defineEmits(['submit'])

// Form ref
const travelFormRef = ref()

// Loading state
const loading = ref(false)

// Current attraction input
const currentAttraction = ref('')

// Form data
const travelForm = reactive({
  peopleCount: 1,
  members: [
    { age: '', gender: '' }
  ],
  days: 3,
  destination: [],
  attractions: [],
  themes: [],
  description: ''
})

// Form validation rules
const travelRules = {
  peopleCount: [
    { required: true, message: 'Please select number of travelers', trigger: 'change' }
  ],
  days: [
    { required: true, message: 'Please enter trip duration', trigger: 'blur' },
    { type: 'number', min: 1, max: 30, message: 'Trip duration should be between 1-30 days', trigger: 'blur' }
  ],
  destination: [
    { required: true, message: 'Please select your destination', trigger: 'change' }
  ],
  themes: [
    { type: 'array', min: 1, message: 'Please select at least one travel theme', trigger: 'change' }
  ]
}

// Australian destination options (simplified version, should be fetched from API in production)
const destinationOptions = [
  {
    value: 'nsw',
    label: 'New South Wales',
    children: [
      {
        value: 'sydney',
        label: 'Sydney',
        children: [
          { value: 'sydney-cbd', label: 'Sydney CBD' },
          { value: 'bondi', label: 'Bondi' },
          { value: 'manly', label: 'Manly' },
          { value: 'darling-harbour', label: 'Darling Harbour' }
        ]
      },
      {
        value: 'blue-mountains',
        label: 'Blue Mountains',
        children: [
          { value: 'katoomba', label: 'Katoomba' },
          { value: 'leura', label: 'Leura' }
        ]
      },
      { value: 'hunter-valley', label: 'Hunter Valley' },
      { value: 'byron-bay', label: 'Byron Bay' }
    ]
  },
  {
    value: 'vic',
    label: 'Victoria',
    children: [
      {
        value: 'melbourne',
        label: 'Melbourne',
        children: [
          { value: 'melbourne-cbd', label: 'Melbourne CBD' },
          { value: 'st-kilda', label: 'St Kilda' },
          { value: 'fitzroy', label: 'Fitzroy' },
          { value: 'south-yarra', label: 'South Yarra' }
        ]
      },
      { value: 'great-ocean-road', label: 'Great Ocean Road' },
      { value: 'yarra-valley', label: 'Yarra Valley' },
      { value: 'phillip-island', label: 'Phillip Island' }
    ]
  },
  {
    value: 'qld',
    label: 'Queensland',
    children: [
      {
        value: 'brisbane',
        label: 'Brisbane',
        children: [
          { value: 'brisbane-cbd', label: 'Brisbane CBD' },
          { value: 'south-bank', label: 'South Bank' }
        ]
      },
      { value: 'gold-coast', label: 'Gold Coast' },
      { value: 'cairns', label: 'Cairns' },
      { value: 'whitsundays', label: 'Whitsundays' },
      { value: 'sunshine-coast', label: 'Sunshine Coast' }
    ]
  },
  {
    value: 'wa',
    label: 'Western Australia',
    children: [
      {
        value: 'perth',
        label: 'Perth',
        children: [
          { value: 'perth-cbd', label: 'Perth CBD' },
          { value: 'fremantle', label: 'Fremantle' }
        ]
      },
      { value: 'margaret-river', label: 'Margaret River' },
      { value: 'broome', label: 'Broome' }
    ]
  },
  {
    value: 'sa',
    label: 'South Australia',
    children: [
      {
        value: 'adelaide',
        label: 'Adelaide',
        children: [
          { value: 'adelaide-cbd', label: 'Adelaide CBD' },
          { value: 'glenelg', label: 'Glenelg' }
        ]
      },
      { value: 'barossa-valley', label: 'Barossa Valley' },
      { value: 'kangaroo-island', label: 'Kangaroo Island' }
    ]
  },
  {
    value: 'tas',
    label: 'Tasmania',
    children: [
      { value: 'hobart', label: 'Hobart' },
      { value: 'launceston', label: 'Launceston' },
      { value: 'cradle-mountain', label: 'Cradle Mountain' }
    ]
  },
  {
    value: 'nt',
    label: 'Northern Territory',
    children: [
      { value: 'darwin', label: 'Darwin' },
      { value: 'alice-springs', label: 'Alice Springs' },
      { value: 'uluru', label: 'Uluru' }
    ]
  },
  {
    value: 'act',
    label: 'Australian Capital Territory',
    children: [
      { value: 'canberra', label: 'Canberra' }
    ]
  }
]

// Watch people count to adjust members array
watch(() => travelForm.peopleCount, (newCount) => {
  const currentLength = travelForm.members.length
  
  if (newCount > currentLength) {
    // Add new members
    for (let i = currentLength; i < newCount; i++) {
      travelForm.members.push({ age: '', gender: '' })
    }
  } else if (newCount < currentLength) {
    // Remove excess members
    travelForm.members.splice(newCount)
  }
})

/**
 * Add a new member
 */
const addMember = () => {
  if (travelForm.members.length < 10) {
    travelForm.members.push({ age: '', gender: '' })
    travelForm.peopleCount = travelForm.members.length
  }
}

/**
 * Remove a member
 */
const removeMember = (index) => {
  if (travelForm.members.length > 1) {
    travelForm.members.splice(index, 1)
    travelForm.peopleCount = travelForm.members.length
  }
}

/**
 * Add attraction
 */
const addAttraction = () => {
  const attraction = currentAttraction.value.trim()
  if (attraction && !travelForm.attractions.includes(attraction)) {
    travelForm.attractions.push(attraction)
    currentAttraction.value = ''
  } else if (travelForm.attractions.includes(attraction)) {
    ElMessage.warning('This attraction has already been added')
  }
}

/**
 * Remove attraction
 */
const removeAttraction = (index) => {
  travelForm.attractions.splice(index, 1)
}

/**
 * Handle form submission
 */
const handleSubmit = async () => {
  try {
    // Validate form
    const valid = await travelFormRef.value.validate()
    if (!valid) return

    // Validate members info
    const invalidMembers = travelForm.members.some(member => !member.age || !member.gender)
    if (invalidMembers) {
      ElMessage.error('Please complete age and gender information for all travelers')
      return
    }

    loading.value = true

    // Prepare data for submission
    const submitData = {
      peopleCount: travelForm.peopleCount,
      members: travelForm.members.map(member => ({
        age: parseInt(member.age),
        gender: member.gender
      })),
      days: travelForm.days,
      destination: travelForm.destination,
      attractions: travelForm.attractions,
      themes: travelForm.themes,
      description: travelForm.description
    }

    // Emit submit event with form data
    emit('submit', submitData)
    
    ElMessage.success('Generating your personalized travel itinerary...')
    
  } catch (error) {
    console.error('Form submission error:', error)
    ElMessage.error('Submission failed, please try again')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.travel-plan-form {
  position: relative;
}

.form-title {
  color: #303133;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 14px;
  margin-bottom: 0;
}

.travel-form-content {
  margin-top: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(64, 158, 255, 0.1);
}

.section-title {
  color: #409eff;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(64, 158, 255, 0.2);
}

.members-container {
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 1rem;
  background: #fafafa;
}

.member-item {
  margin-bottom: 1rem;
}

.member-item:last-of-type {
  margin-bottom: 0.5rem;
}

.member-inputs {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.age-input {
  flex: 1;
  max-width: 120px;
}

.gender-select {
  flex: 1;
  max-width: 120px;
}

.add-member-btn {
  width: 100%;
  border-style: dashed;
}

.attractions-container {
  width: 100%;
}

.attraction-input {
  width: 100%;
}

.attractions-tags {
  min-height: 32px;
}

.submit-btn {
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 6px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border: none;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #66b1ff 0%, #409eff 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

/* Checkbox group styling */
:deep(.el-checkbox-group) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

:deep(.el-checkbox) {
  margin-right: 0;
  white-space: nowrap;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .form-section {
    padding: 1rem;
  }
  
  .member-inputs {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .age-input,
  .gender-select {
    max-width: none;
  }
  
  :deep(.el-checkbox-group) {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
}

@media (max-width: 576px) {
  .form-title {
    font-size: 1.5rem;
  }
  
  .travel-form-content {
    margin-top: 1.5rem;
  }
  
  .section-title {
    font-size: 16px;
  }
}
</style>