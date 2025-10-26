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
                <el-select
                  v-model="member.language"
                  placeholder="Language"
                  class="language-select"
                  :disabled="loading"
                >
                  <el-option label="English" value="english" />
                  <el-option label="Chinese" value="chinese" />
                  <el-option label="Spanish" value="spanish" />
                  <el-option label="French" value="french" />
                  <el-option label="German" value="german" />
                  <el-option label="Japanese" value="japanese" />
                  <el-option label="Korean" value="korean" />
                  <el-option label="Arabic" value="arabic" />
                </el-select>
                <el-input
                  v-model="member.allergiesAndMedical"
                  placeholder="Allergies & Medical Info"
                  class="medical-input"
                  :disabled="loading"
                />
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

        <!-- Trip Start Date -->
        <el-form-item label="Trip Start Date" prop="startDate">
          <el-date-picker
            v-model="travelForm.startDate"
            type="date"
            placeholder="Select start date"
            class="w-100"
            :disabled="loading"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledDate"
          />
        </el-form-item>

        <!-- Travel Destinations -->
        <el-form-item label="Travel Destinations" prop="destinations">
          <div class="destination-container">
            <div
              v-for="(dest, index) in travelForm.destinations"
              :key="index"
              class="destination-item mb-3"
            >
              <!-- Outer Layer: City Selection -->
              <div class="destination-outer-layer">
                <div class="city-selection-row">
                  <el-cascader
                    v-if="!dest.citySelected"
                    v-model="dest.cityPath"
                    :options="cityOptions"
                    placeholder="Select State/City or choose Other"
                    class="city-selector"
                    clearable
                    filterable
                    :disabled="loading"
                    @change="handleCitySelect(index, $event)"
                  />
                  
                  <!-- City Display (when selected) -->
                  <div v-else class="selected-city-display">
                    <el-tag 
                      type="primary" 
                      size="large"
                      class="city-tag"
                      closable
                      @close="clearCitySelection(index)"
                    >
                      {{ dest.cityName }}
                    </el-tag>
                  </div>

                  <!-- Remove Destination Button -->
                  <el-button
                    v-if="travelForm.destinations.length > 1"
                    type="danger"
                    size="small"
                    plain
                    @click="removeDestination(index)"
                    :disabled="loading"
                    class="remove-destination-btn"
                  >
                    Remove
                  </el-button>
                </div>

                <!-- Inner Layer: Attractions Selection (only show when city is selected) -->
                <div v-if="dest.citySelected" class="destination-inner-layer mt-2">
                  <div class="attractions-selection-row">
                    <el-select
                      v-model="selectedAttraction"
                      placeholder="Select attractions in this city"
                      class="attraction-selector"
                      clearable
                      filterable
                      :disabled="loading"
                      @change="handleAttractionSelect(index, $event)"
                    >
                      <el-option
                        v-for="attraction in getAttractionsForCity(dest.cityPath)"
                        :key="attraction.value"
                        :label="attraction.label"
                        :value="attraction.value"
                      />
                      <el-option
                        label="Other (Custom Input)"
                        value="custom"
                      />
                    </el-select>
                  </div>

                  <!-- Attraction Tags -->
                  <div class="attraction-tags mt-2" v-if="dest.attractions && dest.attractions.length">
                    <el-tag
                      v-for="(attraction, aIndex) in dest.attractions"
                      :key="aIndex"
                      closable
                      @close="removeAttractionTag(index, aIndex)"
                      class="me-2 mb-2"
                      type="success"
                      size="small"
                    >
                      {{ attraction }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>

            <!-- Add Destination Button -->
            <el-button
              type="primary"
              plain
              size="small"
              @click="addDestination"
              :disabled="loading || travelForm.destinations.length >= 6"
              class="add-destination-btn"
            >
              <el-icon class="me-1"><Plus /></el-icon>
              Add Destination
            </el-button>
          </div>
        </el-form-item>

        <!-- Trip Duration -->
        <el-form-item label="Trip Duration (days)" prop="days">
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

        <!-- Trip Type -->
        <el-form-item label="Trip Type" prop="tripType">
          <el-select
            v-model="travelForm.tripType"
            placeholder="Select trip type"
            class="w-100"
            :disabled="loading"
          >
            <el-option label="Romantic" value="romantic" />
            <el-option label="Budget Travel" value="budget" />
            <el-option label="Luxury" value="luxury" />
            <el-option label="Family Leisure" value="family" />
            <el-option label="Adventure & Thrill" value="adventure" />
            <el-option label="Cultural Deep Dive" value="cultural" />
            <el-option label="Relaxed & Slow" value="relaxed" />
          </el-select>
        </el-form-item>

        <!-- Travel Pace -->
        <el-form-item label="Preferred Travel Pace" prop="travelPace">
          <div class="slider-container">
            <span class="slider-label">Relaxed & Slow</span>
            <el-slider
              v-model="travelForm.travelPace"
              :min="1"
              :max="5"
              :step="1"
              show-stops
              :disabled="loading"
              class="pace-slider"
            />
            <span class="slider-label">Packed & High Density</span>
          </div>
        </el-form-item>

        <!-- Travel Themes -->
        <el-form-item label="Travel Themes" prop="themes">
          <div class="themes-grid">
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
          </div>
        </el-form-item>

        <!-- Budget Plan -->
        <el-form-item label="Budget Plan" prop="budgetLevel">
          <div class="slider-container">
            <span class="slider-label">Budget Focused</span>
            <el-slider
              v-model="travelForm.budgetLevel"
              :min="1"
              :max="5"
              :step="1"
              show-stops
              :disabled="loading"
              class="budget-slider"
            />
            <span class="slider-label">High-end Luxury</span>
          </div>
        </el-form-item>

        <!-- Travel Wishes -->
        <el-form-item label="Travel Wishes" prop="travelWishes">
          <el-input
            v-model="travelForm.travelWishes"
            type="textarea"
            :rows="3"
            placeholder="e.g., 'Coffee time every day', 'Must visit a place with ocean'"
            maxlength="200"
            show-word-limit
            :disabled="loading"
          />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// Props and emits
const emit = defineEmits(['submit'])

// Form ref
const travelFormRef = ref()

// Loading state
const loading = ref(false)

// Form data
const travelForm = reactive({
  startDate: '',
  peopleCount: 1,
  members: [{ age: '', gender: '', language: '', allergiesAndMedical: '' }],
  days: 3,
  destinations: [{ 
    cityPath: [], 
    cityName: '', 
    citySelected: false, 
    attractions: [] 
  }],
  tripType: '',
  travelPace: 3,
  themes: [],
  budgetLevel: 3,
  travelWishes: '',
  description: ''
})

// Add reactive variable for attraction selection
const selectedAttraction = ref('')

// Form validation rules
const travelRules = {
  startDate: [
    { required: true, message: 'Please select trip start date', trigger: 'change' }
  ],
  peopleCount: [
    { required: true, message: 'Please select number of travelers', trigger: 'change' }
  ],
  days: [
    { required: true, message: 'Please enter trip duration', trigger: 'blur' },
    { type: 'number', min: 1, max: 30, message: 'Trip duration should be between 1-30 days', trigger: 'blur' }
  ],
  destinations: [
    { validator: validateDestinations, trigger: 'blur' }
  ],
  tripType: [
    { required: true, message: 'Please select trip type', trigger: 'change' }
  ],
  themes: [
    { type: 'array', min: 1, message: 'Please select at least one travel theme', trigger: 'change' }
  ]
}

// Custom validation: at least one destination selected
function validateDestinations(rule, value, callback) {
  if (!travelForm.destinations.some(d => d.citySelected)) {
    callback(new Error('Please select at least one destination'))
  } else {
    callback()
  }
}

// Disable past dates
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7 // Disable dates before today
}

