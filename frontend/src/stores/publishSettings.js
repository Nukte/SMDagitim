import { defineStore } from 'pinia'
import api from '../api/client'

export const usePublishSettingsStore = defineStore('publishSettings', {
  state: () => ({
    settings: {
      instagram_aspect_ratio: '4:5',
      facebook_aspect_ratio: '1.91:1',
      linkedin_aspect_ratio: '1.91:1',
      twitter_aspect_ratio: '16:9'
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
      this.isLoading = true
      this.clearError()
      try {
        const response = await api.get('/api/publish/settings')
        this.settings = response.data
      } catch (error) {
        console.error('Publish settings alınamadı:', error)
        this.setError('Ayarlar alınamadı.')
      } finally {
        this.isLoading = false
      }
    },

    async saveSettings(settings) {
      this.isLoading = true
      this.clearError()
      try {
        const response = await api.post('/api/publish/settings', settings)
        this.settings = response.data
        return true
      } catch (error) {
        console.error('Publish settings kaydedilemedi:', error)
        this.setError(error.response?.data?.detail || 'Ayarlar kaydedilirken hata oluştu.')
        return false
      } finally {
        this.isLoading = false
      }
    }
  }
})
