<template>
  <div class="google-map-container">
    <div class="map-header">
      <h2>Travel Map</h2>
      <div class="map-controls">
        <el-button size="small" @click="toggleMapType">
          <el-icon><View /></el-icon>
          {{ mapType === 'roadmap' ? 'Satellite' : 'Road' }}
        </el-button>
      </div>
    </div>
    <div class="map-legend">
      <div class="legend-item">
        <div class="legend-icon planned"></div>
        <span>Planned</span>
      </div>
      <div class="legend-item">
        <div class="legend-icon completed"></div>
        <span>Completed</span>
      </div>
    </div>
    <div ref="mapContainer" class="map-box" :class="{ 'loading': isLoading }">
      <div v-if="isLoading" class="map-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>Loading map...</span>
      </div>
      <div v-if="error" class="map-error">
        <el-icon><Warning /></el-icon>
        <span>{{ error }}</span>
        <el-button size="small" @click="initMap">Retry</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { Location, View, Loading, Warning } from '@element-plus/icons-vue'

// Google Maps API Key - 在实际项目中应该从环境变量或配置文件中获取
const googleMapsApiKey = 'AIzaSyCvUOTSTS_KRZZi5kTbKoQpWsM0QLq2VfM' // 请替换为实际的API Key

// Props
const props = defineProps({
  plans: {
    type: Array,
    default: () => []
  },
  finishedPlans: {
    type: Array,
    default: () => []
  }
})

// Reactive data
const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const isLoading = ref(true)
const error = ref('')
const mapType = ref('roadmap')

// Initialize map
const initMap = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    // Load Google Maps API script if not already loaded
    if (!window.google || !window.google.maps) {
      await loadGoogleMapsScript()
    }
    
    // Wait for DOM to be ready
    await nextTick()
    
    // 更详细的DOM检查
    if (!mapContainer.value) {
      console.error('Map container ref is null')
      throw new Error('Map container not found')
    }
    
    // 检查DOM元素是否真的存在于文档中
    if (!document.contains(mapContainer.value)) {
      console.error('Map container element not in document')
      throw new Error('Map container not attached to document')
    }
    
    console.log('Map container found and ready:', mapContainer.value)

    // Create map instance
    map.value = new google.maps.Map(mapContainer.value, {
      center: { lat: -25.2744, lng: 133.7751 }, // Center of Australia
      zoom: 4,
      mapTypeId: mapType.value,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }]
        }
      ],
      // Disable street view control
      streetViewControl: false,
      mapTypeControl: true,
      fullscreenControl: true,
      zoomControl: true,
      scaleControl: false,
      rotateControl: false,
      clickableIcons: false
    })

    // Add markers for plans
    addPlanMarkers()
    
    isLoading.value = false
  } catch (err) {
    console.error('Error initializing map:', err)
    error.value = err.message || 'Failed to load map'
    isLoading.value = false
  }
}

