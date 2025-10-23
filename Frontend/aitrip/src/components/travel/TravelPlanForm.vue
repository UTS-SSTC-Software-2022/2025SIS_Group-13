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

        <!-- ✅新增：Trip Start Date -->
        <el-form-item label="Trip Start Date" prop="startDate">
          <el-date-picker
            v-model="travelForm.startDate"
            type="date"
            placeholder="Select start date"
            class="w-100"
            :disabled="loading"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <!-- 🆕 Multi-Destination Selection (替换原有 block) -->
        <el-form-item label="Travel Destinations" prop="destination">
          <div class="destination-container">
            <div
              v-for="(dest, index) in travelForm.destinations"
              :key="index"
              class="destination-item mb-3"
            >
              <div class="destination-inputs">
                <!-- Cascader：用户仍然可以选择多级，但我们只在输入框中保留前两层显示 -->
                <el-cascader
                  v-model="dest.path"
                  :options="destinationOptions"
                  placeholder="Select destination (select deeper to add tags)"
                  class="w-100"
                  clearable
                  filterable
                  :disabled="loading"
                  @change="handleDestinationSelect(index, $event)"
                />
                <el-button
                  v-if="travelForm.destinations.length > 1"
                  type="danger"
                  size="small"
                  plain
                  @click="removeDestination(index)"
                  :disabled="loading"
                  style="margin-left: 8px;"
                >
                  Remove
                </el-button>
              </div>

              <!-- Tags for selected fine-grained places (shown under the input like attractions) -->
              <div class="destination-tags mt-2" v-if="dest.tags && dest.tags.length">
                <el-tag
                  v-for="(tag, tIndex) in dest.tags"
                  :key="tIndex"
                  closable
                  @close="removeDestinationTag(index, tIndex)"
                  class="me-2 mb-2"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </div>

            <!-- Add destination button -->
            <el-button
              type="primary"
              plain
              size="small"
              @click="addDestination"
              :disabled="loading || travelForm.destinations.length >= 6"
            >
              <el-icon class="me-1"><Plus /></el-icon>
              Add Destination
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
// 🆕 Add new fields
const travelForm = reactive({
  startDate: '', // 🆕 trip start date
  peopleCount: 1,
  members: [{ age: '', gender: '' }],
  days: 3,
  destinations: [ // 🆕 modified destination structure
    { path: [], tags: [] }
  ],
  attractions: [],
  themes: [],
  description: ''
})

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
  destination: [
    { validator: validateDestinations, trigger: 'blur' }
  ],
  themes: [
    { type: 'array', min: 1, message: 'Please select at least one travel theme', trigger: 'change' }
  ]
}

// 🆕 Custom validation: at least one destination selected
function validateDestinations(rule, value, callback) {
  if (!travelForm.destinations.some(d => d.path.length > 0)) {
    callback(new Error('Please select at least one destination'))
  } else {
    callback()
  }
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
];


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
// 🆕 Manage dynamic destinations
import { ElMessageBox } from 'element-plus'

function addDestination() {
  travelForm.destinations.push({ path: [], tags: [] })
}

function removeDestination(index) {
  travelForm.destinations.splice(index, 1)
}

function removeDestinationTag(destIndex, tagIndex) {
  if (!travelForm.destinations[destIndex]) return
  travelForm.destinations[destIndex].tags.splice(tagIndex, 1)
}

