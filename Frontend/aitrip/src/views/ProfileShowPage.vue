<template>
  <div class="profile-show">
    <!-- Page header -->
    <el-page-header
      class="page-header"
      @back="goBack"
      title="< Back"
      content="User Profile"
    />

    <!-- Card: Basic Information -->
    <div class="container">
      <el-card class="main-card" shadow="hover">
        <h1 class="title">Basic Information</h1>
        <p class="subtitle">This is the profile information stored in the system.</p>

        <el-descriptions
          class="desc"
          :column="1"
          border
          :label-style="{ width: '160px' }"
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
            <div class="avatar-row">
              <el-avatar
                v-if="profile.avatar"
                :src="profile.avatar"
                size="large"
              />
              <span v-else>-</span>
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const profile = reactive({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  avatar: ''
})

function goBack() {
  // 有浏览历史就返回，否则去首页
  if (window.history.length > 1) router.back()
  else router.push('/home')
}

// 尝试从常见的 localStorage key 里读取用户信息
function readAny(keys) {
  for (const k of keys) {
    const raw = localStorage.getItem(k)
    if (!raw) continue
    try { return JSON.parse(raw) } catch { return raw }
  }
  return null
}

onMounted(() => {
  const data =
    readAny(['user', 'userInfo', 'profile', 'auth_user', 'currentUser']) || {}

  // 做字段兼容
  profile.email = data.email || data.mail || ''
  profile.firstName =
    data.firstName || data.firstname || data.givenName || data.name?.first || ''
  profile.lastName =
    data.lastName || data.lastname || data.surname || data.name?.last || ''
  profile.phone = data.phone || data.mobile || data.telephone || ''
  profile.avatar = data.avatar || data.avatarUrl || data.photo || ''
})
</script>

<style scoped>
.profile-show {
  min-height: 100vh;
  padding: 24px;
  /* 背景渐变与当前项目常用配色接近 */
  background: linear-gradient(180deg, #7a69f5 0%, #7f86f3 40%, #8eb4f7 100%);
}

.page-header {
  max-width: 1100px;
  margin: 0 auto 8px;
}

.container {
  display: flex;
  justify-content: center;
}

.main-card {
  width: 100%;
  max-width: 1100px;
  border-radius: 16px;
  padding: 8px 4px;
}

.title {
  margin: 4px 8px;
  font-size: 20px;
  font-weight: 600;
}

.subtitle {
  margin: 0 8px;
  color: #666;
}

.desc {
  margin-top: 12px;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
