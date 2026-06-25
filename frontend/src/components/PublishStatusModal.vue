<template>
  <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="$emit('close')">
    <div class="bg-white dark:bg-slate-900 rounded-2xl w-full max-w-md shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden animate-fade-in-up" @click.stop>
      <!-- Header -->
      <div class="flex items-center justify-between p-5 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-brand/10 text-brand flex items-center justify-center">
            <Send class="w-5 h-5" />
          </div>
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">Paylaşım Durumu</h3>
        </div>
        <button class="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors" @click="$emit('close')">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Body -->
      <div class="p-5 space-y-3">
        <div
          v-for="p in postStore.publishJob?.platforms || []"
          :key="p.platform"
          class="flex items-center gap-4 p-3 rounded-xl border transition-all duration-300"
          :class="{
            'bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700': p.status === 'pending' || p.status === 'publishing',
            'bg-emerald-50 dark:bg-emerald-500/10 border-emerald-200 dark:border-emerald-500/20': p.status === 'success',
            'bg-red-50 dark:bg-red-500/10 border-red-200 dark:border-red-500/20': p.status === 'error'
          }"
        >
          <!-- Status icon -->
          <div class="shrink-0 w-8 flex items-center justify-center">
            <Loader2 v-if="p.status === 'pending' || p.status === 'publishing'" class="w-5 h-5 text-brand animate-spin" />
            <div v-else-if="p.status === 'success'" class="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <Check class="w-4 h-4" stroke-width="3" />
            </div>
            <div v-else class="w-6 h-6 rounded-full bg-red-100 dark:bg-red-500/20 text-red-600 dark:text-red-400 flex items-center justify-center">
              <AlertCircle class="w-4 h-4" />
            </div>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="font-medium text-slate-900 dark:text-white text-sm">{{ platformName(p.platform) }}</div>
            <div class="text-xs font-medium mt-0.5" :class="{
              'text-amber-600 dark:text-amber-400': p.status === 'publishing',
              'text-emerald-600 dark:text-emerald-400': p.status === 'success',
              'text-red-600 dark:text-red-400': p.status === 'error',
              'text-slate-500 dark:text-slate-400': p.status === 'pending'
            }">{{ statusText(p.status) }}</div>
            <div v-if="p.error_message" class="text-xs text-red-500 mt-1 truncate">{{ p.error_message }}</div>
          </div>

          <!-- Link -->
          <a v-if="p.post_url" :href="p.post_url" target="_blank" class="shrink-0 px-3 py-1.5 bg-brand/10 text-brand text-xs font-bold rounded-full hover:bg-brand hover:text-white transition-colors flex items-center gap-1">
            Görüntüle
            <ExternalLink class="w-3 h-3" />
          </a>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="allDone" class="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 flex items-center justify-between">
        <div v-if="allSuccess" class="flex items-center gap-2 text-sm font-medium text-emerald-600 dark:text-emerald-400">
          <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          Tüm paylaşımlar tamamlandı!
        </div>
        <div v-else class="text-sm font-medium text-slate-500">İşlem tamamlandı.</div>
        
        <button class="btn btn-primary px-6" @click="$emit('close')">Kapat</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../stores/post'
import { Send, X, Loader2, Check, AlertCircle, ExternalLink } from 'lucide-vue-next'

const postStore = usePostStore()
defineEmits(['close'])

const allDone = computed(() => {
  const ps = postStore.publishJob?.platforms || []
  return ps.length > 0 && ps.every(p => p.status === 'success' || p.status === 'error')
})

const allSuccess = computed(() =>
  (postStore.publishJob?.platforms || []).every(p => p.status === 'success')
)

const PLATFORM_NAMES = {
  instagram: 'Instagram',
  facebook:  'Facebook',
  twitter:   'X',
  linkedin:  'LinkedIn',
}
const STATUS_TEXT = {
  pending:    'Bekliyor...',
  publishing: 'Gönderiliyor...',
  success:    'Başarıyla Paylaşıldı',
  error:      'Hata Oluştu',
}

function platformName(id) { return PLATFORM_NAMES[id] || id }
function statusText(s)    { return STATUS_TEXT[s] || s }
</script>
