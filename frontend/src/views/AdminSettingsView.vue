<template>
  <div class="admin-settings-view">
    <div class="page-header animate-fade-in-up">
      <h1 class="page-title">Genel Ayarlar</h1>
      <p class="page-subtitle">Uygulamanın genel çalışma kurallarını ve varsayılan ayarlarını yapılandırın.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner spinner-lg"></div>
      <p class="text-tertiary mt-4">Ayarlar yükleniyor...</p>
    </div>
    
    <div v-else class="settings-grid animate-fade-in-up delay-100">
      <!-- Sistem Ayarları -->
      <div class="card settings-card">
        <div class="card-header">
          <h2 class="card-title">Sistem Ayarları</h2>
        </div>
        <div class="card-body">
          <div class="toggle-row">
            <div class="toggle-info">
              <h3 class="toggle-title">Yeni Kullanıcı Kaydı</h3>
              <p class="toggle-desc">Dışarıdan yeni üye kayıtlarını açıp kapatın. Kapalı olduğunda kayıt sayfası gizlenir.</p>
            </div>
            <label class="premium-toggle">
              <input type="checkbox" v-model="settings.registration_enabled" @change="saveSettings">
              <div class="toggle-track">
                <div class="toggle-thumb"></div>
              </div>
            </label>
          </div>
        </div>
      </div>

      <!-- Genel Yapay Zeka Ayarları -->
      <div class="card settings-card delay-200">
        <div class="card-header">
          <h2 class="card-title">Genel Yapay Zeka (AI) Fallback Ayarları</h2>
        </div>
        <div class="card-body">
          <p class="section-desc">
            Kullanıcı kendi yapay zeka anahtarını girmediğinde sistemin genel olarak kullanacağı yedek (fallback) API ayarlarıdır.
          </p>

          <form @submit.prevent="saveSettings" class="settings-form">
            <div class="input-group">
              <label class="input-label">Yapay Zeka Sağlayıcısı</label>
              <div class="input-wrapper">
                <select v-model="settings.global_ai_provider" class="input">
                  <option value="gemini">Google Gemini</option>
                  <option value="openai">OpenAI (ChatGPT)</option>
                  <option value="anthropic">Anthropic (Claude)</option>
                </select>
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">Model Adı</label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  v-model="settings.global_ai_model" 
                  class="input"
                  placeholder="Örn: gemini-2.5-flash veya gpt-4o"
                >
              </div>
            </div>

            <div class="input-group">
              <label class="input-label">API Anahtarı</label>
              <div class="input-wrapper">
                <input 
                  type="password" 
                  v-model="settings.global_ai_api_key" 
                  class="input"
                  placeholder="Yalnızca değiştirmek isterseniz girin"
                >
              </div>
              <span class="input-hint text-success mt-1" v-if="settings.global_ai_api_key">
                ✓ Mevcut bir anahtar kayıtlı.
              </span>
            </div>

            <div class="form-actions mt-6">
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <span v-if="saving" class="spinner spinner-sm"></span>
                <span v-else>Değişiklikleri Kaydet</span>
              </button>
              <transition name="fade">
                <span v-if="successMessage" class="success-message">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  {{ successMessage }}
                </span>
              </transition>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'
import { toast } from '../utils/toast'

const settings = ref({
  registration_enabled: true,
  global_ai_provider: 'gemini',
  global_ai_model: 'gemini-2.5-flash',
  global_ai_api_key: ''
})

const loading = ref(true)
const saving = ref(false)
const successMessage = ref('')

async function fetchSettings() {
  try {
    const response = await api.get('/api/admin/settings')
    settings.value = {
      ...response.data,
      global_ai_api_key: response.data.global_ai_api_key || ''
    }
  } catch (err) {
    console.error('Ayarlar alınamadı:', err)
  } finally {
    loading.value = false
  }
}

async function saveSettings() {
  saving.value = true
  successMessage.value = ''
  try {
    const payload = { ...settings.value }
    if (!payload.global_ai_api_key) {
        delete payload.global_ai_api_key
    }
    
    await api.put('/api/admin/settings', payload)
    successMessage.value = 'Ayarlar başarıyla kaydedildi'
    setTimeout(() => { successMessage.value = '' }, 3000)
    toast.success('Genel ayarlar kaydedildi.')
  } catch (err) {
    toast.error('Ayarlar kaydedilirken hata oluştu.')
    console.error(err)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchSettings()
})
</script>

<style scoped>
.admin-settings-view {
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: var(--space-12);
}

.settings-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.settings-card {
  overflow: hidden;
}

.section-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
  line-height: 1.6;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.mt-1 { margin-top: var(--space-1); }
.mt-4 { margin-top: var(--space-4); }
.mt-6 { margin-top: var(--space-6); }

/* Premium Toggle */
.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2) 0;
}

.toggle-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.toggle-desc {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}

.premium-toggle {
  position: relative;
  display: inline-block;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.premium-toggle input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-track {
  width: 44px;
  height: 24px;
  background-color: var(--border);
  border-radius: 999px;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.15);
}

.premium-toggle input:checked + .toggle-track {
  background-color: var(--accent);
}

.premium-toggle input:checked + .toggle-track .toggle-thumb {
  transform: translateX(20px);
}

.premium-toggle:active .toggle-thumb {
  width: 24px;
}
.premium-toggle input:checked:active + .toggle-track .toggle-thumb {
  transform: translateX(16px);
}

.form-actions {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.success-message {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--success);
  font-size: var(--font-size-sm);
  font-weight: 500;
  background: var(--success-bg);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}
</style>
