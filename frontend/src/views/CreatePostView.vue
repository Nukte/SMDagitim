<template>
  <div class="max-w-7xl mx-auto p-4 md:p-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
      <div>
        <h1 class="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2 tracking-tight">Gönderi Oluştur</h1>
        <p class="text-slate-500 dark:text-slate-400">İçeriğinizi hazırlayın, önizleyin ve tüm platformlarda tek tıkla paylaşın.</p>
      </div>
      <div class="flex gap-3">
        <button class="btn bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600 border-0 shadow-lg shadow-blue-500/25" @click="showCanvaModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/></svg>
          Canva Çeviri
        </button>
        <button class="btn bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600 border-0 shadow-lg shadow-indigo-500/25" @click="showAIModal = true">
          <Sparkles class="w-5 h-5" />
          AI ile Üret
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      <!-- Left Column — Editor -->
      <div class="lg:col-span-7 flex flex-col gap-6">
        <div class="card p-6 shadow-sm">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-white mb-4 uppercase tracking-wide">1. Medya Yükle</h3>
          <MediaUploader />
        </div>
        
        <div class="card p-6 shadow-sm relative overflow-hidden">
          <!-- decorative blur -->
          <div class="absolute -top-10 -right-10 w-32 h-32 bg-brand/5 rounded-full blur-2xl pointer-events-none"></div>
          <h3 class="text-sm font-semibold text-slate-900 dark:text-white mb-4 uppercase tracking-wide">2. İçerik</h3>
          <PostEditor />
        </div>
        
        <div class="card p-6 shadow-sm">
          <h3 class="text-sm font-semibold text-slate-900 dark:text-white mb-4 uppercase tracking-wide">3. Hedef Platformlar</h3>
          <PlatformSelector />
        </div>

        <button
          class="btn btn-primary w-full py-4 text-lg mt-4 shadow-lg shadow-brand/20 rounded-2xl"
          :disabled="!canPublish || postStore.isPublishing"
          @click="handlePublish"
        >
          <Loader2 v-if="postStore.isPublishing" class="w-6 h-6 animate-spin" />
          <template v-else>
            <Send class="w-5 h-5" />
            Şimdi Paylaş
          </template>
        </button>
      </div>

      <!-- Right Column — Preview -->
      <div class="lg:col-span-5 lg:sticky lg:top-24 mt-8 lg:mt-0">
        <div class="card overflow-hidden border-slate-200/60 dark:border-slate-800/60 shadow-xl shadow-slate-200/50 dark:shadow-none">
          <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50 backdrop-blur-sm">
            <h3 class="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
              <Eye class="w-4 h-4 text-slate-400" />
              Canlı Ön İzleme
            </h3>
          </div>

          <!-- Tab selector -->
          <div class="flex overflow-x-auto border-b border-slate-100 dark:border-slate-800 scrollbar-hide">
            <button
              v-for="tab in previewTabs"
              :key="tab.id"
              class="flex-1 min-w-[100px] flex items-center justify-center gap-2 py-3 px-4 text-sm font-medium transition-all relative"
              :class="activePreview === tab.id ? 'text-brand' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/50'"
              @click="activePreview = tab.id"
            >
              <span class="text-lg">{{ tab.icon }}</span>
              <span class="hidden sm:inline">{{ tab.name }}</span>
              <!-- Active Indicator -->
              <div v-if="activePreview === tab.id" class="absolute bottom-0 left-0 right-0 h-0.5 bg-brand rounded-t-full"></div>
            </button>
          </div>

          <!-- Preview Area -->
          <div class="p-6 min-h-[500px] bg-slate-50/50 dark:bg-slate-950/50 flex items-center justify-center">
            <div class="w-full max-w-[380px] bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden transform transition-all duration-300 hover:shadow-md">
              <InstagramPreview v-if="activePreview === 'instagram'" />
              <FacebookPreview  v-if="activePreview === 'facebook'" />
              <TwitterPreview   v-if="activePreview === 'twitter'" />
              <LinkedInPreview  v-if="activePreview === 'linkedin'" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <PublishStatusModal v-if="showStatusModal" @close="closeModal" />
    <AIAssistantModal v-if="showAIModal" :show="showAIModal" @close="showAIModal = false" @generated="handleAIGenerated" />
    <CanvaTranslatorModal v-if="showCanvaModal" :show="showCanvaModal" @close="showCanvaModal = false" @translated="handleCanvaTranslated" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { usePostStore } from '../stores/post'
import MediaUploader    from '../components/MediaUploader.vue'
import PostEditor       from '../components/PostEditor.vue'
import PlatformSelector from '../components/PlatformSelector.vue'
import InstagramPreview from '../components/previews/InstagramPreview.vue'
import FacebookPreview  from '../components/previews/FacebookPreview.vue'
import TwitterPreview   from '../components/previews/TwitterPreview.vue'
import LinkedInPreview  from '../components/previews/LinkedInPreview.vue'
import PublishStatusModal from '../components/PublishStatusModal.vue'
import AIAssistantModal from '../components/AIAssistantModal.vue'
import CanvaTranslatorModal from '../components/CanvaTranslatorModal.vue'
import { Sparkles, Send, Eye, Loader2 } from 'lucide-vue-next'

const router    = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()

const activePreview  = ref('instagram')
const showStatusModal = ref(false)
const showAIModal = ref(false)
const showCanvaModal = ref(false)

const previewTabs = [
  { id: 'instagram', name: 'Instagram', icon: '📸', color: '#E1306C' },
  { id: 'facebook',  name: 'Facebook',  icon: '📘', color: '#1877F2' },
  { id: 'twitter',   name: 'X',         icon: '𝕏',  color: '#000' },
  { id: 'linkedin',  name: 'LinkedIn',  icon: '💼', color: '#0A66C2' },
]

const canPublish = computed(() =>
  postStore.selectedAccounts.length > 0 &&
  (postStore.content.trim().length > 0 || postStore.media.length > 0)
)

async function handlePublish() {
  showStatusModal.value = true
  try {
    const result = await postStore.publishPost()
    const interval = setInterval(async () => {
      const status = await postStore.pollPublishStatus(result.job_id)
      const done   = status.platforms.every(p => p.status === 'success' || p.status === 'error')
      if (done) { clearInterval(interval); postStore.isPublishing = false }
    }, 1500)
  } catch (e) {
    postStore.isPublishing = false
    alert('Paylaşım başlatılırken hata: ' + (e.response?.data?.detail || e.message))
  }
}

function closeModal() {
  showStatusModal.value = false
  if (!postStore.isPublishing) postStore.resetForm()
}

function handleAIGenerated(result) {
  postStore.content = result.content
  postStore.hashtags = result.hashtags || []
  if (result.media_url) {
    postStore.addMedia({
      public_url: result.media_url,
      object_key: result.media_key || 'ai-generated-' + Date.now(),
      media_type: 'image'
    })
  }
}

function handleCanvaTranslated(result) {
  // Canva'dan dönen yeni linki içeriğe ekleyebiliriz
  postStore.content += `\n\n🌍 Çevrilen Tasarım Linki:\n${result.translated_url}`
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
