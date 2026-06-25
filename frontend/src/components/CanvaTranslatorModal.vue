<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
    <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-xl w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-gradient-to-r from-blue-500/10 to-cyan-500/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-600 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Canva Tasarım Çevirisi</h2>
            <p class="text-xs text-slate-500">Çoklu dil desteği ile tasarımları otomatik çevirin</p>
          </div>
        </div>
        <button @click="$emit('close')" class="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
      </div>

      <!-- Content -->
      <div class="p-6 overflow-y-auto flex-1">
        
        <div v-if="canvaStore.error" class="mb-6 p-3 bg-red-50 dark:bg-red-500/10 text-red-600 dark:text-red-400 text-sm rounded-xl border border-red-200 dark:border-red-500/20">
          {{ canvaStore.error }}
        </div>

        <!-- Not Connected State -->
        <div v-if="!canvaStore.isConnected" class="text-center py-8">
          <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-3xl mx-auto mb-4">🎨</div>
          <h3 class="text-lg font-medium text-slate-900 dark:text-white mb-2">Canva Hesabınızı Bağlayın</h3>
          <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">Tasarımlarınızı doğrudan okuyabilmemiz ve çevirip yeni kopyalar oluşturabilmemiz için Canva yetkisi gereklidir.</p>
          <button @click="canvaStore.connectCanva()" class="btn btn-primary px-6 py-2.5">
            Canva ile Giriş Yap
          </button>
        </div>

        <!-- Connected State -->
        <div v-else class="space-y-6">
          <div class="flex items-center justify-between p-3 bg-emerald-50 dark:bg-emerald-500/10 rounded-xl border border-emerald-200 dark:border-emerald-500/20">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span class="text-sm font-medium text-emerald-700 dark:text-emerald-400">Bağlı: {{ canvaStore.accountName || 'Canva Hesabı' }}</span>
            </div>
            <span class="text-xs text-emerald-600 dark:text-emerald-500 bg-emerald-100 dark:bg-emerald-500/20 px-2 py-1 rounded-md">MCP Aktif</span>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Canva Tasarım Linki</label>
            <input 
              type="text" 
              v-model="designUrl" 
              placeholder="Örn: https://www.canva.com/design/DAF.../edit" 
              class="input w-full"
            />
            <p class="text-xs text-slate-500 mt-1">Sadece okuma ve yazma izni olan tasarım linklerini giriniz.</p>
          </div>

          <div class="space-y-1.5">
            <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Hedef Dil</label>
            <select v-model="targetLanguage" class="input w-full">
              <option value="İngilizce">İngilizce (English)</option>
              <option value="Almanca">Almanca (Deutsch)</option>
              <option value="Fransızca">Fransızca (Français)</option>
              <option value="İspanyolca">İspanyolca (Español)</option>
              <option value="Arapça">Arapça (العربية)</option>
              <option value="Rusça">Rusça (Русский)</option>
            </select>
          </div>

          <div v-if="successMessage" class="p-3 bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 text-sm rounded-xl border border-blue-200 dark:border-blue-500/20">
            {{ successMessage }}
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div v-if="canvaStore.isConnected" class="px-6 py-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 flex justify-end gap-3">
        <button @click="$emit('close')" class="btn bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700">
          İptal
        </button>
        <button 
          @click="handleTranslate" 
          :disabled="!designUrl || canvaStore.isLoading" 
          class="btn btn-primary"
        >
          <svg v-if="canvaStore.isLoading" class="w-4 h-4 animate-spin mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          <span v-else>Çevir ve Kopyasını Oluştur</span>
        </button>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCanvaStore } from '../stores/canva'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close', 'translated'])

const canvaStore = useCanvaStore()
const designUrl = ref('')
const targetLanguage = ref('İngilizce')
const successMessage = ref('')

onMounted(() => {
  canvaStore.checkStatus()
})

async function handleTranslate() {
  successMessage.value = ''
  try {
    const result = await canvaStore.translateDesign(designUrl.value, targetLanguage.value)
    successMessage.value = `Çeviri başarılı! Yeni tasarım oluşturuldu: ${result.translated_url}`
    // İsterseniz yeni tasarımı postStore'a veya ilgili yere yollayabilirsiniz
    setTimeout(() => {
      emit('translated', result)
      emit('close')
    }, 3000)
  } catch (e) {
    // Error is handled in store
  }
}
</script>
