// ==========================================
// THREE.JS GLOBE COMPOSABLE
// ==========================================
// This composable handles all Three.js related functionality
// for the Earth Globe component, including scene setup, 
// lighting, model loading, animations, and cleanup.

import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

export function useThreeJsGlobe() {
  // ==========================================
  // PRIVATE VARIABLES
  // ==========================================
  let renderer = null
  let scene = null
  let camera = null
  let controls = null
  let mixer = null
  let animationId = null
  let resizeHandler = null
  let globeModel = null // Store reference to the globe model for scaling

  // ==========================================
  // RESPONSIVE SCALING UTILITIES
  // ==========================================
  function getResponsiveGlobeScale() {
    const width = window.innerWidth
    
    // Define breakpoints (matching Tailwind CSS md breakpoint: 768px)
    const MD_BREAKPOINT = 768
    const SM_BREAKPOINT = 640
    
    // Return different scales based on screen size
    if (width < SM_BREAKPOINT) {
      return 0.55  // Smaller on mobile
    } else if (width < MD_BREAKPOINT) {
      return 0.7  // Medium size on tablet
    } else {
      return 0.85 // Original size on desktop
    }
  }

  function updateGlobeScale() {
    if (globeModel) {
      const newScale = getResponsiveGlobeScale()
      globeModel.scale.setScalar(newScale)
    }
  }

  // ==========================================
  // SCENE INITIALIZATION
  // ==========================================
  function initializeScene(container) {
    // Create scene with transparent background
    scene = new THREE.Scene()
    scene.background = null // Transparent background for overlay effect
    
    // Setup camera with proper aspect ratio
    camera = new THREE.PerspectiveCamera(
      60, 
      container.clientWidth / container.clientHeight, 
      0.1, 
      1000
    )
    camera.position.set(2.5, 1.8, 3.5)
    
    return { scene, camera }
  }

  // ==========================================
  // RENDERER SETUP
  // ==========================================
  function initializeRenderer(container) {
    renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true // Enable transparency
    })
    
    renderer.setSize(container.clientWidth, container.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.outputColorSpace = THREE.SRGBColorSpace
    renderer.toneMapping = THREE.ACESFilmicToneMapping
    renderer.toneMappingExposure = 2
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    
    container.appendChild(renderer.domElement)
    
    return renderer
  }

  // ==========================================
  // LIGHTING SETUP
  // ==========================================
  function setupLighting() {
    // Hemisphere light for natural ambient lighting
    const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0xA6A6A6, 0.8)
    hemisphereLight.position.set(0, 1, 0)
    scene.add(hemisphereLight)

    // Directional light for dramatic shadows
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0)
    directionalLight.position.set(5, 10, 7)
    directionalLight.castShadow = true
    
    // Configure shadow properties
    directionalLight.shadow.mapSize.width = 2048
    directionalLight.shadow.mapSize.height = 2048
    directionalLight.shadow.camera.near = 0.5
    directionalLight.shadow.camera.far = 50
    
    scene.add(directionalLight)
    
    return { hemisphereLight, directionalLight }
  }

  // ==========================================
  // CONTROLS SETUP
  // ==========================================
  function setupControls(camera, renderer) {
    controls = new OrbitControls(camera, renderer.domElement)
    
    // Configure control behavior
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.autoRotate = true
    controls.autoRotateSpeed = 0.3
    controls.enableZoom = false // Disable zoom for consistent view
    controls.enablePan = false  // Disable panning for focused experience
    
    // Set rotation limits for better UX
    controls.minPolarAngle = Math.PI * 0.3
    controls.maxPolarAngle = Math.PI * 0.7
    
    return controls
  }

  // ==========================================
  // MODEL LOADING
  // ==========================================
  function loadGlobeModel() {
    const loader = new GLTFLoader()
    
    loader.load(
      'src/assets/models/scene.gltf',
      (gltf) => {
        const root = gltf.scene
        
        // Configure model properties
        root.traverse((obj) => {
          if (obj.isMesh) {
            obj.castShadow = true
            obj.receiveShadow = true
            
            // Enhance material properties if needed
            if (obj.material) {
              obj.material.needsUpdate = true
            }
          }
        })
        
        // Store reference to the globe model for responsive scaling
        globeModel = root
        
        // Apply initial responsive scale
        const initialScale = getResponsiveGlobeScale()
        root.scale.setScalar(initialScale)
        
        // Add model to scene
        scene.add(root)
        
        // Setup animations if available
        setupAnimations(gltf, root)
        
        console.log('✅ Globe model loaded successfully')
      },
      (progress) => {
        const percentage = Math.round((progress.loaded / progress.total) * 100)
        console.log(`🌍 Loading globe: ${percentage}%`)
      },
      (error) => {
        console.error('❌ Error loading globe model:', error)
      }
    )
  }

  // ==========================================
  // ANIMATION SETUP
  // ==========================================
  function setupAnimations(gltf, root) {
    if (gltf.animations && gltf.animations.length > 0) {
      mixer = new THREE.AnimationMixer(root)
      
      // Play all available animations
      gltf.animations.forEach((clip) => {
        const action = mixer.clipAction(clip)
        action.play()
      })
      
      console.log(`🎬 Loaded ${gltf.animations.length} animations:`, 
                  gltf.animations.map(clip => clip.name))
    } else {
      console.log('ℹ️ No animations found in the model')
    }
  }

  // ==========================================
  // RESIZE HANDLING
  // ==========================================
  function setupResizeHandler(container) {
    resizeHandler = () => {
      if (!container || !camera || !renderer) return
      
      const width = container.clientWidth
      const height = container.clientHeight
      
      // Update camera aspect ratio
      camera.aspect = width / height
      camera.updateProjectionMatrix()
      
      // Update renderer size
      renderer.setSize(width, height)
      
      // Update globe scale based on new window size
      updateGlobeScale()
    }
    
    window.addEventListener('resize', resizeHandler)
    return resizeHandler
  }

  // ==========================================
  // ANIMATION LOOP
  // ==========================================
  function startAnimationLoop() {
    const clock = new THREE.Clock()
    
    const animate = () => {
      animationId = requestAnimationFrame(animate)
      
      const deltaTime = clock.getDelta()
      
      // Update controls with damping
      if (controls) controls.update()
      
      // Update model animations
      if (mixer) mixer.update(deltaTime)
      
      // Render the scene
      if (renderer && scene && camera) {
        renderer.render(scene, camera)
      }
    }
    
    animate()
  }

  // ==========================================
  // PUBLIC API
  // ==========================================
  function initializeGlobe(container) {
    try {
      // Initialize core Three.js components
      initializeScene(container)
      initializeRenderer(container)
      
      // Setup lighting and controls
      setupLighting()
      setupControls(camera, renderer)
      
      // Load the globe model
      loadGlobeModel()
      
      // Setup responsive behavior
      setupResizeHandler(container)
      
      // Start the animation loop
      startAnimationLoop()
      
      console.log('🚀 Three.js Globe initialized successfully')
      
    } catch (error) {
      console.error('❌ Failed to initialize Three.js Globe:', error)
    }
  }

  function cleanup() {
    try {
      // Stop animation loop
      if (animationId) {
        cancelAnimationFrame(animationId)
        animationId = null
      }
      
      // Remove resize listener
      if (resizeHandler) {
        window.removeEventListener('resize', resizeHandler)
        resizeHandler = null
      }
      
      // Stop animations
      if (mixer) {
        mixer.stopAllAction()
        mixer = null
      }
      
      // Dispose of Three.js resources
      if (renderer) {
        renderer.dispose()
        
        // Remove canvas from DOM
        if (renderer.domElement && renderer.domElement.parentNode) {
          renderer.domElement.parentNode.removeChild(renderer.domElement)
        }
        
        renderer = null
      }
      
      // Clear controls
      if (controls) {
        controls.dispose()
        controls = null
      }
      
      // Clear scene references
      scene = null
      camera = null
      globeModel = null
      
      console.log('🧹 Three.js Globe cleaned up successfully')
      
    } catch (error) {
      console.error('❌ Error during Three.js cleanup:', error)
    }
  }

  // Return public API
  return {
    initializeGlobe,
    cleanup
  }
}
