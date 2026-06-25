<template>
  <div class="max-w-4xl mx-auto p-4 md:p-8 animate-fade-in">
    <div class="mb-8">
      <h1 class="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2 tracking-tight">Genel Ayarlar</h1>
      <p class="text-slate-500 dark:text-slate-400">Uygulamanın genel çalışma kurallarını ve varsayılan ayarlarını yapılandırın.</p>
    </div>

    <div v-if="loading" class="flex flex-col items-center justify-center p-12">
      <Loader2 class="w-8 h-8 animate-spin text-brand" />
      <p class="text-slate-500 dark:text-slate-400 mt-4">Ayarlar yükleniyor...</p>
    </div>
    
    <div v-else class="space-y-6">
      <!-- Sistem Ayarları -->
      <div class="card p-6">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-6">Sistem Ayarları</h2>
        
        <div class="flex items-center justify-between py-4 border-t border-slate-100 dark:border-slate-800">
          <div>
            <h3 class="font-medium text-slate-900 dark:text-white">Yeni Kullanıcı Kaydı</h3>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Dışarıdan yeni üye kayıtlarını açıp kapatın. Kapalı olduğunda kayıt sayfası gizlenir.</p>
          </div>
          
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="settings.registration_enabled" @change="saveSettings" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer dark:bg-slate-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-brand"></div>
          </label>
        </div>
      </div>

      <!-- Genel Yapay Zeka Ayarları -->
      <div class="card p-6">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Genel Yapay Zeka (AI) Fallback Ayarları</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">
          Kullanıcı kendi yapay zeka anahtarını girmediğinde sistemin genel olarak kullanacağı yedek (fallback) API ayarlarıdır.
        </p>

        <form @submit.prevent="saveSettings" class="space-y-5">
          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Yapay Zeka Sağlayıcısı</label>
            <select v-model="settings.global_ai_provider" class="input">
              <option value="gemini">Google Gemini</option>
              <option value="openai">OpenAI (ChatGPT)</option>
              <option value="anthropic">Anthropic (Claude)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Model Adı</label>
            <input 
              type="text" 
              v-model="settings.global_ai_model" 
              class="input"
              placeholder="Örn: gemini-2.5-flash veya gpt-4o"
            >
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">API Anahtarı</label>
            <input 
              type="password" 
              v-model="settings.global_ai_api_key" 
              class="input"
              placeholder="Yalnızca değiştirmek isterseniz girin"
            >
            <p v-if="settings.global_ai_api_key" class="text-xs text-emerald-600 dark:text-emerald-400 mt-1 flex items-center gap-1">
              <CheckCircle2 class="w-3 h-3" /> Mevcut bir anahtar kayıtlı.
            </p>
          </div>

          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center gap-4">
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
              <span v-else>Değişiklikleri Kaydet</span>
            </button>
            <transition 
              enter-active-class="transition duration-300 ease-out"
              enter-from-class="transform -translate-x-2 opacity-0"
              enter-to-class="transform translate-x-0 opacity-100"
              leave-active-class="transition duration-200 ease-in"
              leave-from-class="transform translate-x-0 opacity-100"
              leave-to-class="transform -translate-x-2 opacity-0"
            >
              <span v-if="successMessage" class="text-sm font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                <CheckCircle2 class="w-4 h-4" />
                {{ successMessage }}
              </span>
            </transition>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'
import { toast } from '../utils/toast'
import { Loader2, CheckCircle2 } from 'lucide-vue-next'

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
