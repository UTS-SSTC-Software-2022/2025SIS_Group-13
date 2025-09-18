import request from './request'

/**
 * User login API
 * @param {Object} loginData - Login credentials
 * @param {string} loginData.email - User email
 * @param {string} loginData.password - User password
 * @returns {Promise} Login response
 */
export const loginAPI = (loginData) => {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: {
      email: loginData.email,
      password: loginData.password,
    }
  })
}

/**
 * User registration API
 * @param {Object} registerData - Registration data
 * @param {string} registerData.email - User email
 * @param {string} registerData.password - User password
 * @param {string} registerData.confirmPassword - Password confirmation
 * @param {string} registerData.firstName - User first name
 * @param {string} registerData.lastName - User last name
 * @returns {Promise} Registration response
 */
export const registerAPI = (registerData) => {
  return request({
    url: '/auth/register/',
    method: 'post',
    data: {
      email: registerData.email,
      username: registerData.username,
      firstName: registerData.firstname,
      lastName: registerData.lastname,
      password: registerData.password,
      confirmPassword: registerData.confirmPassword,
    }
  })
}

/**
 * Forgot password API
 * @param {string} email - User email
 * @returns {Promise} Forgot password response
 */
export const forgotPasswordAPI = (email) => {
  return request({
    url: '/auth/forgot-password/',
    method: 'post',
    data: { email }
  })
}

/**
 * Reset password API
 * @param {Object} resetData - Reset password data
 * @param {string} resetData.token - Reset token
 * @param {string} resetData.password - New password
 * @param {string} resetData.confirmPassword - Password confirmation
 * @returns {Promise} Reset password response
 */
export const resetPasswordAPI = (resetData) => {
  return request({
    url: '/auth/reset-password/',
    method: 'post',
    data: {
      token: resetData.token,
      password: resetData.password,
      confirmPassword: resetData.confirmPassword
    }
  })
}

/**
 * Get user profile API
 * @returns {Promise} User profile response
 */
export const getUserProfileAPI = () => {
  return request({
    url: '/auth/profile/',
    method: 'get'
  })
}

/**
 * Update user profile API
 * @param {Object} profileData - Profile update data
 * @param {string} profileData.firstName - User first name
 * @param {string} profileData.lastName - User last name
 * @param {string} profileData.phone - User phone number
 * @param {string} profileData.avatar - User avatar URL
 * @returns {Promise} Profile update response
 */
export const updateUserProfileAPI = (profileData) => {
  return request({
    url: '/auth/profile/',
    method: 'put',
    data: profileData
  })
}

/**
 * Change password API
 * @param {Object} passwordData - Password change data
 * @param {string} passwordData.currentPassword - Current password
 * @param {string} passwordData.newPassword - New password
 * @param {string} passwordData.confirmPassword - Password confirmation
 * @returns {Promise} Password change response
 */
export const changePasswordAPI = (passwordData) => {
  return request({
    url: '/auth/change-password/',
    method: 'put',
    data: {
      currentPassword: passwordData.currentPassword,
      newPassword: passwordData.newPassword,
      confirmPassword: passwordData.confirmPassword
    }
  })
}

/**
 * User logout API
 * @returns {Promise} Logout response
 */
export const logoutAPI = () => {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}

/**
 * Refresh token API
 * @returns {Promise} Refresh token response
 */
export const refreshTokenAPI = () => {
  return request({
    url: '/auth/refresh-token/',
    method: 'post'
  })
}

/**
 * Verify email API
 * @param {string} token - Verification token
 * @returns {Promise} Email verification response
 */
export const verifyEmailAPI = (token) => {
  return request({
    url: '/auth/verify-email/',
    method: 'post',
    data: { token }
  })
}

/**
 * Resend email verification API
 * @param {string} email - User email
 * @returns {Promise} Resend verification response
 */
export const resendVerificationAPI = (email) => {
  return request({
    url: '/auth/resend-verification/',
    method: 'post',
    data: { email }
  })
}