// Load Google Maps API script
const loadGoogleMapsScript = () => {
  return new Promise((resolve, reject) => {
    // Check if script is already loaded
    if (window.google && window.google.maps) {
      resolve()
      return
    }

    // Check if script is already being loaded
    if (document.querySelector('script[src*="maps.googleapis.com"]')) {
      // Wait for the existing script to load
      const checkLoaded = () => {
        if (window.google && window.google.maps) {
          resolve()
        } else {
          setTimeout(checkLoaded, 100)
        }
      }
      checkLoaded()
      return
    }

    // Create and load the script
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&libraries=maps,marker&language=en`
    script.async = true
    script.defer = true
    
    script.onload = () => {
      resolve()
    }
    
    script.onerror = () => {
      reject(new Error('Failed to load Google Maps API'))
    }
    
    document.head.appendChild(script)
  })
}

// Add markers for travel plans
const addPlanMarkers = async () => {
  if (!map.value) return

  // Clear existing markers
  clearMarkers()

  // City coordinates mapping with more details
  const cityCoordinates = {
    'Sydney': { lat: -33.8688, lng: 151.2093, attractions: ['Opera House', 'Harbour Bridge', 'Bondi Beach'] },
    'Melbourne': { lat: -37.8136, lng: 144.9631, attractions: ['Federation Square', 'Royal Botanic Gardens', 'St Kilda Beach'] },
    'Brisbane': { lat: -27.4698, lng: 153.0251, attractions: ['South Bank', 'Lone Pine Koala Sanctuary', 'Story Bridge'] },
    'Canberra': { lat: -35.2809, lng: 149.1300, attractions: ['Parliament House', 'War Memorial', 'National Gallery'] },
    'Perth': { lat: -31.9505, lng: 115.8605, attractions: ['Kings Park', 'Swan River', 'Fremantle'] },
    'Adelaide': { lat: -34.9285, lng: 138.6007, attractions: ['Adelaide Oval', 'Central Market', 'Glenelg Beach'] },
    'Darwin': { lat: -12.4634, lng: 130.8456, attractions: ['Mindil Beach', 'Crocosaurus Cove', 'Litchfield National Park'] },
    'Hobart': { lat: -42.8821, lng: 147.3272, attractions: ['Salamanca Market', 'Mount Wellington', 'MONA'] }
  }


  // Add markers for unfinished plans (gray flags)
  props.plans.forEach((plan) => {
    const destination = plan.destination || plan.formData?.destination
    const coords = cityCoordinates[destination]
    
    if (coords) {
      const marker = new google.maps.Marker({
        position: coords,
        map: map.value,
        title: plan.title || `${destination} Trip (Planned)`,
        icon: {
          url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
            <svg width="32" height="40" viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 2 L28 2 L24 8 L28 14 L4 14 Z" fill="#666" stroke="#999" stroke-width="1"/>
              <path d="M4 14 L8 20 L4 26 L4 14 Z" fill="#666" stroke="#999" stroke-width="1"/>
            </svg>
          `)}`,
          scaledSize: new google.maps.Size(32, 40),
          anchor: new google.maps.Point(16, 20)
        }
      })

      // Create enhanced info window
      const attractions = coords.attractions ? coords.attractions.slice(0, 3).join(', ') : 'Various attractions'
      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div style="padding: 12px; font-family: Arial, sans-serif; max-width: 300px;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
              <div style="width: 8px; height: 8px; background: #909399; border-radius: 50%; margin-right: 8px;"></div>
              <h3 style="margin: 0; color: #333; font-size: 16px;">${plan.title || `${destination} Trip`}</h3>
            </div>
            <div style="margin-bottom: 8px;">
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>📍 Destination:</strong> ${destination}</p>
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>⏱️ Duration:</strong> ${plan.duration || plan.formData?.duration || '0 days'}</p>
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>📅 Date:</strong> ${plan.date || 'TBD'}</p>
            </div>
            <div style="background: #f5f5f5; padding: 8px; border-radius: 4px; margin-bottom: 8px;">
              <p style="margin: 0; color: #555; font-size: 12px;"><strong>🎯 Key Attractions:</strong></p>
              <p style="margin: 4px 0 0; color: #777; font-size: 11px;">${attractions}</p>
            </div>
            <div style="text-align: center;">
              <span style="background: #909399; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">PLANNED</span>
            </div>
          </div>
        `
      })

      marker.addListener('click', () => {
        infoWindow.open(map.value, marker)
      })

      markers.value.push({ marker, infoWindow })
    }
  })

  // Add markers for finished plans (colored flags)
  props.finishedPlans.forEach((plan) => {
    const destination = plan.destination || plan.formData?.destination
    const coords = cityCoordinates[destination]
    
    if (coords) {
      const marker = new google.maps.Marker({
        position: coords,
        map: map.value,
        title: plan.title || `${destination} Trip (Completed)`,
        icon: {
          url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
            <svg width="32" height="40" viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 2 L28 2 L24 8 L28 14 L4 14 Z" fill="#52c41a" stroke="#389e0d" stroke-width="1"/>
              <path d="M4 14 L8 20 L4 26 L4 14 Z" fill="#52c41a" stroke="#389e0d" stroke-width="1"/>
            </svg>
          `)}`,
          scaledSize: new google.maps.Size(32, 40),
          anchor: new google.maps.Point(16, 20)
        }
      })

      // Create enhanced info window for completed plans
      const attractions = coords.attractions ? coords.attractions.slice(0, 3).join(', ') : 'Various attractions'
      const infoWindow = new google.maps.InfoWindow({
        content: `
          <div style="padding: 12px; font-family: Arial, sans-serif; max-width: 300px;">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
              <div style="width: 8px; height: 8px; background: #67c23a; border-radius: 50%; margin-right: 8px;"></div>
              <h3 style="margin: 0; color: #333; font-size: 16px;">${plan.title || `${destination} Trip`}</h3>
            </div>
            <div style="margin-bottom: 8px;">
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>📍 Destination:</strong> ${destination}</p>
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>⏱️ Duration:</strong> ${plan.duration || plan.formData?.duration || '0 days'}</p>
              <p style="margin: 0 0 4px; color: #666; font-size: 14px;"><strong>📅 Date:</strong> ${plan.date || 'Completed'}</p>
            </div>
            <div style="background: #f0f9ff; padding: 8px; border-radius: 4px; margin-bottom: 8px;">
              <p style="margin: 0; color: #555; font-size: 12px;"><strong>🎯 Key Attractions:</strong></p>
              <p style="margin: 4px 0 0; color: #777; font-size: 11px;">${attractions}</p>
            </div>
            <div style="text-align: center;">
              <span style="background: #67c23a; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">✓ COMPLETED</span>
            </div>
          </div>
        `
      })

      marker.addListener('click', () => {
        infoWindow.open(map.value, marker)
      })

      markers.value.push({ marker, infoWindow })
    }
  })
}

