import { defineStore } from 'pinia'
import api from '../api/client'

export const useAiStore = defineStore('ai', {
  state: () => ({
    settings: {
      provider: 'gemini',
      model_name: 'gemini-2.5-flash',
      api_key: ''
    },
    brandProfile: {
      brand_name: '',
      tone: '',
      target_audience: '',
      keywords: []
    },
    isLoading: false,
    error: null,
    errorTimeout: null
  }),

  actions: {
    setError(msg) {
      this.error = msg
      if (this.errorTimeout) clearTimeout(this.errorTimeout)
      if (msg) {
        this.errorTimeout = setTimeout(() => {
          this.error = null
        }, 4000)
      }
    },
    clearError() {
      this.error = null
      if (this.errorTimeout) clearTimeout(this.errorTimeout)
    },
    async fetchSettings() {
      try {
        const response = await api.get('/api/ai/settings')
        this.settings = response.data
      } catch (error) {
        console.error('AI ayarları alınamadı:', error)
      }
    },

    async saveSettings(settings) {
      try {
        const response = await api.post('/api/ai/settings', settings)
        this.settings = response.data
        return true
      } catch (error) {
        console.error('AI ayarları kaydedilemedi:', error)
        this.setError(error.response?.data?.detail || 'Ayarlar kaydedilirken hata oluştu.')
        return false
      }
    },

    async fetchBrandProfile() {
      try {
        const response = await api.get('/api/ai/brand')
        this.brandProfile = response.data
      } catch (error) {
        console.error('Marka profili alınamadı:', error)
      }
    },

    async saveBrandProfile(profile) {
      try {
        const response = await api.post('/api/ai/brand', profile)
        this.brandProfile = response.data
        return true
      } catch (error) {
        console.error('Marka profili kaydedilemedi:', error)
        this.setError(error.response?.data?.detail || 'Marka profili kaydedilirken hata oluştu.')
        return false
      }
    },

    async generateContent(topic, generateImage = true) {
      this.isLoading = true
      this.clearError()
      try {
        const response = await api.post('/api/ai/generate', {
          topic,
          generate_image: generateImage
        })
        return response.data
      } catch (error) {
        console.error('İçerik üretilemedi:', error)
        this.setError(error.response?.data?.detail || 'İçerik üretilirken hata oluştu.')
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async analyzeBrandFile(file) {
      this.isLoading = true
      this.clearError()
      try {
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await api.post('/api/ai/analyze-brand-file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } catch (error) {
        console.error('Dosya analiz edilemedi:', error)
        this.setError(error.response?.data?.detail || 'Dosya analiz edilirken hata oluştu.')
        throw error
      } finally {
        this.isLoading = false
      }
    }
  }
})
