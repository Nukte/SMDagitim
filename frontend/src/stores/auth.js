import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const email = ref(localStorage.getItem('email') || null)
  const isSuperuser = ref(localStorage.getItem('isSuperuser') === 'true')

  const isAuthenticated = computed(() => !!token.value)

  async function login(emailInput, password) {
    const response = await api.post('/api/auth/login', {
      email: emailInput,
      password: password
    })

    token.value = response.data.access_token
    email.value = emailInput

    localStorage.setItem('token', token.value)
    localStorage.setItem('email', emailInput)

    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

    await fetchProfile()

    return response.data
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      const response = await api.get('/api/auth/me')
      isSuperuser.value = response.data.is_superuser
      localStorage.setItem('isSuperuser', isSuperuser.value)
    } catch (err) {
      console.error('Failed to fetch profile', err)
      if (err.response?.status === 401) {
        logout()
      }
    }
  }

  async function register(emailInput, password) {
    const response = await api.post('/api/auth/register', {
      email: emailInput,
      password: password
    })
    return response.data
  }

  function logout() {
    token.value = null
    email.value = null
    isSuperuser.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('isSuperuser')
    delete api.defaults.headers.common['Authorization']
  }

  function restoreToken() {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  return {
    token,
    email,
    isSuperuser,
    isAuthenticated,
    login,
    register,
    logout,
    restoreToken,
    fetchProfile
  }
})