/*
  关键函数：处理 cascader 变化
  规则：
    - 接收完整的 path （如 ['nsw','sydney','sydney-cbd']）
    - basePath 保留前两层（如果存在两层），用于在输入框中显示（dest.path = basePath）
    - extras 为 path 的第3层及以后；把 extras 对应的 label（或用户自定义值）添加至 dest.tags
    - 如果 extras 中出现 'others'（value === 'others'），弹出 prompt 让用户输入自定义 tag 并加入 dest.tags
*/
async function handleDestinationSelect(index, fullPath) {
  const dest = travelForm.destinations[index]
  if (!dest) return

  // ensure arrays
  if (!Array.isArray(dest.tags)) dest.tags = []
  if (!Array.isArray(fullPath)) fullPath = []

  // if user cleared selection
  if (fullPath.length === 0) {
    dest.path = []
    return
  }

  // compute base (keep up to 2 levels)
  const basePath = fullPath.length >= 2 ? fullPath.slice(0, 2) : fullPath.slice()
  // extras are deeper levels (3rd, 4th, ...)
  const extrasPath = fullPath.slice(2)

  // get labels for fullPath to map extras values to human labels (if available)
  const fullLabels = findLabelsFromPath(destinationOptions, fullPath) // may be null if custom inserted
  const baseLabels = fullLabels ? fullLabels.slice(0, 2) : null
  const extrasLabels = fullLabels ? fullLabels.slice(2) : null

  // apply basePath to dest.path so input displays only base
 dest.path = basePath

  // process extras: for each extra value, either add mapped label or handle 'others'
  for (let i = 0; i < extrasPath.length; i++) {
    const extraValue = extrasPath[i]
    // if extras label available from options, use it; else fallback to the value
    const labelFromOptions = extrasLabels && extrasLabels[i] ? extrasLabels[i] : null

    if (extraValue === 'others') {
      // prompt for custom label
      try {
        const res = await ElMessageBox.prompt(
          'Please enter your custom destination name (max 15 characters):',
          'Custom Destination',
          {
            confirmButtonText: 'Confirm',
            cancelButtonText: 'Cancel',
            inputPattern: /^.{1,15}$/,
            inputErrorMessage: 'Up to 15 characters allowed'
          }
        )
        const custom = res && res.value ? String(res.value).trim() : ''
        if (custom) {
          // add to tags if not duplicate
          if (!dest.tags.includes(custom)) dest.tags.push(custom)
        }
      } catch (e) {
        // user cancelled prompt -> do nothing (不要把 'Others...' 当作标签保留)
      }
    } else {
      // normal case: add mapped label (preferred) or the raw value
      const toAdd = labelFromOptions || extraValue
      if (toAdd && !dest.tags.includes(toAdd)) dest.tags.push(toAdd)
    }
  }
}

// 🆕 Recursive search utility
function findOptionsByValue(options, values) {
  let currentOptions = options
  let currentNode = null
  for (const v of values) {
    currentNode = currentOptions.find(opt => opt.value === v)
    if (!currentNode) return null
    currentOptions = currentNode.children || []
  }
  return currentNode
}

// Helper：根据 value path 返回对应的 label path（若找不到返回 null）
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
    // Validate form
    const valid = await travelFormRef.value.validate()
    if (!valid) return

    // Validate members info
    const invalidMembers = travelForm.members.some(member => !member.age || !member.gender)
    if (invalidMembers) {
      ElMessage.error('Please complete age and gender information for all travelers')
      return
    }

    // Validate attractions or destination selection
    if (!travelForm.destinations && (!travelForm.attractions || travelForm.attractions.length === 0)) {
      ElMessage.error('Please select at least one destination or attraction')
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
      destination: travelForm.destinations,
      attractions: travelForm.attractions,
      themes: travelForm.themes,
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
  color: #E5E7EB; /* 深色背景下更清晰 */
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 14px;
  margin-bottom: 0;
  color: #9CA3AF; /* 深色背景副标题 */
}

.travel-form-content { margin-top: 2rem; }

.form-section {
  margin-bottom: 2rem;
  padding: 1.25rem 1.25rem 1rem;
  background: rgba(17, 24, 39, 0.65); /* 深色毛玻璃卡片 */
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
}

.section-title {
  color: #cbd5e1; /* 深色标题 */
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
  background: rgba(255, 255, 255, 0.04); /* 深色半透明 */
}

.member-item { margin-bottom: 1rem; }
.member-item:last-of-type { margin-bottom: 0.5rem; }
.member-inputs { display: flex; gap: 0.5rem; align-items: center; }
.age-input { flex: 1; max-width: 120px; }
.gender-select { flex: 1; max-width: 120px; }

.add-member-btn {
  width: 100%;
  border-style: dashed;
  border-color: rgba(148, 163, 184, 0.3);
  background: rgba(255, 255, 255, 0.04);
}

.attractions-container { width: 100%; }
.attraction-input { width: 100%; }
.attractions-tags { min-height: 32px; }

.submit-btn {
  height: 44px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 8px;
  border: none;
  color: #fff;
  background: linear-gradient(90deg, #3b82f6, #6366f1); /* 复用既有蓝紫渐变 */
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

/* 让 Select 输入框在非聚焦时也保持深色 */
:deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.035) !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
}

/* 特殊需求文本域改为更深背景，降低亮度 */
:deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.06) !important;
  border-color: rgba(148, 163, 184, 0.22) !important;
}

/* Select 下拉面板使用深色毛玻璃，并提升文字对比 */
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

:deep(.el-checkbox-group) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}
:deep(.el-checkbox) { margin-right: 0; white-space: nowrap; }

@media (max-width: 768px) {
  .form-section { padding: 1rem; }
  .member-inputs { flex-direction: column; gap: 0.5rem; }
  .age-input, .gender-select { max-width: none; }
  :deep(.el-checkbox-group) { grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); }
}

@media (max-width: 576px) {
  .form-title { font-size: 1.5rem; }
  .travel-form-content { margin-top: 1.5rem; }
  .section-title { font-size: 16px; }
}
</style>