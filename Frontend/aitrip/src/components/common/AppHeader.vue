<template>
  <header class="app-header">
    <div class="header-left">
      <div class="logo-link" @click="go('/home')">
        <img src="@/assets/images/LeisurA logo.svg" alt="LeisurA Logo" class="logo" />
      </div>
    </div>
    <div class="header-right">
      <el-dropdown>
        <span class="user-info">
          <el-icon><User /></el-icon>
          {{ userName }}
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="go('/profile')">Profile</el-dropdown-item>
            <el-dropdown-item divided @click="logout">Logout</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, ArrowDown } from '@element-plus/icons-vue'
import { logoutAPI } from '@/apis/auth'

const router = useRouter()
const userName = localStorage.getItem('userName') || 'Guest'

const go = (path) => router.push(path)

const logout = async () => {
  try {
    await logoutAPI()
    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    ElMessage.success('Logged out successfully')
    router.push('/login')
  } catch (e) {
    ElMessage.error('Logout failed')
  }
}
</script>

<style scoped>
.app-header {
  background-color: #1f1f1f;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  flex-shrink: 0;
}

.logo-link {
  display: inline-block;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.logo-link:hover {
  transform: scale(1.05);
}

.logo {
  width: 10rem;
  height: 5rem;
  filter: drop-shadow(0 0 10px rgba(4, 108, 184, 0.3));
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
  color: #fff;
}

.user-info:hover {
  background-color: #333;
}

.user-info .el-icon {
  margin-right: 8px;
}

.user-info .el-icon--right {
  margin-left: 8px;
  margin-right: 0;
}
</style>
