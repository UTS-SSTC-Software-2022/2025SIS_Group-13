<template>
  <div class="earth-globe-page">
    <!-- 3D Globe Container -->
    <div ref="container" class="globe-container"></div>

    <!-- Main Title and Tagline -->
    <div class="title-overlay">
      <h1 class="main-title">LeisurA</h1>
      <p class="tagline">Plan smarter. Travel freer. Remember deeper.</p>
    </div>
  </div>
</template>

<script setup>
// ==========================================
// IMPORTS & COMPOSABLES
// ==========================================
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useThreeJsGlobe } from './composables/useThreeJsGlobe'

// ==========================================
// COMPONENT STATE
// ==========================================
const container = ref(null)

// ==========================================
// THREE.JS GLOBE SETUP
// ==========================================
const { initializeGlobe, cleanup } = useThreeJsGlobe()

// ==========================================
// LIFECYCLE HOOKS
// ==========================================
onMounted(() => {
  if (container.value) {
    initializeGlobe(container.value)
  }
})

onBeforeUnmount(() => {
  cleanup()
})
</script>

<style scoped>
/* Page Layout */
.earth-globe-page {
  position: relative;
  width: 100%;
  height: 100dvh;
  overflow: hidden;
}

/* 3D Globe Container */
.globe-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Main Title Overlay */
.title-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  z-index: 5;
  pointer-events: none;
}



.main-title {
  font-family: "Outfit","Inter","SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  font-weight: 900;
  font-size: clamp(4rem, 11vw, 7rem);
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 1rem 0;
  background: linear-gradient(180deg, #f8ffa1 0%, #cfe607 55%, #9fb605 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.03em;
  line-height: 0.9;
  -webkit-text-stroke: 1px rgba(0,0,0,.45);   

}

.tagline {
  font-family: "Outfit","Inter","SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  font-weight: 900;
  font-size: clamp(1.3rem, 2.5vw, 1.7rem);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: 0.02em;
  line-height: 1.4;
  width: clamp(300px,80vw,900px);
}

/* Animation Effects */
.main-title {
  animation: fadeInUp 2s ease-out 0.5s both;
}

.tagline {
  animation: fadeInUp 2s ease-out 0.5s both;
}


@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
