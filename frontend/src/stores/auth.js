import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(localStorage.getItem('username') || null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(usernameInput, password) {
    const response = await api.post('/api/auth/login', {
      username: usernameInput,
      password: password
    })

    token.value = response.data.access_token
    username.value = usernameInput

    localStorage.setItem('token', token.value)
    localStorage.setItem('username', usernameInput)

    // Axios instance'a token'ı ekle
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`

    return response.data
  }

  function logout() {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    delete api.defaults.headers.common['Authorization']
  }

  // Sayfa yenilemede token'ı geri yükle
  function restoreToken() {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  return {
    token,
    username,
    isAuthenticated,
    login,
    logout,
    restoreToken
  }
})
