<template>
  <div class="google-map-container">
    <div ref="mapContainer" class="map"></div>
    <div class="map-controls">
      <div class="control-group">
        <button class="control-btn" @click="toggleLayers">
          <el-icon><Layers /></el-icon>
        </button>
        <button class="control-btn" @click="centerOnLocation">
          <el-icon><Location /></el-icon>
        </button>
        <button class="control-btn" @click="zoomIn">
          <el-icon><Plus /></el-icon>
        </button>
        <button class="control-btn" @click="zoomOut">
          <el-icon><Minus /></el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'
import { Layers, Location, Plus, Minus } from '@element-plus/icons-vue'

const mapContainer = ref(null)
let map = null
let markers = []

// Google Maps API Key - You should replace this with your actual API key
const GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

/**
 * Initialize Google Map
 */
const initMap = async () => {
  try {
    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places', 'geometry']
    })

    const { Map } = await loader.importLibrary('maps')
    const { Marker } = await loader.importLibrary('marker')

    // Initialize map centered on Asia
    map = new Map(mapContainer.value, {
      center: { lat: 35.0, lng: 105.0 }, // Center on Asia
      zoom: 4,
      mapTypeId: 'roadmap',
      styles: [
        {
          featureType: 'water',
          elementType: 'geometry',
          stylers: [{ color: '#e9e9e9' }]
        },
        {
          featureType: 'land',
          elementType: 'geometry',
          stylers: [{ color: '#f5f5f5' }]
        }
      ]
    })

    // Add sample markers for popular destinations
    addSampleMarkers(Marker)

  } catch (error) {
    console.error('Error loading Google Maps:', error)
    // Fallback: show a placeholder
    mapContainer.value.innerHTML = `
      <div class="map-placeholder">
        <div class="placeholder-content">
          <h3>Map Loading...</h3>
          <p>Please configure your Google Maps API key</p>
          <small>Add your API key in GoogleMap.vue component</small>
        </div>
      </div>
    `
  }
}

/**
 * Add sample markers for popular destinations
 */
const addSampleMarkers = (Marker) => {
  const destinations = [
    { lat: 35.6762, lng: 139.6503, name: 'Tokyo', icon: '🏯' },
    { lat: 1.3521, lng: 103.8198, name: 'Singapore', icon: '🌴' },
    { lat: -8.3405, lng: 115.0920, name: 'Bali', icon: '🏝️' },
    { lat: 25.2048, lng: 55.2708, name: 'Dubai', icon: '🏙️' },
    { lat: 35.0116, lng: 135.7681, name: 'Kyoto', icon: '⛩️' }
  ]

  destinations.forEach(destination => {
    const marker = new Marker({
      position: { lat: destination.lat, lng: destination.lng },
      map: map,
      title: destination.name,
      icon: {
        url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
          <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" fill="#409eff" stroke="white" stroke-width="2"/>
            <text x="20" y="26" text-anchor="middle" font-size="16">${destination.icon}</text>
          </svg>
        `)}`,
        scaledSize: new google.maps.Size(40, 40),
        anchor: new google.maps.Point(20, 20)
      }
    })

    markers.push(marker)
  })
}

/**
 * Toggle map layers
 */
const toggleLayers = () => {
  if (map) {
    const currentMapType = map.getMapTypeId()
    const newMapType = currentMapType === 'roadmap' ? 'satellite' : 'roadmap'
    map.setMapTypeId(newMapType)
  }
}

/**
 * Center map on user's location
 */
const centerOnLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        if (map) {
          map.setCenter({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          })
          map.setZoom(10)
        }
      },
      (error) => {
        console.error('Error getting location:', error)
        // Fallback to Sydney
        if (map) {
          map.setCenter({ lat: -33.8688, lng: 151.2093 })
          map.setZoom(10)
        }
      }
    )
  }
}

/**
 * Zoom in
 */
const zoomIn = () => {
  if (map) {
    const currentZoom = map.getZoom()
    map.setZoom(currentZoom + 1)
  }
}

/**
 * Zoom out
 */
const zoomOut = () => {
  if (map) {
    const currentZoom = map.getZoom()
    map.setZoom(currentZoom - 1)
  }
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  // Clean up markers
  markers.forEach(marker => marker.setMap(null))
  markers = []
})
</script>

<style scoped>
.google-map-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.map {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 8px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.control-btn:hover {
  background: #f5f5f5;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.control-btn:active {
  transform: translateY(0);
}

.map-placeholder {
  width: 100%;
  height: 100%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  text-align: center;
  color: #666;
}

.placeholder-content h3 {
  margin-bottom: 1rem;
  color: #333;
}

.placeholder-content p {
  margin-bottom: 0.5rem;
}

.placeholder-content small {
  color: #999;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .map-controls {
    bottom: 10px;
    right: 10px;
  }
  
  .control-group {
    flex-direction: row;
    gap: 4px;
    padding: 4px;
  }
  
  .control-btn {
    width: 36px;
    height: 36px;
  }
}
</style>
