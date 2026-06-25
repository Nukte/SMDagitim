<template>
  <div>
    <div v-if="postStore.connectedAccounts.length === 0" class="text-sm text-slate-500 dark:text-slate-400 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-800">
      Hesap bulunamadı. Lütfen önce dashboard'dan hesap bağlayın.
    </div>

    <div class="space-y-3">
      <label
        v-for="account in postStore.connectedAccounts"
        :key="account.account_id"
        class="flex items-center gap-4 p-4 rounded-xl border cursor-pointer transition-all duration-200 select-none group"
        :class="[
          postStore.selectedAccounts.includes(account.account_id) 
            ? 'border-brand bg-brand/5 dark:bg-brand/10 shadow-sm shadow-brand/10' 
            : 'border-slate-200 dark:border-slate-700 hover:border-brand/50 hover:bg-slate-50 dark:hover:bg-slate-800/50'
        ]"
      >
        <input
          type="checkbox"
          :value="account.account_id"
          v-model="postStore.selectedAccounts"
          class="hidden"
        />
        
        <!-- Checkbox Indicator -->
        <div 
          class="w-6 h-6 rounded-md border flex items-center justify-center transition-colors duration-200 shrink-0"
          :class="postStore.selectedAccounts.includes(account.account_id) ? 'bg-brand border-brand text-white' : 'border-slate-300 dark:border-slate-600 text-transparent'"
        >
          <Check class="w-4 h-4" />
        </div>
        
        <!-- Icon -->
        <div class="text-xl" :style="{ color: getPlatform(account.platform)?.color }">
          {{ getPlatform(account.platform)?.icon }}
        </div>
        
        <!-- Details -->
        <div class="flex-1">
          <div class="font-medium text-slate-900 dark:text-white text-sm">
            {{ getPlatform(account.platform)?.name }}
          </div>
          <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 flex items-center gap-1">
            <span class="truncate max-w-[120px]">{{ account.account_name || 'İsimsiz' }}</span>
            <span v-if="account.target_language" class="px-1.5 py-0.5 rounded-md bg-slate-200 dark:bg-slate-700 text-[10px] uppercase font-bold">{{ account.target_language }}</span>
          </div>
        </div>
      </label>
    </div>
  </div>
</template>

<script setup>
import { usePostStore } from '../stores/post'
import { Check } from 'lucide-vue-next'

const postStore = usePostStore()

function getPlatform(platformId) {
  return postStore.platforms.find(p => p.id === platformId)
}
</script>
