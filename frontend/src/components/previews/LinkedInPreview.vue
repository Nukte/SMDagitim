<template>
  <div class="bg-white w-full h-full font-sans text-[14px] text-gray-900 flex flex-col">
    <!-- Header -->
    <div class="flex gap-3 p-3 mb-1">
      <div class="w-12 h-12 rounded-full bg-[#0A66C2] shrink-0"></div>
      <div class="flex flex-col flex-1 min-w-0 leading-tight">
        <span class="font-bold text-gray-900">Profil Adı</span>
        <span class="text-[12px] text-gray-500 mt-0.5">Yazılım Geliştirici</span>
        <span class="text-[11px] text-gray-500 mt-0.5 flex items-center gap-1">Şimdi · <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg></span>
      </div>
    </div>

    <!-- Content -->
    <div class="px-3 pb-2 flex-1">
      <p class="whitespace-pre-wrap leading-snug">{{ postStore.content || 'LinkedIn post içeriği...' }}</p>
      <div v-if="postStore.hashtags.length" class="mt-2 flex flex-wrap gap-1">
        <span v-for="tag in postStore.hashtags" :key="tag" class="text-[#0A66C2] font-semibold">#{{ tag }}</span>
      </div>
    </div>

    <!-- Media -->
    <div 
      v-if="postStore.media[0]" 
      class="w-full bg-gray-100 flex items-center justify-center overflow-hidden"
      :style="{ aspectRatio: formattedAspectRatio }"
    >
      <img v-if="postStore.media[0].media_type === 'image'" :src="postStore.media[0].localPreview || postStore.media[0].public_url" alt="" class="w-full h-full object-cover block" />
      <div v-else class="text-gray-400">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      </div>
    </div>

    <!-- Reactions -->
    <div class="flex justify-between items-center px-3 py-2 border-b border-gray-200/60 text-[12px] text-gray-500">
      <div class="flex items-center gap-1">
        <div class="flex -space-x-1">
          <div class="w-4 h-4 rounded-full bg-[#0A66C2] flex items-center justify-center text-white text-[8px] z-30">👍</div>
          <div class="w-4 h-4 rounded-full bg-yellow-500 flex items-center justify-center text-white text-[8px] z-20">💡</div>
          <div class="w-4 h-4 rounded-full bg-red-500 flex items-center justify-center text-white text-[8px] z-10">❤️</div>
        </div>
        <span class="ml-1">12</span>
      </div>
      <span>3 yorum</span>
    </div>

    <!-- Actions -->
    <div class="flex px-1 py-1">
      <button class="flex-1 flex items-center justify-center gap-2 py-3 text-gray-500 font-semibold text-[13px] rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
        Beğen
      </button>
      <button class="flex-1 flex items-center justify-center gap-2 py-3 text-gray-500 font-semibold text-[13px] rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
        Yorum
      </button>
      <button class="flex-1 flex items-center justify-center gap-2 py-3 text-gray-500 font-semibold text-[13px] rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 2.1l4 4-4 4"/><path d="M3 12.2v-2a4 4 0 0 1 4-4h12.8M7 21.9l-4-4 4-4"/><path d="M21 11.8v2a4 4 0 0 1-4 4H4.2"/></svg>
        Paylaş
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../../stores/post'
import { usePublishSettingsStore } from '../../stores/publishSettings'

const postStore = usePostStore()
const publishSettings = usePublishSettingsStore()

const formattedAspectRatio = computed(() => {
  const ratio = publishSettings.settings?.linkedin_aspect_ratio || '1.91:1'
  return ratio.replace(':', ' / ')
})
</script>
