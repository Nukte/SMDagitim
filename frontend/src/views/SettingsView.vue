<template>
  <div class="page-container">

    <div class="page-header">
      <h1 class="page-title">Ayarlar</h1>
      <p class="page-subtitle">AI sağlayıcı ayarları ve marka kimliğini yapılandır.</p>
    </div>

    <!-- AI Settings Section -->
    <section class="card settings-card animate-fade-in-up">
      <div class="card-header">
        <h2 class="card-title">Yapay Zeka Ayarları</h2>
      </div>
      <div class="card-body">
        <p class="settings-desc">İçerik üretiminde kullanılacak AI modelini yapılandırın.</p>

        <div class="form-grid">
          <div class="input-group">
            <label class="input-label">AI Sağlayıcı</label>
            <select v-model="settings.provider" class="input">
              <option value="gemini">Google Gemini</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-label">Model Adı</label>
            <input type="text" v-model="settings.model_name" placeholder="Örn: gemini-2.5-flash veya gpt-4o" class="input" />
          </div>

          <div class="input-group full-width">
            <label class="input-label">API Key</label>
            <input type="password" v-model="settings.api_key" placeholder="AI sağlayıcısının API anahtarı" class="input" />
          </div>
        </div>

        <button class="btn btn-primary" @click="saveSettings" :disabled="aiStore.isLoading">
          {{ aiStore.isLoading ? 'Kaydediliyor...' : 'Kaydet' }}
        </button>
      </div>
    </section>

    <!-- Brand Profile Section -->
    <section class="card settings-card animate-fade-in-up delay-100">
      <div class="card-header">
        <h2 class="card-title">Marka Kimliği</h2>
      </div>
      <div class="card-body">
        <p class="settings-desc">Yapay zeka içerik üretirken bu marka kimliğini dikkate alacaktır.</p>

        <!-- File Upload -->
        <div class="file-upload-area" @click="triggerBrandFileInput">
          <input type="file" ref="brandFileInput" @change="handleFileUpload" accept=".pdf,.docx,.txt" class="file-input-hidden" />
          <div class="file-upload-content">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            <span v-if="isAnalyzing">Analiz ediliyor...</span>
            <span v-else>Marka kimliği dosyası yükle (PDF, DOCX, TXT)</span>
          </div>
          <p class="input-hint">Yapay zeka aşağıdaki alanları otomatik dolduracaktır.</p>
        </div>

        <div class="form-grid">
          <div class="input-group">
            <label class="input-label">Marka Adı</label>
            <input type="text" v-model="brand.brand_name" placeholder="Markanızın adı" class="input" />
          </div>

          <div class="input-group">
            <label class="input-label">Marka Tonu</label>
            <select v-model="brand.tone" class="input">
              <option value="Profesyonel">Profesyonel</option>
              <option value="Samimi">Samimi</option>
              <option value="Eğlenceli">Eğlenceli</option>
              <option value="Ciddi">Ciddi</option>
              <option value="Mizahi">Mizahi</option>
            </select>
          </div>

          <div class="input-group full-width">
            <label class="input-label">Hedef Kitle</label>
            <textarea v-model="brand.target_audience" rows="2" placeholder="Örn: Genç profesyoneller, yazılımcılar, B2B şirketleri..." class="input"></textarea>
          </div>

          <div class="input-group full-width">
            <label class="input-label">Anahtar Kelimeler</label>
            <input type="text" v-model="keywordsString" placeholder="teknoloji, yazılım, inovasyon (virgülle ayırın)" class="input" />
          </div>
        </div>

        <button class="btn btn-primary" @click="saveBrand" :disabled="aiStore.isLoading">
          {{ aiStore.isLoading ? 'Kaydediliyor...' : 'Marka Profilini Kaydet' }}
        </button>
      </div>
    </section>

    <!-- Publish Settings Section -->
    <section class="card settings-card animate-fade-in-up delay-200">
      <div class="card-header">
        <h2 class="card-title">Paylaşım ve Boyut Ayarları</h2>
      </div>
      <div class="card-body">
        <p class="settings-desc">Her platform için varsayılan görsel boyutlandırma (en-boy) oranlarını belirleyin. Görselleriniz yayınlanırken otomatik olarak bulanık arka plan (blur padding) ile bu oranlara uyarlanacaktır.</p>

        <div class="form-grid">
          <div class="input-group">
            <label class="input-label">Instagram En-Boy Oranı</label>
            <select v-model="publishSettings.instagram_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5) - Önerilen</option>
              <option value="1.91:1">Yatay (1.91:1)</option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-label">Facebook En-Boy Oranı</label>
            <select v-model="publishSettings.facebook_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5)</option>
              <option value="1.91:1">Yatay (1.91:1) - Önerilen</option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-label">LinkedIn En-Boy Oranı</label>
            <select v-model="publishSettings.linkedin_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5)</option>
              <option value="1.91:1">Yatay (1.91:1) - Önerilen</option>
            </select>
          </div>

          <div class="input-group">
            <label class="input-label">X (Twitter) En-Boy Oranı</label>
            <select v-model="publishSettings.twitter_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="16:9">Geniş Ekran (16:9) - Önerilen</option>
              <option value="1.91:1">Yatay (1.91:1)</option>
            </select>
          </div>
        </div>

        <button class="btn btn-primary" @click="savePublishSettings" :disabled="publishStore.isLoading">
          {{ publishStore.isLoading ? 'Kaydediliyor...' : 'Paylaşım Ayarlarını Kaydet' }}
        </button>
      </div>
    </section>

    <!-- Notifications -->
    <div v-if="successMessage" class="notification notification-success animate-fade-in-up">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      {{ successMessage }}
    </div>
    <div v-if="aiStore.error" class="notification notification-error animate-fade-in-up">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      {{ aiStore.error }}
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAiStore } from '../stores/ai'
import { usePublishSettingsStore } from '../stores/publishSettings'

