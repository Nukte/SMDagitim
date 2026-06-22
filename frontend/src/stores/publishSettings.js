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
    error: null
  }),

  actions: {
    async fetchSettings() {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.get('/api/publish/settings')
        this.settings = response.data
      } catch (error) {
        console.error('Publish settings alınamadı:', error)
        this.error = 'Ayarlar alınamadı.'
      } finally {
        this.isLoading = false
      }
    },

    async saveSettings(settings) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.post('/api/publish/settings', settings)
        this.settings = response.data
        return true
      } catch (error) {
        console.error('Publish settings kaydedilemedi:', error)
        this.error = error.response?.data?.detail || 'Ayarlar kaydedilirken hata oluştu.'
        return false
      } finally {
        this.isLoading = false
      }
    }
  }
})
