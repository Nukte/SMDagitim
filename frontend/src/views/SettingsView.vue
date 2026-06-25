<template>
  <div class="max-w-4xl mx-auto p-4 md:p-8 animate-fade-in">

    <div class="mb-8">
      <h1 class="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2 tracking-tight">Ayarlar</h1>
      <p class="text-slate-500 dark:text-slate-400">AI sağlayıcı ayarları ve marka kimliğini yapılandır.</p>
    </div>

    <div class="space-y-6">
      <!-- AI Settings Section -->
      <section class="card p-6">
        <div class="flex items-center gap-2 mb-6">
          <Cpu class="w-5 h-5 text-brand" />
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Yapay Zeka Ayarları</h2>
        </div>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">İçerik üretiminde kullanılacak AI modelini yapılandırın.</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">AI Sağlayıcı</label>
            <select v-model="settings.provider" class="input">
              <option value="gemini">Google Gemini</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Model Adı</label>
            <input type="text" v-model="settings.model_name" placeholder="Örn: gemini-2.5-flash veya gpt-4o" class="input" />
          </div>

          <div class="space-y-1.5 md:col-span-2">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">API Key</label>
            <input type="password" v-model="settings.api_key" placeholder="AI sağlayıcısının API anahtarı" class="input" />
          </div>
        </div>

        <button class="btn btn-primary w-full md:w-auto" @click="saveSettings" :disabled="aiStore.isLoading">
          <Loader2 v-if="aiStore.isLoading" class="w-4 h-4 animate-spin" />
          <span v-else>Kaydet</span>
        </button>
      </section>

      <!-- Brand Profile Section -->
      <section class="card p-6">
        <div class="flex items-center gap-2 mb-6">
          <Palette class="w-5 h-5 text-brand" />
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Marka Kimliği</h2>
        </div>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">Yapay zeka içerik üretirken bu marka kimliğini dikkate alacaktır.</p>

        <!-- File Upload -->
        <div class="border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-2xl p-8 text-center cursor-pointer hover:border-brand hover:bg-brand/5 dark:hover:bg-brand/10 transition-colors mb-6 group" @click="triggerBrandFileInput">
          <input type="file" ref="brandFileInput" @change="handleFileUpload" accept=".pdf,.docx,.txt" class="hidden" />
          <div class="flex flex-col items-center gap-3">
            <UploadCloud class="w-8 h-8 text-slate-400 group-hover:text-brand transition-colors" />
            <span v-if="isAnalyzing" class="text-sm font-medium text-slate-600 dark:text-slate-300">Analiz ediliyor...</span>
            <span v-else class="text-sm font-medium text-slate-600 dark:text-slate-300">Marka kimliği dosyası yükle (PDF, DOCX, TXT)</span>
          </div>
          <p class="text-xs text-slate-500 mt-2">Yapay zeka aşağıdaki alanları otomatik dolduracaktır.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Marka Adı</label>
            <input type="text" v-model="brand.brand_name" placeholder="Markanızın adı" class="input" />
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Marka Tonu</label>
            <select v-model="brand.tone" class="input">
              <option value="Profesyonel">Profesyonel</option>
              <option value="Samimi">Samimi</option>
              <option value="Eğlenceli">Eğlenceli</option>
              <option value="Ciddi">Ciddi</option>
              <option value="Mizahi">Mizahi</option>
            </select>
          </div>

          <div class="space-y-1.5 md:col-span-2">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Hedef Kitle</label>
            <textarea v-model="brand.target_audience" rows="2" placeholder="Örn: Genç profesyoneller, yazılımcılar, B2B şirketleri..." class="input resize-y"></textarea>
          </div>

          <div class="space-y-1.5 md:col-span-2">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Anahtar Kelimeler</label>
            <input type="text" v-model="keywordsString" placeholder="teknoloji, yazılım, inovasyon (virgülle ayırın)" class="input" />
          </div>
        </div>

        <button class="btn btn-primary w-full md:w-auto" @click="saveBrand" :disabled="aiStore.isLoading">
          <Loader2 v-if="aiStore.isLoading" class="w-4 h-4 animate-spin" />
          <span v-else>Marka Profilini Kaydet</span>
        </button>
      </section>

      <!-- Publish Settings Section -->
      <section class="card p-6">
        <div class="flex items-center gap-2 mb-6">
          <Image as="Image" class="w-5 h-5 text-brand" />
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Paylaşım ve Boyut Ayarları</h2>
        </div>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">Her platform için varsayılan görsel boyutlandırma (en-boy) oranlarını belirleyin. Görselleriniz yayınlanırken otomatik olarak bulanık arka plan (blur padding) ile bu oranlara uyarlanacaktır.</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Instagram En-Boy Oranı</label>
            <select v-model="publishSettings.instagram_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5) - Önerilen</option>
              <option value="1.91:1">Yatay (1.91:1)</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Facebook En-Boy Oranı</label>
            <select v-model="publishSettings.facebook_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5)</option>
              <option value="1.91:1">Yatay (1.91:1) - Önerilen</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">LinkedIn En-Boy Oranı</label>
            <select v-model="publishSettings.linkedin_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="4:5">Dikey (4:5)</option>
              <option value="1.91:1">Yatay (1.91:1) - Önerilen</option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">X (Twitter) En-Boy Oranı</label>
            <select v-model="publishSettings.twitter_aspect_ratio" class="input">
              <option value="1:1">Kare (1:1)</option>
              <option value="16:9">Geniş Ekran (16:9) - Önerilen</option>
              <option value="1.91:1">Yatay (1.91:1)</option>
            </select>
          </div>
        </div>

        <button class="btn btn-primary w-full md:w-auto" @click="savePublishSettings" :disabled="publishStore.isLoading">
          <Loader2 v-if="publishStore.isLoading" class="w-4 h-4 animate-spin" />
          <span v-else>Paylaşım Ayarlarını Kaydet</span>
        </button>
      </section>
    </div>

    <!-- Notifications -->
    <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      <transition 
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform translate-y-2 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform translate-y-2 opacity-0"
      >
        <div v-if="successMessage" class="flex items-center gap-3 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-600 dark:text-emerald-400 px-4 py-3 rounded-xl shadow-lg">
          <CheckCircle2 class="w-5 h-5" />
          <span class="text-sm font-medium">{{ successMessage }}</span>
        </div>
      </transition>
      
      <transition 
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div v-if="aiStore.error" class="flex items-center justify-between gap-3 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-600 dark:text-red-400 px-4 py-3 rounded-xl shadow-lg">
          <div class="flex items-center gap-3">
            <AlertCircle class="w-5 h-5 shrink-0" />
            <span class="text-sm font-medium">{{ aiStore.error }}</span>
          </div>
          <button @click="aiStore.clearError()" class="p-1 hover:bg-red-100 dark:hover:bg-red-500/20 rounded-lg transition-colors">
            <X class="w-4 h-4" />
          </button>
        </div>
      </transition>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAiStore } from '../stores/ai'
import { usePublishSettingsStore } from '../stores/publishSettings'
import { Cpu, Palette, UploadCloud, Image, Loader2, CheckCircle2, AlertCircle, X } from 'lucide-vue-next'

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
