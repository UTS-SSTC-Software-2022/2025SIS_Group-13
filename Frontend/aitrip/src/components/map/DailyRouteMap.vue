<template>
  <div class="daily-route-map-container">
    <div class="daily-map-header" @click="toggleMapExpansion">
      <div class="daily-map-info">
        <h4 class="daily-map-title">🗺️ Day Route Map</h4>
        <p class="daily-map-subtitle">View today's travel route and locations</p>
      </div>
      <el-icon class="daily-map-expand-icon" :class="{ 'rotated': isExpanded }">
        <ArrowDown />
      </el-icon>
    </div>
    
    <el-collapse-transition>
      <div v-show="isExpanded" class="daily-map-content">
        <!-- Google Maps Container -->
        <div class="google-map-container">
          <div ref="mapContainer" class="map-container"></div>
          <div v-if="mapLoading" class="map-loading">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>Loading map...</span>
          </div>
        </div>
        
        <!-- Route summary -->
        <div class="daily-route-summary">
          <div class="summary-item">
            <el-icon class="summary-icon"><Location /></el-icon>
            <div>
              <div class="summary-label">Locations</div>
              <div class="summary-value">{{ dayLocations.length }}</div>
            </div>
          </div>
          <div class="summary-item">
            <el-icon class="summary-icon"><Clock /></el-icon>
            <div>
              <div class="summary-label">Total Time</div>
              <div class="summary-value">{{ estimatedTotalTime }}</div>
            </div>
          </div>
          <div class="summary-item">
            <el-icon class="summary-icon"><Position /></el-icon>
            <div>
              <div class="summary-label">Distance</div>
              <div class="summary-value">{{ actualDistance }}</div>
            </div>
          </div>
        </div>
      </div>
    </el-collapse-transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { setOptions, importLibrary } from '@googlemaps/js-api-loader'
import { ArrowDown, Location, Clock, Position, Loading } from '@element-plus/icons-vue'

// Google Maps API Key
const googleMapsApiKey = 'AIzaSyCvUOTSTS_KRZZi5kTbKoQpWsM0QLq2VfM'

// Props
const props = defineProps({
  dayData: {
    type: Object,
    default: null
  }
})

// Reactive data
const isExpanded = ref(false)
const mapContainer = ref(null)
const map = ref(null)
const mapLoading = ref(false)
const markers = ref([])
const directionsService = ref(null)
const directionsRenderer = ref(null)
const actualDistance = ref('0 km')

// Google Maps API Key - Get from environment variables
// Computed properties
const dayLocations = computed(() => {
  if (!props.dayData || !props.dayData.activities) return []
  
  return props.dayData.activities
    .filter(activity => activity.location && activity.location.name)
    .map((activity, index) => ({
      name: activity.location.name,
      time: activity.time,
      address: activity.location.address,
      type: activity.type,
      coordinates: activity.location.coordinates || null,
      sequence: index + 1
    }))
})

const estimatedTotalTime = computed(() => {
  if (!props.dayData || !props.dayData.activities) return '0h'
  
  // Simple estimation based on activity count
  const activityCount = props.dayData.activities.length
  const hours = Math.max(1, Math.ceil(activityCount * 1.5))
  return `${hours}h`
})

// Methods
const toggleMapExpansion = async () => {
  isExpanded.value = !isExpanded.value
  
  if (isExpanded.value && !map.value) {
    await nextTick()
    await initializeMap()
  }
}

