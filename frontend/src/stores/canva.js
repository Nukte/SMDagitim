import { defineStore } from 'pinia'
import api from '../api/client'

export const useCanvaStore = defineStore('canva', {
  state: () => ({
    isConnected: false,
    accountName: null,
    isLoading: false,
    error: null,
  }),

  actions: {
    async checkStatus() {
      try {
        const res = await api.get('/api/canva/status')
        this.isConnected = res.data.connected
        this.accountName = res.data.account_name
      } catch (err) {
        console.error('Canva bağlantı durumu alınamadı:', err)
        this.isConnected = false
      }
    },

    async connectCanva() {
      try {
        const res = await api.get('/api/canva/auth/login')
        window.location.href = res.data.url
      } catch (err) {
        this.error = 'Bağlantı başlatılamadı'
        console.error(err)
      }
    },

    async translateDesign(designUrl, targetLanguage) {
      this.isLoading = true
      this.error = null
      try {
        const res = await api.post('/api/canva/translate', {
          design_url: designUrl,
          target_language: targetLanguage
        })
        return res.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Çeviri sırasında bir hata oluştu'
        throw err
      } finally {
        this.isLoading = false
      }
    }
  }
})