const aiStore = useAiStore()
const publishStore = usePublishSettingsStore()

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

const publishSettings = ref({
  instagram_aspect_ratio: '4:5',
  facebook_aspect_ratio: '1.91:1',
  linkedin_aspect_ratio: '1.91:1',
  twitter_aspect_ratio: '16:9'
})

const successMessage = ref('')
const brandFileInput = ref(null)
const isAnalyzing = ref(false)

const keywordsString = computed({
  get: () => brand.value.keywords.join(', '),
  set: (val) => {
    brand.value.keywords = val.split(',').map(k => k.trim()).filter(k => k)
  }
})

onMounted(async () => {
  await Promise.all([
    aiStore.fetchSettings(),
    aiStore.fetchBrandProfile(),
    publishStore.fetchSettings()
  ])

  if (aiStore.settings) {
    settings.value = { ...aiStore.settings, api_key: aiStore.settings.api_key || '' }
  }
  if (aiStore.brandProfile) {
    brand.value = { ...aiStore.brandProfile }
  }
  if (publishStore.settings) {
    publishSettings.value = { ...publishStore.settings }
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

const savePublishSettings = async () => {
  successMessage.value = ''
  const success = await publishStore.saveSettings(publishSettings.value)
  if (success) {
    successMessage.value = 'Paylaşım ve boyut ayarları başarıyla kaydedildi.'
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
    event.target.value = ''
  }
}
</script>

<style scoped>
.settings-card {
  margin-bottom: var(--space-6);
}

.settings-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.full-width {
  grid-column: 1 / -1;
}

/* File Upload */
.file-upload-area {
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: var(--space-6);
}

.file-upload-area:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.file-upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.file-upload-content svg {
  color: var(--text-tertiary);
}

.file-input-hidden {
  display: none;
}

/* Notifications */
.notification {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  margin-top: var(--space-4);
}

.notification-success {
  background: var(--success-bg);
  border: 1px solid var(--success-border);
  color: var(--success);
}

.notification-error {
  background: var(--error-bg);
  border: 1px solid var(--error-border);
  color: var(--error);
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