const initializeMap = async () => {
  if (!mapContainer.value || map.value) return
  
  mapLoading.value = true
  
  try {
    // Set Google Maps options
    setOptions({
      apiKey: googleMapsApiKey,
      version: 'weekly'
    })

    // Import required libraries
    const { Map } = await importLibrary('maps')
    const { Marker } = await importLibrary('marker')
    const { DirectionsService, DirectionsRenderer } = await importLibrary('routes')
    
    // Wait for DOM to be ready
    await nextTick()
    
    if (!mapContainer.value) {
      throw new Error('Map container not found')
    }

    // Create map instance
    map.value = new Map(mapContainer.value, {
      center: { lat: -37.8136, lng: 144.9631 }, // Default to Melbourne
      zoom: 12,
      mapTypeId: 'roadmap',
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }]
        }
      ],
      // Disable street view control (hide the little man icon)
      streetViewControl: false,
      // Disable other controls that might show Chinese text
      mapTypeControl: true,
      fullscreenControl: true,
      zoomControl: true,
      scaleControl: false,
      rotateControl: false,
      clickableIcons: false
    })

    // Initialize directions service
    directionsService.value = new DirectionsService()
    directionsRenderer.value = new DirectionsRenderer({
      suppressMarkers: true,
      polylineOptions: {
        strokeColor: '#409eff',
        strokeWeight: 4,
        strokeOpacity: 0.8
      }
    })
    
    directionsRenderer.value.setMap(map.value)
    
    // Load locations and draw route
    await loadLocationsAndDrawRoute()
    
    mapLoading.value = false
  } catch (error) {
    console.error('Error initializing Google Maps:', error)
    mapLoading.value = false
  }
}


const loadLocationsAndDrawRoute = async () => {
  if (!map.value || dayLocations.value.length === 0) return
  
  try {
    // Import required libraries
    const { Marker } = await importLibrary('marker')
    const { InfoWindow } = await importLibrary('maps')
    
    // Clear existing markers
    markers.value.forEach(marker => marker.setMap(null))
    markers.value = []
    
    const locations = dayLocations.value
    
    // If we have coordinates, use them; otherwise geocode addresses
    const waypoints = []
    
    for (let i = 0; i < locations.length; i++) {
      const location = locations[i]
      let position = null
      
      if (location.coordinates) {
        position = new google.maps.LatLng(location.coordinates.lat, location.coordinates.lng)
      } else {
        // Geocode the address
        try {
          const geocoder = new google.maps.Geocoder()
          const result = await new Promise((resolve, reject) => {
            geocoder.geocode({ 
              address: location.address || location.name,
              language: 'en',
              region: 'AU'
            }, (results, status) => {
              if (status === 'OK' && results[0]) {
                resolve(results[0].geometry.location)
              } else {
                reject(new Error(`Geocoding failed: ${status}`))
              }
            })
          })
          position = result
        } catch (error) {
          console.error(`Failed to geocode ${location.name}:`, error)
          continue
        }
      }
      
      // Create marker with sequence number
      const marker = new Marker({
        position: position,
        map: map.value,
        title: `${location.sequence}. ${location.name}`,
        label: {
          text: location.sequence.toString(),
          color: 'white',
          fontWeight: 'bold',
          fontSize: '12px'
        },
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 20,
          fillColor: getMarkerColor(location.sequence, locations.length),
          fillOpacity: 1,
          strokeColor: 'white',
          strokeWeight: 2
        }
      })
      
      // Create info window
      const infoWindow = new InfoWindow({
        content: `
          <div style="padding: 8px;">
            <h4 style="margin: 0 0 4px 0; color: #333;">${location.sequence}. ${location.name}</h4>
            <p style="margin: 0 0 4px 0; color: #666; font-size: 12px;">${location.time}</p>
            <p style="margin: 0; color: #888; font-size: 11px;">${location.address || ''}</p>
          </div>
        `
      })
      
      marker.addListener('click', () => {
        infoWindow.open(map.value, marker)
      })
      
      markers.value.push(marker)
      waypoints.push(position)
    }
    
    // Draw route if we have multiple locations
    if (waypoints.length > 1) {
      await drawRoute(waypoints)
    } else if (waypoints.length === 1) {
      // Center map on single location
      map.value.setCenter(waypoints[0])
      map.value.setZoom(15)
    }
    
  } catch (error) {
    console.error('Error loading locations and drawing route:', error)
  }
}

