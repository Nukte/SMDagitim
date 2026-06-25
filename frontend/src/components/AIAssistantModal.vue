<template>
  <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" v-if="show" @click.self="close">
    <div class="bg-white dark:bg-slate-900 rounded-2xl w-full max-w-lg shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden animate-fade-in-up">
      <!-- Header -->
      <div class="flex items-center justify-between p-5 border-b border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-500/10 text-brand flex items-center justify-center">
            <Sparkles class="w-5 h-5" />
          </div>
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">AI İçerik Üreticisi</h3>
        </div>
        <button class="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors" @click="close">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Body -->
      <div class="p-6 space-y-6">
        <div class="space-y-2">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300">Konu veya İstek</label>
          <textarea
            v-model="topic"
            rows="3"
            class="input w-full resize-none bg-slate-50 dark:bg-slate-950 focus:bg-white dark:focus:bg-slate-900"
            placeholder="Örn: Yeni ürünümüz hakkında heyecan verici bir duyuru..."
            :disabled="aiStore.isLoading"
          ></textarea>
        </div>

        <label class="flex items-center gap-3 cursor-pointer group">
          <div class="relative flex items-center justify-center">
            <input type="checkbox" v-model="generateImage" :disabled="aiStore.isLoading" class="peer sr-only" />
            <div class="w-5 h-5 border-2 border-slate-300 dark:border-slate-600 rounded bg-white dark:bg-slate-800 peer-checked:bg-brand peer-checked:border-brand transition-colors"></div>
            <Check class="w-3.5 h-3.5 text-white absolute opacity-0 peer-checked:opacity-100 transition-opacity" stroke-width="3" />
          </div>
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white transition-colors">AI ile Görsel Üret</span>
        </label>

        <div v-if="aiStore.isLoading" class="flex flex-col items-center justify-center py-6 gap-4">
          <Loader2 class="w-8 h-8 text-brand animate-spin" />
          <p class="text-sm font-medium text-slate-500 dark:text-slate-400 animate-pulse">AI içeriği hazırlıyor, lütfen bekleyin...</p>
        </div>

        <transition 
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-2"
        >
          <div v-if="aiStore.error" class="p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-600 dark:text-red-400 rounded-xl text-sm font-medium flex items-start justify-between gap-3">
            <div class="flex items-start gap-3">
              <AlertCircle class="w-5 h-5 shrink-0 mt-0.5" />
              <span>{{ aiStore.error }}</span>
            </div>
            <button @click="aiStore.clearError()" class="p-1 -mt-1 -mr-1 hover:bg-red-100 dark:hover:bg-red-500/20 rounded-lg transition-colors shrink-0">
              <X class="w-4 h-4" />
            </button>
          </div>
        </transition>
      </div>

      <!-- Footer -->
      <div class="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50 flex justify-end gap-3">
        <button class="btn btn-secondary px-6" @click="close" :disabled="aiStore.isLoading">İptal</button>
        <button class="btn btn-primary px-6 bg-gradient-to-r from-indigo-500 to-purple-500 border-0 hover:from-indigo-600 hover:to-purple-600 shadow-lg shadow-indigo-500/25" @click="generate" :disabled="!topic.trim() || aiStore.isLoading">
          <Sparkles class="w-4 h-4 mr-2" />
          İçerik Üret
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAiStore } from '../stores/ai'
import { Sparkles, X, Check, Loader2, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close', 'generated'])

const aiStore = useAiStore()
const topic = ref('')
const generateImage = ref(true)

const close = () => {
  if (aiStore.isLoading) return
  emit('close')
}

const generate = async () => {
  if (!topic.value.trim()) return

  try {
    const result = await aiStore.generateContent(topic.value, generateImage.value)
    emit('generated', result)
    close()
    topic.value = ''
  } catch (e) {
    // Error is handled in the store
  }
}
</script>
