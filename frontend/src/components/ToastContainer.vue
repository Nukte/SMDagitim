<template>
  <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none max-w-[360px] w-[calc(100vw-2rem)]">
    <transition-group 
      enter-active-class="transition-all duration-400 ease-[cubic-bezier(0.175,0.885,0.32,1.275)]"
      enter-from-class="opacity-0 translate-x-[50px] scale-90"
      enter-to-class="opacity-100 translate-x-0 scale-100"
      leave-active-class="transition-all duration-300 ease-in absolute w-full"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-5 scale-90"
      move-class="transition-transform duration-400 ease-in-out"
    >
      <div 
        v-for="item in toast.toasts.value" 
        :key="item.id" 
        class="flex items-start gap-3 p-4 bg-white dark:bg-slate-900 rounded-xl shadow-xl border border-slate-100 dark:border-slate-800 pointer-events-auto relative overflow-hidden group"
        :class="[
          item.type === 'success' ? 'border-l-4 border-l-emerald-500' :
          item.type === 'error' ? 'border-l-4 border-l-red-500' :
          item.type === 'warning' ? 'border-l-4 border-l-amber-500' :
          'border-l-4 border-l-indigo-500'
        ]"
      >
        <!-- Background Tint -->
        <div class="absolute inset-0 opacity-5 pointer-events-none" :class="[
          item.type === 'success' ? 'bg-emerald-500' :
          item.type === 'error' ? 'bg-red-500' :
          item.type === 'warning' ? 'bg-amber-500' :
          'bg-indigo-500'
        ]"></div>

        <!-- Icon -->
        <div class="shrink-0 flex items-center justify-center mt-0.5" :class="[
          item.type === 'success' ? 'text-emerald-500' :
          item.type === 'error' ? 'text-red-500' :
          item.type === 'warning' ? 'text-amber-500' :
          'text-indigo-500'
        ]">
          <CheckCircle2 v-if="item.type === 'success'" class="w-5 h-5" />
          <XCircle v-else-if="item.type === 'error'" class="w-5 h-5" />
          <AlertTriangle v-else-if="item.type === 'warning'" class="w-5 h-5" />
          <Info v-else class="w-5 h-5" />
        </div>

        <!-- Content -->
        <div class="flex-1 text-sm font-medium text-slate-800 dark:text-slate-200 leading-relaxed pt-px">
          {{ item.message }}
        </div>

        <!-- Close Button -->
        <button 
          class="shrink-0 p-1 -m-1 -mr-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors" 
          @click="toast.removeToast(item.id)"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { toast } from '../utils/toast'
import { CheckCircle2, XCircle, AlertTriangle, Info, X } from 'lucide-vue-next'
</script>