const drawRoute = async (waypoints) => {
  if (!directionsService.value || waypoints.length < 2) return
  
  try {
    const request = {
      origin: waypoints[0],
      destination: waypoints[waypoints.length - 1],
      waypoints: waypoints.slice(1, -1).map(point => ({
        location: point,
        stopover: true
      })),
      travelMode: 'DRIVING',
      optimizeWaypoints: false // Keep original order
    }
    
    const result = await new Promise((resolve, reject) => {
      directionsService.value.route(request, (result, status) => {
        if (status === 'OK') {
          resolve(result)
        } else {
          reject(new Error(`Directions request failed: ${status}`))
        }
      })
    })
    
    if (directionsRenderer.value) {
      directionsRenderer.value.setDirections(result)
    }
    
    // Calculate total distance
    if (result.routes && result.routes[0] && result.routes[0].legs) {
      let totalDistance = 0
      result.routes[0].legs.forEach(leg => {
        if (leg.distance && leg.distance.value) {
          totalDistance += leg.distance.value
        }
      })
      
      actualDistance.value = `${Math.round(totalDistance / 1000)} km`
    }
    
  } catch (error) {
    console.error('Error drawing route:', error)
    // Fallback: show estimated distance
    const estimatedDistance = (waypoints.length - 1) * 5
    actualDistance.value = `~${estimatedDistance} km`
  }
}

const getMarkerColor = (sequence, total) => {
  if (total === 1) return '#409eff'
  if (sequence === 1) return '#67c23a' // Start - Green
  if (sequence === total) return '#f56c6c' // End - Red
  return '#409eff' // Middle - Blue
}

// Watch for changes in dayData
watch(() => props.dayData, async () => {
  if (map.value && isExpanded.value) {
    await loadLocationsAndDrawRoute()
  }
}, { deep: true })

// Watch for expansion changes
watch(isExpanded, async (newValue) => {
  if (newValue && !map.value) {
    await nextTick()
    await initializeMap()
  }
})

// Cleanup on component unmount
onUnmounted(() => {
  // Clean up markers
  if (markers.value) {
    markers.value.forEach(marker => marker.setMap(null))
  }
  
  // Clean up directions renderer
  if (directionsRenderer.value) {
    directionsRenderer.value.setMap(null)
  }
})
</script>

<style scoped>
.daily-route-map-container {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(8px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.daily-route-map-container:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.daily-map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.04);
  transition: all 0.3s ease;
  min-height: 60px;
}

.daily-map-header:hover {
  background: rgba(255, 255, 255, 0.08);
}

.daily-map-info {
  flex: 1;
}

.daily-map-title {
  font-size: 1rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 0 0 0.25rem 0;
}

.daily-map-subtitle {
  font-size: 0.8rem;
  color: #a0aec0;
  margin: 0;
}

.daily-map-expand-icon {
  font-size: 1rem;
  color: #409eff;
  transition: transform 0.3s ease;
}

.daily-map-expand-icon.rotated {
  transform: rotate(180deg);
}

.daily-map-content {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
}

.google-map-container {
  position: relative;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(148, 163, 184, 0.18);
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 12px;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  z-index: 1000;
}

.loading-icon {
  font-size: 24px;
  margin-bottom: 8px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.daily-route-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.summary-item:hover {
  background: rgba(255, 255, 255, 0.09);
  transform: translateY(-1px);
}

.summary-icon {
  font-size: 1.2rem;
  opacity: 0.9;
}

.summary-label {
  font-size: 0.75rem;
  opacity: 0.8;
  color: #a0aec0;
}

.summary-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #e6edf3;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .daily-map-header {
    padding: 0.75rem 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .daily-map-content {
    padding: 1rem;
  }
  
  .google-map-container {
    height: 300px;
    margin-bottom: 1rem;
  }
  
  .daily-route-summary {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}
</style>
