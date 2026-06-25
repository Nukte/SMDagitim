<template>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div v-if="isOpen" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4" @click="cancel">
      <div class="bg-white dark:bg-slate-900 rounded-2xl w-full max-w-sm shadow-2xl border border-slate-200 dark:border-slate-800 p-6 text-center transform transition-all" @click.stop>
        
        <div class="mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-5" :class="{
          'bg-amber-100 dark:bg-amber-500/20 text-amber-500': type === 'warning',
          'bg-red-100 dark:bg-red-500/20 text-red-500': type === 'danger',
          'bg-indigo-100 dark:bg-indigo-500/20 text-indigo-500': type === 'info'
        }">
          <AlertTriangle v-if="type === 'warning'" class="w-8 h-8" />
          <XCircle v-else-if="type === 'danger'" class="w-8 h-8" />
          <Info v-else class="w-8 h-8" />
        </div>
        
        <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-2">{{ title }}</h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-8 leading-relaxed">{{ message }}</p>
        
        <div class="flex gap-3 w-full">
          <button class="btn btn-secondary flex-1" @click="cancel">{{ cancelText }}</button>
          <button class="btn flex-1" :class="{
            'btn-primary': type === 'warning',
            'btn-danger': type === 'danger',
            'btn-primary': type === 'info' // Assuming primary maps well to info actions
          }" @click="confirm" :disabled="loading">
            <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
            <span v-else>{{ confirmText }}</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { AlertTriangle, XCircle, Info, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  title: { type: String, default: 'Emin misiniz?' },
  message: { type: String, default: 'Bu işlemi onaylıyor musunuz?' },
  confirmText: { type: String, default: 'Onayla' },
  cancelText: { type: String, default: 'İptal' },
  type: { type: String, default: 'warning' }, // warning, danger, info
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['confirm', 'cancel'])

const isOpen = ref(false)

const open = () => {
  isOpen.value = true
}

const close = () => {
  isOpen.value = false
}

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
  close()
}

defineExpose({ open, close })
</script>
