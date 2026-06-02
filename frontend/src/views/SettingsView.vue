<template>
  <div class="settings-view">
    <header class="header">
      <div class="header-left">
        <router-link to="/" class="back-link">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          Geri Dön
        </router-link>
        <h1>Ayarlar</h1>
      </div>
    </header>

    <div class="settings-content">
      <!-- AI Settings Section -->
      <section class="settings-section">
        <div class="section-header">
          <h2>Yapay Zeka Ayarları</h2>
          <p>İçerik üretiminde kullanılacak AI modelini yapılandırın.</p>
        </div>
        
        <div class="form-group">
          <label>AI Sağlayıcı</label>
          <select v-model="settings.provider">
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
          </select>
        </div>

        <div class="form-group">
          <label>Model Adı</label>
          <input type="text" v-model="settings.model_name" placeholder="Örn: gemini-2.5-flash veya gpt-4o" />
        </div>

        <div class="form-group">
          <label>API Key</label>
          <input type="password" v-model="settings.api_key" placeholder="AI sağlayıcısının API anahtarı" />
        </div>
        
        <button class="btn btn-primary" @click="saveSettings" :disabled="aiStore.isLoading">
          {{ aiStore.isLoading ? 'Kaydediliyor...' : 'AI Ayarlarını Kaydet' }}
        </button>
      </section>

      <!-- Brand Profile Section -->
      <section class="settings-section mt-4">
        <div class="section-header">
          <h2>Marka Kimliği</h2>
          <p>Yapay zeka içerik üretirken bu marka kimliğini dikkate alacaktır.</p>
        </div>

        <div class="form-group analyze-group">
          <label>Marka Kimliği Dosyası Yükle (Otomatik Analiz)</label>
          <div class="upload-controls">
            <input type="file" ref="brandFileInput" @change="handleFileUpload" accept=".pdf,.docx,.txt" class="file-input" />
            <button class="btn btn-secondary btn-sm" @click="triggerBrandFileInput" :disabled="isAnalyzing">
              <span v-if="isAnalyzing">Analiz Ediliyor...</span>
              <span v-else>📁 Dosya Seç ve Analiz Et</span>
            </button>
          </div>
          <p class="help-text">PDF, DOCX veya TXT belgenizi yükleyin. Yapay zeka aşağıdaki alanları otomatik dolduracaktır.</p>
        </div>

        <div class="form-group">
          <label>Marka Adı</label>
          <input type="text" v-model="brand.brand_name" placeholder="Markanızın adı" />
        </div>

        <div class="form-group">
          <label>Marka Tonu</label>
          <select v-model="brand.tone">
            <option value="Profesyonel">Profesyonel</option>
            <option value="Samimi">Samimi</option>
            <option value="Eğlenceli">Eğlenceli</option>
            <option value="Ciddi">Ciddi</option>
            <option value="Mizahi">Mizahi</option>
          </select>
        </div>

        <div class="form-group">
          <label>Hedef Kitle</label>
          <textarea v-model="brand.target_audience" rows="2" placeholder="Örn: Genç profesyoneller, yazılımcılar, B2B şirketleri..."></textarea>
        </div>

        <div class="form-group">
          <label>Anahtar Kelimeler (Virgülle ayırın)</label>
          <input type="text" v-model="keywordsString" placeholder="teknoloji, yazılım, inovasyon" />
        </div>

        <button class="btn btn-primary" @click="saveBrand" :disabled="aiStore.isLoading">
          {{ aiStore.isLoading ? 'Kaydediliyor...' : 'Marka Profilini Kaydet' }}
        </button>
      </section>
      
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="aiStore.error" class="error-message">{{ aiStore.error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAiStore } from '../stores/ai'

const aiStore = useAiStore()

const settings = ref({
  provider: 'gemini',
  model_name: 'gemini-2.5-flash',
  api_key: ''
})

const brand = ref({
  brand_name: '',
  tone: 'Profesyonel',
  target_audience: '',
  keywords: []
})

const successMessage = ref('')
const brandFileInput = ref(null)
const isAnalyzing = ref(false)

// Virgülle ayrılmış string'i listeye çevirmek için
const keywordsString = computed({
  get: () => brand.value.keywords.join(', '),
  set: (val) => {
    brand.value.keywords = val.split(',').map(k => k.trim()).filter(k => k)
  }
})

onMounted(async () => {
  await aiStore.fetchSettings()
  await aiStore.fetchBrandProfile()
  
  if (aiStore.settings) {
    settings.value = { ...aiStore.settings, api_key: aiStore.settings.api_key || '' }
  }
  if (aiStore.brandProfile) {
    brand.value = { ...aiStore.brandProfile }
  }
})

const saveSettings = async () => {
  successMessage.value = ''
  const success = await aiStore.saveSettings(settings.value)
  if (success) {
    successMessage.value = 'AI ayarları başarıyla kaydedildi.'
    setTimeout(() => { successMessage.value = '' }, 3000)
  }
}

const saveBrand = async () => {
  successMessage.value = ''
  const success = await aiStore.saveBrandProfile(brand.value)
  if (success) {
    successMessage.value = 'Marka profili başarıyla kaydedildi.'
    setTimeout(() => { successMessage.value = '' }, 3000)
  }
}

const triggerBrandFileInput = () => {
  brandFileInput.value?.click()
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  isAnalyzing.value = true
  aiStore.error = null
  successMessage.value = ''
  
  try {
    const result = await aiStore.analyzeBrandFile(file)
    if (result) {
      brand.value.brand_name = result.brand_name || brand.value.brand_name
      brand.value.tone = result.tone || brand.value.tone
      brand.value.target_audience = result.target_audience || brand.value.target_audience
      if (result.keywords && result.keywords.length > 0) {
        brand.value.keywords = result.keywords
      }
      successMessage.value = 'Dosya başarıyla analiz edildi. Lütfen bilgileri kontrol edip kaydedin.'
      setTimeout(() => { successMessage.value = '' }, 5000)
    }
  } catch (error) {
    // Error is handled in store
  } finally {
    isAnalyzing.value = false
    event.target.value = '' // reset input
  }
}
</script>

<style scoped>
.settings-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--accent-primary);
}

.settings-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.mt-4 {
  margin-top: 2rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.2rem;
  margin-bottom: 0.25rem;
}

.section-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-secondary);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid var(--accent-success);
  color: var(--accent-success);
  border-radius: 8px;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--accent-danger);
  color: var(--accent-danger);
  border-radius: 8px;
}

.analyze-group {
  padding: 1rem;
  background: rgba(99, 102, 241, 0.05);
  border: 1px dashed var(--accent-primary);
  border-radius: 8px;
  margin-bottom: 2rem;
}

.upload-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.file-input {
  display: none;
}

.btn-secondary {
  background: var(--bg-input);
  border: 1px solid var(--border);
  color: var(--text-primary);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--accent-primary);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.help-text {
  font-size: 0.8rem;
  color: var(--text-tertiary);
  margin-top: 0.5rem;
}
</style>
