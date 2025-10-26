<template>
  <div class="route-map-demo">
    <div class="demo-header">
      <h1>🗺️ Google Maps 路线展示功能演示</h1>
      <p>基于时间顺序的地点标记和路线显示</p>
    </div>

    <div class="demo-content">
      <RouteMap 
        :day-data="demoDayData" 
        :itinerary-data="demoItineraryData"
      />
    </div>

    <div class="demo-info">
      <h3>功能特性：</h3>
      <ul>
        <li>✅ 基于Google Maps API的真实地图显示</li>
        <li>✅ 按时间顺序自动排序地点</li>
        <li>✅ 自定义标记点（开始/中间/结束点不同颜色）</li>
        <li>✅ 自动绘制路线连接各个地点</li>
        <li>✅ 点击标记显示详细信息窗口</li>
        <li>✅ 路线动画播放功能</li>
        <li>✅ 时间线导航</li>
        <li>✅ 地图类型切换（道路/卫星）</li>
        <li>✅ 响应式设计，支持移动端</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RouteMap from '@/components/map/RouteMap.vue'

// Demo data for testing
const demoDayData = ref({
  day: 1,
  date: "2024-01-15",
  overview: "Sydney City Exploration",
  weather: {
    temperature: 28,
    condition: "Sunny"
  },
  activities: [
    {
      time: "09:00",
      title: "Arrive at Sydney Airport",
      description: "Check into hotel and freshen up",
      type: "Transportation",
      location: {
        name: "Sydney Airport",
        address: "Sydney Airport, NSW 2020"
      }
    },
    {
      time: "11:00",
      title: "Circular Quay & Opera House",
      description: "Visit the iconic Sydney Opera House and take photos",
      type: "Culture",
      location: {
        name: "Sydney Opera House",
        address: "Bennelong Point, Sydney NSW 2000"
      }
    },
    {
      time: "14:00",
      title: "Lunch at The Rocks",
      description: "Traditional Australian lunch with harbor views",
      type: "Dining",
      location: {
        name: "The Rocks",
        address: "The Rocks, Sydney NSW 2000"
      }
    },
    {
      time: "16:00",
      title: "Harbor Bridge Walk",
      description: "Walk across the Sydney Harbour Bridge",
      type: "Adventure",
      location: {
        name: "Sydney Harbour Bridge",
        address: "Sydney Harbour Bridge, Sydney NSW 2000"
      }
    },
    {
      time: "18:00",
      title: "Darling Harbour",
      description: "Evening waterfront dining and entertainment",
      type: "Dining",
      location: {
        name: "Darling Harbour",
        address: "Darling Harbour, Sydney NSW 2000"
      }
    }
  ]
})

const demoItineraryData = ref({
  destination: "Sydney, Australia",
  duration: 1,
  travelers: 2,
  estimatedBudget: 300
})
</script>

<style scoped>
.route-map-demo {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
  padding: 2rem;
  color: #e6edf3;
}

.demo-header {
  text-align: center;
  margin-bottom: 2rem;
}

.demo-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.demo-header p {
  font-size: 1.1rem;
  color: #a0aec0;
}

.demo-content {
  max-width: 1200px;
  margin: 0 auto 3rem;
}

.demo-info {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(10px);
}

.demo-info h3 {
  color: #e6edf3;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.demo-info ul {
  list-style: none;
  padding: 0;
}

.demo-info li {
  padding: 0.5rem 0;
  color: #a0aec0;
  font-size: 1rem;
  line-height: 1.5;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .route-map-demo {
    padding: 1rem;
  }
  
  .demo-header h1 {
    font-size: 2rem;
  }
  
  .demo-info {
    padding: 1.5rem;
  }
}
</style>
