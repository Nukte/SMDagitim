<template>
  <div class="bg-white dark:bg-black w-full h-full font-sans text-[14px] text-gray-900 dark:text-gray-100 p-3 flex flex-col">
    <!-- Header -->
    <div class="flex items-start gap-3 mb-2">
      <div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-800 shrink-0"></div>
      <div class="flex flex-col flex-1 min-w-0 leading-tight">
        <div class="flex items-center gap-1">
          <span class="font-bold truncate">Kullanıcı Adı</span>
          <span class="w-4 h-4 bg-blue-500 text-white rounded-full flex items-center justify-center text-[10px] shrink-0">✓</span>
        </div>
        <span class="text-[13px] text-gray-500 truncate">@kullanici · şimdi</span>
      </div>
      <div class="text-xl font-bold font-serif shrink-0 text-black dark:text-white">𝕏</div>
    </div>

    <!-- Content -->
    <div class="mb-3">
      <p class="whitespace-pre-wrap leading-normal break-words">{{ displayText }}</p>
      <div v-if="isOverLimit" class="mt-2 text-[12px] font-semibold text-red-500">
        ⚠️ {{ postStore.content.length - 280 }} karakter fazla
      </div>
      <div v-if="postStore.hashtags.length" class="mt-1.5 flex flex-wrap gap-1">
        <span v-for="tag in postStore.hashtags" :key="tag" class="text-blue-500 hover:underline">#{{ tag }}</span>
      </div>
    </div>

    <!-- Media -->
    <div 
      v-if="firstMedia" 
      class="w-full rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 mb-3 relative flex items-center justify-center" 
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

    <!-- Time -->
    <div class="text-[13px] text-gray-500 pb-3 border-b border-gray-100 dark:border-gray-800">
      {{ currentTime }} · <span class="hover:underline">X for Web</span>
    </div>

    <!-- Stats -->
    <div class="flex gap-4 py-3 border-b border-gray-100 dark:border-gray-800 text-[13px] text-gray-500">
      <span><strong class="text-black dark:text-white font-bold">0</strong> Repost</span>
      <span><strong class="text-black dark:text-white font-bold">0</strong> Alıntı</span>
      <span><strong class="text-black dark:text-white font-bold">0</strong> Beğeni</span>
      <span class="hidden sm:inline"><strong class="text-black dark:text-white font-bold">0</strong> Görüntüleme</span>
    </div>

    <!-- Actions -->
    <div class="flex justify-between items-center pt-3 text-gray-500 px-2">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 2.1l4 4-4 4"/><path d="M3 12.2v-2a4 4 0 0 1 4-4h12.8M7 21.9l-4-4 4-4"/><path d="M21 11.8v2a4 4 0 0 1-4 4H4.2"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><polyline points="14 2 14 8 20 8"/><path d="M2 15h10"/><path d="M9 18l3-3-3-3"/></svg>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/></svg>
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
  const ratio = publishSettings.settings?.twitter_aspect_ratio || '16:9'
  return ratio.replace(':', ' / ')
})
const firstMedia = computed(() => postStore.media[0] || null)

const isOverLimit = computed(() => postStore.content.length > 280)

const displayText = computed(() => {
  const text = postStore.content || 'Buraya tweet içeriği gelecek...'
  return text
})

const currentTime = computed(() => {
  const now = new Date()
  return now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) +
    ' · ' + now.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' })
})
</script>
