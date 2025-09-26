<template>
  <div class="profile-page">
    <h2>User Profile</h2>

    <el-card class="profile-card">
      <el-form :model="profileForm" label-width="120px">
        <el-form-item label="Email">
          <el-input v-model="profileForm.email" disabled />
        </el-form-item>
        <el-form-item label="First Name">
          <el-input v-model="profileForm.firstName" />
        </el-form-item>
        <el-form-item label="Last Name">
          <el-input v-model="profileForm.lastName" />
        </el-form-item>
        <el-form-item label="Phone">
          <el-input v-model="profileForm.phone" />
        </el-form-item>
        <el-form-item label="Avatar">
          <el-input v-model="profileForm.avatar" placeholder="Image URL" />
        </el-form-item>
      </el-form>

      <div style="text-align: right; margin-top: 20px;">
        <el-button type="primary" @click="updateProfile">Save</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserProfileAPI, updateUserProfileAPI } from '@/apis/auth'
import { ElMessage } from 'element-plus'

const profileForm = ref({
  email: '',
  firstName: '',
  lastName: '',
  phone: '',
  avatar: ''
})

onMounted(async () => {
  try {
    const res = await getUserProfileAPI()
    profileForm.value = res.data
  } catch (e) {
    ElMessage.error('Failed to load profile')
  }
})

const updateProfile = async () => {
  try {
    await updateUserProfileAPI(profileForm.value)
    ElMessage.success('Profile updated successfully')
  } catch (e) {
    ElMessage.error('Failed to update profile')
  }
}
</script>

<style scoped>
.profile-page {
  padding: 20px;
}
.profile-card {
  max-width: 600px;
  margin: auto;
}
</style>