// City options (State/City only) - updated to match destinationOptions structure
const cityOptions = [
  {
    value: 'nsw',
    label: 'New South Wales',
    children: [
      { value: 'Sydney', label: 'Sydney' },
      { value: 'Blue Mountains', label: 'Blue Mountains' },
      { value: 'Hunter Valley', label: 'Hunter Valley' },
      { value: 'Byron Bay', label: 'Byron Bay' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'vic',
    label: 'Victoria',
    children: [
      { value: 'Melbourne', label: 'Melbourne' },
      { value: 'Great Ocean Road', label: 'Great Ocean Road' },
      { value: 'Yarra Valley', label: 'Yarra Valley' },
      { value: 'Phillip Island', label: 'Phillip Island' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'qld',
    label: 'Queensland',
    children: [
      { value: 'Brisbane', label: 'Brisbane' },
      { value: 'Gold Coast', label: 'Gold Coast' },
      { value: 'Cairns', label: 'Cairns' },
      { value: 'Whitsundays', label: 'Whitsundays' },
      { value: 'Sunshine Coast', label: 'Sunshine Coast' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'wa',
    label: 'Western Australia',
    children: [
      { value: 'Perth', label: 'Perth' },
      { value: 'Margaret River', label: 'Margaret River' },
      { value: 'Broome', label: 'Broome' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'sa',
    label: 'South Australia',
    children: [
      { value: 'Adelaide', label: 'Adelaide' },
      { value: 'Barossa Valley', label: 'Barossa Valley' },
      { value: 'Kangaroo Island', label: 'Kangaroo Island' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'tas',
    label: 'Tasmania',
    children: [
      { value: 'Hobart', label: 'Hobart' },
      { value: 'Launceston', label: 'Launceston' },
      { value: 'Cradle Mountain', label: 'Cradle Mountain' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'nt',
    label: 'Northern Territory',
    children: [
      { value: 'Darwin', label: 'Darwin' },
      { value: 'Alice Springs', label: 'Alice Springs' },
      { value: 'Uluru', label: 'Uluru' },
      { value: 'Others...', label: 'Others...' }
    ]
  },
  {
    value: 'act',
    label: 'Australian Capital Territory',
    children: [
      { value: 'Canberra', label: 'Canberra' },
      { value: 'Others...', label: 'Others...' }
    ]
  }
]

// Full destination options with attractions (for getting attractions by city)
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
          { value: 'darling-harbour', label: 'Darling Harbour' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      {
        value: 'blue-mountains',
        label: 'Blue Mountains',
        children: [
          { value: 'katoomba', label: 'Katoomba' },
          { value: 'leura', label: 'Leura' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      { value: 'hunter-valley', label: 'Hunter Valley' },
      { value: 'byron-bay', label: 'Byron Bay' },
      { value: 'others', label: 'Others...', isCustom: true }
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
          { value: 'south-yarra', label: 'South Yarra' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      { value: 'great-ocean-road', label: 'Great Ocean Road' },
      { value: 'yarra-valley', label: 'Yarra Valley' },
      { value: 'phillip-island', label: 'Phillip Island' },
      { value: 'others', label: 'Others...', isCustom: true }
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
          { value: 'south-bank', label: 'South Bank' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      { value: 'gold-coast', label: 'Gold Coast' },
      { value: 'cairns', label: 'Cairns' },
      { value: 'whitsundays', label: 'Whitsundays' },
      { value: 'sunshine-coast', label: 'Sunshine Coast' },
      { value: 'others', label: 'Others...', isCustom: true }
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
          { value: 'fremantle', label: 'Fremantle' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      { value: 'margaret-river', label: 'Margaret River' },
      { value: 'broome', label: 'Broome' },
      { value: 'others', label: 'Others...', isCustom: true }
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
          { value: 'glenelg', label: 'Glenelg' },
          { value: 'others', label: 'Others...', isCustom: true }
        ]
      },
      { value: 'barossa-valley', label: 'Barossa Valley' },
      { value: 'kangaroo-island', label: 'Kangaroo Island' },
      { value: 'others', label: 'Others...', isCustom: true }
    ]
  },
  {
    value: 'tas',
    label: 'Tasmania',
    children: [
      { value: 'hobart', label: 'Hobart' },
      { value: 'launceston', label: 'Launceston' },
      { value: 'cradle-mountain', label: 'Cradle Mountain' },
      { value: 'others', label: 'Others...', isCustom: true }
    ]
  },
  {
    value: 'nt',
    label: 'Northern Territory',
    children: [
      { value: 'darwin', label: 'Darwin' },
      { value: 'alice-springs', label: 'Alice Springs' },
      { value: 'uluru', label: 'Uluru' },
      { value: 'others', label: 'Others...', isCustom: true }
    ]
  },
  {
    value: 'act',
    label: 'Australian Capital Territory',
    children: [
      { value: 'canberra', label: 'Canberra' },
      { value: 'others', label: 'Others...', isCustom: true }
    ]
  }
]

// Watch people count to adjust members array
watch(() => travelForm.peopleCount, (newCount) => {
  const currentLength = travelForm.members.length
  
  if (newCount > currentLength) {
    // Add new members
    for (let i = currentLength; i < newCount; i++) {
      travelForm.members.push({ age: '', gender: '', language: '', allergiesAndMedical: '' })
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
    travelForm.members.push({ age: '', gender: '', language: '', allergiesAndMedical: '' })
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
 * Manage dynamic destinations
 */
function addDestination() {
  travelForm.destinations.push({ 
    cityPath: [], 
    cityName: '', 
    citySelected: false, 
    attractions: [] 
  })
}

function removeDestination(index) {
  travelForm.destinations.splice(index, 1)
}

// Handle city selection (outer layer)
const handleCitySelect = (index, value) => {
  const dest = travelForm.destinations[index]
  
  if (!value || value.length === 0) {
    dest.citySelected = false
    dest.cityName = ''
    dest.attractions = []
    return
  }

  // Check if the last level is "others"
  if (value[value.length - 1] === 'others') {
    // Prompt for custom city name
    ElMessageBox.prompt('Please enter the custom city name:', 'Custom City', {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      inputPattern: /\S+/,
      inputErrorMessage: 'City name cannot be empty'
    }).then(({ value: customName }) => {
      if (customName && customName.trim()) {
        dest.cityPath = value
        dest.cityName = customName.trim()
        dest.citySelected = true
        dest.attractions = []
      }
    }).catch(() => {
      // User cancelled, reset selection
      dest.cityPath = []
    })
  } else {
    // For predefined cities
    dest.cityPath = value
    dest.cityName = value[value.length - 1]
    dest.citySelected = true
    dest.attractions = []
  }
}

// Clear city selection
const clearCitySelection = (index) => {
  const dest = travelForm.destinations[index]
  dest.cityPath = []
  dest.cityName = ''
  dest.citySelected = false
  dest.attractions = []
}

// Handle attraction selection (inner layer)
const handleAttractionSelect = (index, value) => {
  if (!value) return
  
  const dest = travelForm.destinations[index]
  
  if (value === 'custom') {
    // Prompt for custom attraction name
    ElMessageBox.prompt('Please enter the custom attraction name:', 'Custom Attraction', {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      inputPattern: /\S+/,
      inputErrorMessage: 'Attraction name cannot be empty'
    }).then(({ value: customName }) => {
      if (customName && customName.trim()) {
        const attractionName = customName.trim()
        if (!dest.attractions.includes(attractionName)) {
          dest.attractions.push(attractionName)
        }
      }
    }).catch(() => {
      // User cancelled, do nothing
    })
  } else {
    // For predefined attractions
    if (!dest.attractions.includes(value)) {
      dest.attractions.push(value)
    }
  }
  
  // Clear the selection
  selectedAttraction.value = ''
}

// Remove attraction tag
const removeAttractionTag = (index, attractionIndex) => {
  travelForm.destinations[index].attractions.splice(attractionIndex, 1)
}

// Get attractions for a specific city
const getAttractionsForCity = (cityPath) => {
  if (!cityPath || cityPath.length < 2) return []
  
  const [state, city] = cityPath
  
  // Find the state in destinationOptions
  const stateOption = destinationOptions.find(s => s.value === state)
  if (!stateOption) return []
  
  // Find the city in the state
  const cityOption = stateOption.children.find(c => c.value === city)
  if (!cityOption || !cityOption.children) return []
  
  // Return the attractions (children of the city)
  return cityOption.children.filter(attraction => attraction.value !== 'others')
}

/**
 * Helper: find labels from path
 */
function findLabelsFromPath(options, path) {
  const labels = []
  let opts = options
  for (const v of path) {
    if (!Array.isArray(opts)) return null
    const node = opts.find(o => o.value === v)
    if (!node) return null
    labels.push(node.label)
    opts = node.children || []
  }
  return labels
}

/**
 * Handle form submission
 */
const handleSubmit = async () => {
  try {
    // Validate form with detailed error messages
    const valid = await travelFormRef.value.validate().catch(() => false)
    if (!valid) {
      // Check specific validation failures and provide detailed English messages
      const validationErrors = []
      
      // Check required fields
      if (!travelForm.startDate) {
        validationErrors.push('Trip start date is required')
      }
      if (!travelForm.peopleCount) {
        validationErrors.push('Number of travelers is required')
      }
      if (!travelForm.days || travelForm.days < 1 || travelForm.days > 30) {
        validationErrors.push('Trip duration must be between 1-30 days')
      }
      if (!travelForm.destinations.some(d => d.citySelected)) {
        validationErrors.push('At least one travel destination must be selected')
      }
      if (!travelForm.tripType) {
        validationErrors.push('Trip type must be selected')
      }
      if (!travelForm.themes || travelForm.themes.length === 0) {
        validationErrors.push('At least one travel theme must be selected')
      }
      
      // Show detailed error message
      const errorMessage = validationErrors.length > 0 
        ? `Please complete the following required information:\n• ${validationErrors.join('\n• ')}`
        : 'Please complete all required fields before generating your itinerary'
      
      ElMessage({
        message: errorMessage,
        type: 'error',
        duration: 6000,
        showClose: true
      })
      return
    }

    // Validate members info
    const invalidMembers = travelForm.members.some(member => !member.age || !member.gender || !member.language)
    if (invalidMembers) {
      ElMessage({
        message: 'Please complete age, gender and language information for all travelers',
        type: 'error',
        duration: 5000,
        showClose: true
      })
      return
    }

    loading.value = true

    // Prepare destination string for backend
    const destinationString = travelForm.destinations
      .filter(dest => dest.citySelected)
      .map(dest => {
        const cityString = dest.cityName
        const attractionsString = dest.attractions.length > 0 ? ' #' + dest.attractions.join(', #') : ''
        return cityString + attractionsString
      })
      .join('\n')

    // Prepare data for submission
    const submitData = {
      startDate: travelForm.startDate,
      peopleCount: travelForm.peopleCount,
      members: travelForm.members.map(member => ({
        age: parseInt(member.age),
        gender: member.gender,
        language: member.language,
        allergiesAndMedical: member.allergiesAndMedical || ''
      })),
      days: travelForm.days,
      destination: destinationString,
      tripType: travelForm.tripType,
      travelPace: travelForm.travelPace,
      themes: travelForm.themes,
      budgetLevel: travelForm.budgetLevel,
      travelWishes: travelForm.travelWishes || '',
      description: String(travelForm.description || '').trim()
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
.travel-plan-form { position: relative; }

.form-title {
  color: #E5E7EB;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 14px;
  margin-bottom: 0;
  color: #9CA3AF;
}

.travel-form-content { margin-top: 2rem; }

.form-section {
  margin-bottom: 2rem;
  padding: 1.25rem 1.25rem 1rem;
  background: rgba(17, 24, 39, 0.65);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
}

.section-title {
  color: #cbd5e1;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.members-container {
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 10px;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.04);
}

.member-item { margin-bottom: 1rem; }
.member-item:last-of-type { margin-bottom: 0.5rem; }
.member-inputs { 
  display: grid; 
  grid-template-columns: 80px 100px 120px 1fr auto;
  gap: 0.5rem; 
  align-items: center; 
}

.age-input { max-width: 80px; }
.gender-select { max-width: 100px; }
.language-select { max-width: 120px; }
.medical-input { flex: 1; }

.add-member-btn {
  width: 100%;
  border-style: dashed;
  border-color: rgba(148, 163, 184, 0.3);
  background: rgba(255, 255, 255, 0.04);
}

.destination-container { width: 100%; }
.destination-item { margin-bottom: 1rem; }

.destination-outer-layer {
  width: 100%;
}

.city-selection-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.city-selector {
  flex: 1;
  min-width: 0;
}

.selected-city-display {
  flex: 1;
  min-width: 0;
}

.city-tag {
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 6px;
}

.remove-destination-btn {
  flex-shrink: 0;
}

.destination-inner-layer {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 6px;
  padding: 12px;
  margin-top: 8px;
}

.attractions-selection-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.attraction-selector {
  width: 100%;
}

.attraction-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.add-destination-btn {
  margin-top: 8px;
  width: 100%;
  border-style: dashed;
  border-color: rgba(148, 163, 184, 0.3);
  background: rgba(255, 255, 255, 0.04);
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.slider-label {
  color: #9CA3AF;
  font-size: 12px;
  white-space: nowrap;
  min-width: 100px;
}

.pace-slider, .budget-slider {
  flex: 1;
}

.themes-grid {
  width: 100%;
}

.themes-grid :deep(.el-checkbox-group) {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem 1rem;
}

.submit-btn {
  height: 44px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 8px;
  border: none;
  color: #fff;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  box-shadow: 0 8px 22px rgba(59, 130, 246, 0.28);
}
.submit-btn:hover { filter: brightness(1.05); }

:deep(.el-form-item__label) { color: #cdd6e3 !important; }
:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.035) !important;
  box-shadow: none !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}
:deep(.el-input__inner),
:deep(.el-textarea__inner) { color: #e5e7eb !important; }
:deep(.el-input__inner::placeholder),
:deep(.el-textarea__inner::placeholder) { color: #9aa4b2 !important; }
:deep(.el-input.is-focus .el-input__wrapper),
:deep(.el-textarea.is-focus .el-textarea__inner),
:deep(.el-select .el-input.is-focus .el-input__wrapper) {
  border-color: #7c8cf8 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.22) !important;
  background: rgba(255, 255, 255, 0.06) !important;
}

:deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.035) !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
}

:deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.06) !important;
  border-color: rgba(148, 163, 184, 0.22) !important;
}

:deep(.el-select__popper) {
  background: rgba(15, 23, 42, 0.92) !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45) !important;
  backdrop-filter: blur(10px) !important;
}
:deep(.el-select__popper .el-select-dropdown) {
  background: transparent !important;
  color: #e5e7eb !important;
}
:deep(.el-select-dropdown__item) { color: #e5e7eb !important; }
:deep(.el-select-dropdown__item:hover) { background-color: rgba(255, 255, 255, 0.06) !important; }
:deep(.el-select-dropdown__item.is-selected),
:deep(.el-select-dropdown__item.selected) {
  background-color: rgba(99, 102, 241, 0.18) !important;
  color: #fff !important;
}

:deep(.el-checkbox) { 
  margin-right: 0; 
  white-space: nowrap; 
  color: #e5e7eb !important;
}

:deep(.el-slider__runway) {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-slider__bar) {
  background-color: #6366f1 !important;
}

:deep(.el-slider__button) {
  border-color: #6366f1 !important;
  background-color: #6366f1 !important;
}

:deep(.el-slider__stop) {
  background-color: rgba(255, 255, 255, 0.3) !important;
}

@media (max-width: 768px) {
  .form-section { padding: 1rem; }
  .member-inputs { 
    grid-template-columns: 1fr;
    gap: 0.5rem; 
  }
  .age-input, .gender-select, .language-select, .medical-input { max-width: none; }
  .themes-grid :deep(.el-checkbox-group) { 
    grid-template-columns: 1fr;
  }
  .slider-container {
    flex-direction: column;
    gap: 0.5rem;
  }
  .slider-label {
    min-width: auto;
    text-align: center;
  }
}

@media (max-width: 576px) {
  .form-title { font-size: 1.5rem; }
  .travel-form-content { margin-top: 1.5rem; }
  .section-title { font-size: 16px; }
}
</style>