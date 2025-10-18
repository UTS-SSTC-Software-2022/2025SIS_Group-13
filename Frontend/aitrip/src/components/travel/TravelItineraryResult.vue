<template>
  <div class="travel-theme">
    <!-- 背景（与注册页一致） -->
    <div class="auth-bg"></div>

    <!-- 玻璃卡片外壳（与注册页一致） -->
    <div class="auth-card">
      <!-- 顶部返回（保持原样逻辑，可按需修改） -->
      <el-page-header
        class="page-header"
        @back="$router.push('/home')"
        title="< Back"
        content="Create Your Personalized Travel Itinerary"
      />

      <!-- ✅ 保留原文案与原格式 -->
      <h1 class="title">Create Your Personalized Travel Itinerary</h1>
      <p class="subtitle">
        Tell us your preferences and we'll craft the perfect Australian adventure for you
      </p>

      <!-- 内层主卡片（深色毛玻璃，与注册页一致） -->
      <el-card class="main-card" shadow="hover">
        <!-- 可滚动表单区域：不改内部结构 -->
        <div class="scroll-area">
          <!-- ✅ 在此处粘贴你当前的 el-form 内容（完全原样，不要动里面的字段/校验/数据） -->
          <!-- ───────────────────────────────────────────────────────────── -->
          <!-- 例如：                                                        -->
          <!-- <el-form ref="formRef" :model="form" :rules="rules"           -->
          <!--          label-position="top">                                -->
          <!--   ... 你原来的所有 el-form-item、按钮、等内容 ...               -->
          <!-- </el-form>                                                   -->
          <!-- ───────────────────────────────────────────────────────────── -->

          <!-- 下面仅提供一个“示例按钮”，便于展示样式与跳转。若你已有主按钮，请删除这一段。 -->
          <div class="demo-btn-wrap">
            <el-button
              type="primary"
              size="large"
              class="btn-primary"
              @click="goResult"
            >
              Generate Travel Itinerary
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

/**
 * 如果你自己的主按钮里已经有生成逻辑，直接用你自己的方法。
 * 这里只提供一个跳转到结果页的便捷函数。
 */
function goResult () {
  router.push('/travel/itinerary-result') // 如果路由不同，改这里
}
</script>

<!-- ❶ 背景样式需要不加 scoped 才能盖住白底 -->
<style>
.travel-theme {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
}

/* 背景与注册页一致（双径向 + 深色线性渐变） */
.travel-theme .auth-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(1200px 600px at 20% 20%, rgba(82, 0, 255, .20), transparent 60%),
    radial-gradient(1200px 600px at 80% 80%, rgba(0, 212, 255, .18), transparent 60%),
    linear-gradient(160deg, #243b55, #141e30);
  z-index: 0;
}

/* 如果外层布局容器有白底，这里强制透明（可保留） */
.travel-theme,
.travel-theme *:where(.page-container, .layout, .content) {
  background: transparent !important;
}
</style>

<!-- ❷ 组件内部样式（scoped） -->
<style scoped>
/* 主题变量（与注册页一致） */
:root {
  --card-bg: rgba(15, 23, 42, 0.92);
  --card-border: rgba(148, 163, 184, 0.15);
  --text: #e5e7eb;
  --muted: #94a3b8;
  --primary: #3b82f6;
  --primary-2: #6ea8ff;
}

/* 外层大卡片（与注册页一致） */
.auth-card {
  position: relative;
  z-index: 1;
  width: min(1100px, calc(100% - 48px));
  margin: 48px auto;
  padding: 28px 28px 36px;
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--card-border);
  border-radius: 16px;
  color: var(--text);
}

/* 标题/副标题（保留原格式） */
.title {
  font-size: 36px;
  font-weight: 800;
  margin: 8px 0 6px;
  color: #fff;
}
.subtitle {
  margin: 0 0 18px;
  color: var(--muted);
}

/* 内层主卡片（与注册页一致） */
.main-card {
  background: rgba(2, 6, 23, 0.6);
  border-color: rgba(148, 163, 184, 0.12);
}
:deep(.el-card__header) {
  background: transparent;
  border-color: rgba(148, 163, 184, 0.12);
}
:deep(.el-divider--horizontal) {
  border-top-color: rgba(148, 163, 184, 0.12);
}

/* 保留内部滚动（仅限制表单区域，避免整页滚动） */
.scroll-area {
  max-height: calc(100vh - 260px); /* 视情况微调，保证有滚动条 */
  overflow: auto;
  padding-right: 6px;
}

/* 主按钮渐变（与注册页一致） */
.btn-primary,
:deep(.el-button--primary) {
  border: none;
  color: #fff;
  background: linear-gradient(90deg, var(--primary), var(--primary-2));
  box-shadow: 0 8px 24px rgba(59, 130, 246, .35);
}
.btn-primary:hover,
:deep(.el-button--primary:hover) {
  filter: brightness(1.05);
}

/* 仅用于演示按钮位置，若你已有按钮可删 */
.demo-btn-wrap { margin-top: 12px; }
</style>
