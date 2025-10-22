# DailyRouteMap Component

## 概述
DailyRouteMap组件是一个基于Google Maps API的路线展示组件，用于显示旅行行程中的地点和路线。

> **注意**: 此组件使用`@googlemaps/js-api-loader`的新函数式API（`setOptions`和`importLibrary`），提供更稳定和现代的Google Maps集成方式。

## 功能特性
- 🗺️ 集成Google Maps API显示真实地图
- 🔢 按时间顺序显示地点序号
- 🛣️ 自动绘制连接各点的路线
- 📍 支持坐标和地址两种定位方式
- 💬 点击标记显示详细信息
- 📱 响应式设计，支持移动端
- ⏱️ 显示实际距离和预估时间
- 🎨 自定义地图样式，隐藏中文标签和街景控制

## 使用方法

### 1. 配置Google Maps API密钥
在项目根目录创建`.env`文件：
```env
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### 2. 在组件中使用
```vue
<template>
  <DailyRouteMap :dayData="dayData" />
</template>

<script setup>
import DailyRouteMap from '@/components/map/DailyRouteMap.vue'

const dayData = {
  activities: [
    {
      location: {
        name: "Melbourne Central",
        address: "Melbourne Central, Melbourne VIC 3000, Australia",
        coordinates: { lat: -37.8102, lng: 144.9631 }
      },
      time: "09:00",
      type: "attraction"
    },
    {
      location: {
        name: "Federation Square",
        address: "Federation Square, Melbourne VIC 3000, Australia",
        coordinates: { lat: -37.8183, lng: 144.9671 }
      },
      time: "11:00",
      type: "attraction"
    }
  ]
}
</script>
```

## Props

### dayData (Object)
包含一天行程数据的对象。

**结构：**
```javascript
{
  activities: [
    {
      location: {
        name: String,        // 地点名称
        address: String,     // 地址（可选）
        coordinates: {       // 坐标（可选）
          lat: Number,
          lng: Number
        }
      },
      time: String,          // 时间
      type: String           // 活动类型
    }
  ]
}
```

## 功能说明

### 地点标记
- 每个地点都会在地图上显示为带序号的圆形标记
- 起始点：绿色标记
- 中间点：蓝色标记  
- 结束点：红色标记
- 点击标记可查看详细信息

### 路线绘制
- 自动连接所有地点形成路线
- 使用Google Maps Directions API计算最优路径
- 显示实际距离而非估算距离

### 地址解析
- 如果提供了坐标，直接使用坐标定位
- 如果没有坐标，使用地址进行地理编码
- 支持多种地址格式

## 样式定制

组件使用CSS变量，可以通过覆盖以下变量来自定义样式：

```css
.daily-route-map-container {
  --primary-color: #409eff;
  --success-color: #67c23a;
  --danger-color: #f56c6c;
  --text-color: #e6edf3;
  --bg-color: rgba(255, 255, 255, 0.04);
}
```

## 技术实现

### API加载方式
组件使用`@googlemaps/js-api-loader`的新函数式API：
- 使用`setOptions()`设置API配置
- 使用`importLibrary()`按需导入所需库
- 提供更稳定和现代的Google Maps集成
- 支持异步加载和错误处理

### 性能优化
- 地图只在用户展开组件时初始化
- 支持API重复使用，避免多次加载
- 智能缓存机制，提高加载速度

### 地图样式配置
组件使用自定义地图样式来优化显示效果：
- **隐藏POI标签**：通过设置`featureType: 'poi'`的`visibility: 'off'`来隐藏兴趣点标签
- **隐藏街景控制**：设置`streetViewControl: false`隐藏右下角的小人图标
- **简化界面**：隐藏不必要的地图控件，保持界面简洁
- **保留核心功能**：保留缩放控制和全屏功能，确保用户仍可操作地图
- **英文地理编码**：在地理编码请求中设置`language: 'en'`和`region: 'AU'`

## 注意事项

1. **API密钥**：确保Google Maps API密钥有效且有足够的配额
2. **网络连接**：需要网络连接来加载Google Maps
3. **浏览器兼容性**：支持现代浏览器
4. **性能优化**：地图只在展开时初始化，避免不必要的API调用
5. **API限制**：注意Google Maps API的使用配额和计费

## 错误处理

组件包含以下错误处理机制：
- API密钥无效时显示控制台错误
- 地址解析失败时跳过该地点
- 路线计算失败时显示控制台错误
- 网络错误时显示加载状态

## 开发调试

在开发环境中，可以通过浏览器控制台查看详细的错误信息和调试信息。