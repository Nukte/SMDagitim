import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export const usePostStore = defineStore('post', () => {
  // Post verileri
  const content = ref('')
  const hashtags = ref([])
  const media = ref([])
  const selectedAccounts = ref([])

  // Platform bağlantı durumları
  const connectedAccounts = ref([])

  // Paylaşım durumu
  const publishJob = ref(null)
  const isPublishing = ref(false)

  // Platform bilgileri
  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: '📸', color: '#E1306C', maxChars: 2200 },
    { id: 'facebook', name: 'Facebook', icon: '📘', color: '#1877F2', maxChars: 63206 },
    { id: 'twitter', name: 'X / Twitter', icon: '𝕏', color: '#000000', maxChars: 280 },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: '#0A66C2', maxChars: 3000 }
  ]

  const currentMinChars = computed(() => {
    if (selectedAccounts.value.length === 0) return 63206
    const selectedPlatformsSet = new Set(
      connectedAccounts.value
        .filter(acc => selectedAccounts.value.includes(acc.account_id))
        .map(acc => acc.platform)
    )
    const selected = platforms.filter(p => selectedPlatformsSet.has(p.id))
    return Math.min(...selected.map(p => p.maxChars), 63206)
  })

  // Platform bağlantı durumlarını getir
  async function fetchPlatformStatus() {
    try {
      const response = await api.get('/api/oauth/status')
      connectedAccounts.value = response.data.accounts || []
    } catch (error) {
      console.error('Bağlı hesaplar alınamadı:', error)
    }
  }

  // Presigned URL al (dosya yükleme için)
  async function getPresignedUrl(filename, contentType) {
    const response = await api.post('/api/upload/presign', {
      filename,
      content_type: contentType
    })
    return response.data
  }

  // Yükleme onayı
  async function confirmUpload(objectKey, contentType) {
    const response = await api.post('/api/upload/confirm', {
      object_key: objectKey,
      content_type: contentType
    })
    return response.data
  }

  // Dosyayı MinIO'ya doğrudan yükle
  async function uploadToMinIO(file, presignedData, onProgress) {
    const formData = new FormData()

    // Presigned POST fields'ı ekle
    Object.entries(presignedData.upload_fields).forEach(([key, value]) => {
      formData.append(key, value)
    })

    // Dosyayı en son ekle
    formData.append('file', file)

    // XMLHttpRequest ile yükle (progress tracking için)
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable && onProgress) {
          onProgress(Math.round((e.loaded / e.total) * 100))
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Upload failed: ${xhr.status}`))
        }
      })

      xhr.addEventListener('error', () => reject(new Error('Upload failed')))

      xhr.open('POST', presignedData.upload_url)
      xhr.send(formData)
    })
  }

  // Frontend'den dosyayı backend'e atıp, backend üzerinden MinIO'ya yükleme yöntemi (Presigned URL hatalarını aşmak için)
  async function uploadDirect(file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/api/upload/direct', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            onProgress(Math.round((progressEvent.loaded / progressEvent.total) * 100))
          }
        }
      })
      return response.data
    } catch (error) {
      console.error('Direct upload failed:', error)
      throw error
    }
  }

  // Medya ekle
  function addMedia(mediaItem) {
    media.value.push(mediaItem)
  }

  // Medya kaldır
  function removeMedia(index) {
    media.value.splice(index, 1)
  }

  // Paylaşım yap
  async function publishPost() {
    isPublishing.value = true
    try {
      const response = await api.post('/api/publish', {
        content: content.value,
        hashtags: hashtags.value,
        media: media.value.map(m => ({
          url: m.public_url,
          object_key: m.object_key,
          type: m.media_type
        })),
        account_ids: selectedAccounts.value
      })

      publishJob.value = response.data
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Paylaşım durumunu sorgula (polling)
  async function pollPublishStatus(jobId) {
    const response = await api.get(`/api/publish/${jobId}`)
    publishJob.value = response.data
    return response.data
  }

  // Formu sıfırla
  function resetForm() {
    content.value = ''
    hashtags.value = []
    media.value = []
    selectedAccounts.value = []
    publishJob.value = null
    isPublishing.value = false
  }

  return {
    content,
    hashtags,
    media,
    selectedAccounts,
    connectedAccounts,
    publishJob,
    isPublishing,
    platforms,
    currentMinChars,
    fetchPlatformStatus,
    getPresignedUrl,
    confirmUpload,
    uploadToMinIO,
    uploadDirect,
    addMedia,
    removeMedia,
    publishPost,
    pollPublishStatus,
    resetForm
  }
})
