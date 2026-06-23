import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const email = ref(localStorage.getItem('email') || null)
  const isSuperuser = ref(localStorage.getItem('isSuperuser') === 'true')
  const firstName = ref(localStorage.getItem('firstName') || '')
  const lastName = ref(localStorage.getItem('lastName') || '')

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
      firstName.value = response.data.first_name || ''
      lastName.value = response.data.last_name || ''
      
      localStorage.setItem('isSuperuser', isSuperuser.value)
      localStorage.setItem('firstName', firstName.value)
      localStorage.setItem('lastName', lastName.value)
    } catch (err) {
      console.error('Failed to fetch profile', err)
      if (err.response?.status === 401) {
        logout()
      }
    }
  }

  async function register(firstNameInput, lastNameInput, emailInput, password) {
    const response = await api.post('/api/auth/register', {
      first_name: firstNameInput,
      last_name: lastNameInput,
      email: emailInput,
      password: password
    })
    return response.data
  }

  function logout() {
    token.value = null
    email.value = null
    isSuperuser.value = false
    firstName.value = ''
    lastName.value = ''
    
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('isSuperuser')
    localStorage.removeItem('firstName')
    localStorage.removeItem('lastName')
    
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
    firstName,
    lastName,
    isAuthenticated,
    login,
    register,
    logout,
    restoreToken,
    fetchProfile
  }
})
