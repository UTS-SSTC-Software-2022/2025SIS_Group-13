# Google Maps 配置说明

## 设置 Google Maps API Key

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用以下API：
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. 创建API密钥
5. 在 `Frontend/aitrip/src/components/travel/GoogleMap.vue` 文件中替换 `YOUR_GOOGLE_MAPS_API_KEY` 为你的实际API密钥

## 功能特性

- 响应式地图显示
- 亚洲地区默认视图
- 热门目的地标记
- 地图控制按钮（图层切换、定位、缩放）
- 移动端优化

## 注意事项

- 确保API密钥有适当的限制设置
- 在生产环境中使用环境变量存储API密钥
- 定期检查API使用配额
