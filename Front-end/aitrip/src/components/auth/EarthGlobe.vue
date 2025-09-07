<template>
  <div class="earth-globe-page">
    <!-- Logo and Brand Header -->
    <header class="brand-header">
      <div class="logo-container">
        <img src="\src\assets\images\LeisurA logo.svg" alt="LeisurA Logo" class="logo" />
        <!-- <h1 class="brand-title">LeisurA</h1> -->
      </div>
    </header>

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

/* Brand Header */
.brand-header {
  position: absolute;
  z-index: 10;
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  width: 10rem;
  height:5rem;
  filter: drop-shadow(0 0 10px rgba(4, 108, 184, 0.3));
}

.brand-title {
  font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 0 20px rgba(4, 108, 184, 0.5);
  letter-spacing: -0.02em;
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
  font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #bc8e02 0%, #bfd004 50%, #e9eb77 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(1, 31, 53, 0.875);
  letter-spacing: -0.03em;
  line-height: 0.9;
}

.tagline {
  font-family: 'Inter', 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.02em;
  line-height: 1.4;
  max-width: 600px;
  margin: 0 auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .brand-header {
    top: 1.5rem;
    left: 1.5rem;
  }
  
  .logo {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .brand-title {
    font-size: 1.5rem;
  }
  
  .title-overlay {
    padding: 0 1rem;
  }
}

@media (max-width: 480px) {
  .brand-header {
    top: 1rem;
    left: 1rem;
  }
  
  .logo-container {
    gap: 0.75rem;
  }
  
  .logo {
    width: 2rem;
    height: 2rem;
  }
  
  .brand-title {
    font-size: 1.3rem;
  }
}

/* Animation Effects */
.main-title {
  animation: titleGlow 4s ease-in-out infinite alternate;
}

.tagline {
  animation: fadeInUp 2s ease-out 0.5s both;
}

@keyframes titleGlow {
  0% {
    text-shadow: 0 0 40px rgba(4, 108, 184, 0.3);
  }
  100% {
    text-shadow: 0 0 60px rgba(4, 108, 184, 0.6), 0 0 100px rgba(70, 163, 247, 0.2);
  }
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
