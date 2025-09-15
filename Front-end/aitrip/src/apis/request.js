import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 600000
})

// Request interceptor
request.interceptors.request.use(
  (config) => {
    if (config.noToken) {
      return config
    }

    // Get token from localStorage
    const token = localStorage.getItem('token')

    // Add token to request headers if it exists
    if (token) {
      config.headers['Authorization'] = `${token}`
    }
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  (response) => {
    const res = response.data

    if (res.code === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }

    // Update localStorage if response contains new token
    if (response.headers['new-token']) {
      localStorage.setItem('token', response.headers['new-token'])
    }
    // Return the response data directly
    return res
  },
  (error) => {
    console.error('Response error:', error)
    return Promise.reject(error)
  }
)

export default request
