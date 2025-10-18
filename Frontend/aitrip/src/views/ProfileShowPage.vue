<template>
  <div class="show-shell">
    <!-- 深色渐变背景（与注册页一致） -->
    <div class="auth-bg" />

    <!-- 内容卡片 -->
    <div class="show-card">
      <!-- 顶部：返回 + 标题（深色背景下浅色文字） -->
      <el-page-header
        class="page-header"
        @back="$router.back()"
        title="< Back"
        content="User Profile"
      />

      <!-- 标题与说明 -->
      <h1 class="heading">Basic Information</h1>
      <p class="subtext">This is the profile information stored in the system.</p>

      <!-- 浅色信息表（与浅色表格风格一致） -->
      <div class="table-card">
        <el-descriptions
          class="desc-table"
          :column="1"
          border
          :label-style="{ width: '220px' }"
        >
          <el-descriptions-item label="Email">
            {{ profile.email || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="First Name">
            {{ profile.firstName || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="Last Name">
            {{ profile.lastName || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="Phone">
            {{ profile.phone || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="Avatar">
            {{ profile.avatar || '-' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

/**
 * 你项目里若已有获取用户信息的方式（例如 Pinia/接口），
 * 可直接把下方的默认赋值替换为你的数据源。
 */
const profile = reactive({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  avatar: ''
})

onMounted(() => {
  // 示例：如果之前把资料放在 localStorage，可在此恢复
  try {
    const saved = JSON.parse(localStorage.getItem('profile') || '{}')
    Object.assign(profile, saved)
  } catch (e) { /* 忽略 */ }
})
</script>

<style scoped>
.show-shell {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 内容卡片最大宽度与居中 */
.show-card {
  position: relative;
  z-index: 1;
  max-width: 1120px;
  margin: 0 auto;
  padding: 28px 28px 40px;
}

/* 顶部返回区在深色背景下的浅色文字 */
.page-header {
  margin-bottom: 12px;
}
:deep(.el-page-header__left .el-page-header__title) {
  color: #e8edf6; /* 浅色 */
  font-weight: 600;
}
:deep(.el-page-header__content) {
  color: #e8edf6; /* “User Profile” */
  font-weight: 700;
  font-size: 22px;
}

/* 标题与副标题（浅色） */
.heading {
  color: #e8edf6;
  font-size: 36px;
  font-weight: 800;
  margin: 6px 0 6px;
  letter-spacing: .2px;
}
.subtext {
  color: rgba(232, 237, 246, .85);
  margin: 0 0 18px;
  font-size: 18px;
}

/* 表格所在的浅色卡片（与浅色表格搭配） */
.table-card {
  background: #ffffff;
  border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, .22);
  padding: 0;
  overflow: hidden;
}

/* Element Plus Descriptions 的浅色表格风格（第三张图） */
.desc-table {
  --border-color: #e6ebf2;
}
:deep(.el-descriptions__body) {
  border-top: 1px solid var(--border-color);
}
:deep(.el-descriptions__table.is-bordered .el-descriptions__cell) {
  border-color: var(--border-color);
}

/* 左侧标签列：浅灰底、深灰字、加粗 */
:deep(.el-descriptions__label.is-bordered-label) {
  background: #f5f7fa;        /* 浅灰底 */
  color: #606266;             /* 深灰字 */
  font-weight: 600;
}

/* 右侧内容列：白底深灰字 */
:deep(.el-descriptions__content) {
  background: #ffffff;
  color: #606266;
}

/* 小屏优化 */
@media (max-width: 768px) {
  .show-card { padding: 18px 16px 28px; }
  .heading { font-size: 28px; }
  .subtext { font-size: 14px; }
}
</style>

<!-- 深色渐变背景（非 scoped；与注册页一致的感觉） -->
<style>
.auth-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  /* 与注册页统一的深色渐变氛围 */
  background:
    radial-gradient(1200px 800px at 85% 35%, rgba(98, 86, 240, 0.25) 0%, rgba(98, 86, 240, 0) 60%),
    radial-gradient(1000px 700px at 10% 20%, rgba(35, 116, 221, 0.25) 0%, rgba(35, 116, 221, 0) 60%),
    linear-gradient(180deg, #0f1b2d 0%, #0e1a2c 45%, #15243d 100%);
}
</style>