// Clear all markers
const clearMarkers = () => {
  markers.value.forEach(({ marker, infoWindow }) => {
    marker.setMap(null)
    infoWindow.close()
  })
  markers.value = []
}


// Toggle map type
const toggleMapType = () => {
  if (!map.value) return
  
  mapType.value = mapType.value === 'roadmap' ? 'satellite' : 'roadmap'
  map.value.setMapTypeId(mapType.value)
}

// Computed properties
const hasPlans = computed(() => (props.plans && props.plans.length > 0) || (props.finishedPlans && props.finishedPlans.length > 0))

// Watch for plans changes
watch([() => props.plans, () => props.finishedPlans], async () => {
  if (map.value) {
    await addPlanMarkers()
  }
}, { deep: true })

// Lifecycle
onMounted(async () => {
  // 等待DOM完全渲染
  await nextTick()
  
  // 添加延迟确保DOM元素可用
  setTimeout(() => {
    if (mapContainer.value) {
      initMap()
    } else {
      console.warn('Map container not found, retrying...')
      // 如果容器还没准备好，再等一会儿
      setTimeout(() => {
        if (mapContainer.value) {
          initMap()
        } else {
          console.error('Map container still not found after retry')
          error.value = 'Map container not available'
          isLoading.value = false
        }
      }, 500)
    }
  }, 100)
})

onUnmounted(() => {
  clearMarkers()
})
</script>

<style scoped>
.google-map-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.map-header h2 {
  color: #333;
  margin: 0;
  font-size: 18px;
}

.map-controls {
  display: flex;
  gap: 8px;
}

.map-legend {
  display: flex;
  gap: 16px;
  padding: 8px 16px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
  font-size: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #555;
}

.legend-icon {
  width: 16px;
  height: 20px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.legend-icon.planned {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg width='16' height='20' viewBox='0 0 16 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2 1 L14 1 L12 4 L14 7 L2 7 Z' fill='%23666' stroke='%23999' stroke-width='0.5'/%3E%3Cpath d='M2 7 L4 10 L2 13 L2 7 Z' fill='%23666' stroke='%23999' stroke-width='0.5'/%3E%3C/svg%3E");
}

.legend-icon.completed {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg width='16' height='20' viewBox='0 0 16 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2 1 L14 1 L12 4 L14 7 L2 7 Z' fill='%2352c41a' stroke='%23389e0d' stroke-width='0.5'/%3E%3Cpath d='M2 7 L4 10 L2 13 L2 7 Z' fill='%2352c41a' stroke='%23389e0d' stroke-width='0.5'/%3E%3C/svg%3E");
}

.map-box {
  flex: 1;
  position: relative;
  min-height: 400px;
}

.map-box.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.map-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #666;
}

.map-loading .el-icon {
  font-size: 24px;
}

.map-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #ff6b6b;
  padding: 20px;
  text-align: center;
}

.map-error .el-icon {
  font-size: 24px;
}

/* Responsive design */
@media (max-width: 768px) {
  .map-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .map-controls {
    justify-content: center;
  }
  
  .map-legend {
    justify-content: center;
    gap: 20px;
  }
  
  .map-box {
    min-height: 300px;
  }
}
</style>
