<template>
  <div class="bg-white w-full h-full font-sans text-[13px] text-gray-900 flex flex-col">
    <!-- Header -->
    <div class="flex items-center gap-2.5 p-3">
      <div class="w-10 h-10 rounded-full bg-blue-600 shrink-0"></div>
      <div class="flex flex-col flex-1 min-w-0 justify-center">
        <span class="font-bold leading-tight flex items-center gap-1">
          Sayfa Adı
          <span class="w-3.5 h-3.5 bg-blue-500 rounded-full text-white flex items-center justify-center text-[8px]">✓</span>
        </span>
        <div class="text-[11px] text-gray-500 flex items-center gap-1 leading-tight mt-0.5">
          <span>Şimdi</span>
          <span>·</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
        </div>
      </div>
      <button class="text-gray-500 p-1 font-bold text-lg mb-2">⋯</button>
    </div>

    <!-- Content -->
    <div class="px-3 pb-2 flex-1">
      <p class="whitespace-pre-wrap leading-relaxed">{{ displayText }}</p>
      <div v-if="postStore.hashtags.length" class="mt-1.5 flex flex-wrap gap-1">
        <span v-for="tag in postStore.hashtags" :key="tag" class="text-blue-600 font-medium">#{{ tag }}</span>
      </div>
    </div>

    <!-- Media -->
    <div 
      v-if="firstMedia" 
      class="w-full bg-gray-100 flex items-center justify-center overflow-hidden"
      :style="{ aspectRatio: formattedAspectRatio }"
    >
      <img
        v-if="firstMedia.media_type === 'image'"
        :src="firstMedia.localPreview || firstMedia.public_url"
        alt=""
        class="w-full h-full object-cover block"
      />
      <div v-else class="text-gray-400">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      </div>
    </div>

    <!-- Reactions Bar -->
    <div class="flex justify-between items-center px-3 py-2 text-[11px] text-gray-500 border-b border-gray-200/60">
      <div class="flex items-center gap-1.5">
        <div class="flex -space-x-1">
          <div class="w-[18px] h-[18px] rounded-full bg-blue-500 flex items-center justify-center text-white text-[10px] border border-white z-20">👍</div>
          <div class="w-[18px] h-[18px] rounded-full bg-red-500 flex items-center justify-center text-white text-[10px] border border-white z-10">❤️</div>
        </div>
        <span>42</span>
      </div>
      <div class="flex gap-2">
        <span>5 yorum</span>
        <span>2 paylaşım</span>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex px-1 py-1">
      <button class="flex-1 flex items-center justify-center gap-2 py-1.5 text-gray-500 font-medium rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
        Beğen
      </button>
      <button class="flex-1 flex items-center justify-center gap-2 py-1.5 text-gray-500 font-medium rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
        Yorum Yap
      </button>
      <button class="flex-1 flex items-center justify-center gap-2 py-1.5 text-gray-500 font-medium rounded-md hover:bg-gray-100 transition-colors">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/></svg>
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
  const ratio = publishSettings.settings?.facebook_aspect_ratio || '1.91:1'
  return ratio.replace(':', ' / ')
})
const firstMedia = computed(() => postStore.media[0] || null)

const displayText = computed(() => {
  return postStore.content || 'Buraya post içeriği gelecek...'
})
</script>
