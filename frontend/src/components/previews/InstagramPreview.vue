<template>
  <div class="overflow-hidden bg-white w-full h-full font-sans text-[13px]">
    <!-- Header -->
    <div class="flex items-center gap-2.5 p-2.5 border-b border-gray-100">
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-yellow-400 via-red-500 to-fuchsia-600 p-[2px] shrink-0">
        <div class="w-full h-full rounded-full bg-gray-200 border-2 border-white"></div>
      </div>
      <div class="flex flex-col flex-1 min-w-0">
        <span class="font-semibold text-gray-900 leading-tight">kullanici_adi</span>
        <span class="text-[11px] text-gray-900 leading-tight">Konum</span>
      </div>
      <button class="p-1 text-gray-900 flex items-center justify-center">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle cx="6" cy="12" r="1.5" fill="currentColor"/>
          <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
          <circle cx="18" cy="12" r="1.5" fill="currentColor"/>
        </svg>
      </button>
    </div>

    <!-- Media -->
    <div 
      class="relative bg-gray-50 flex items-center justify-center w-full overflow-hidden"
      :style="{ aspectRatio: formattedAspectRatio }"
    >
      <img
        v-if="firstMedia && firstMedia.media_type === 'image'"
        :src="firstMedia.localPreview || firstMedia.public_url"
        alt="Post preview"
        class="w-full h-full object-cover block"
      />
      <div v-else-if="firstMedia && firstMedia.media_type === 'video'" class="flex flex-col items-center justify-center gap-2 text-gray-400">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
        <span class="text-sm">Video</span>
      </div>
      <div v-else class="flex flex-col items-center justify-center gap-2 text-gray-400 opacity-50">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
        <span class="text-sm">Medya yüklenmedi</span>
      </div>

      <!-- Carousel dots -->
      <div v-if="postStore.media.length > 1" class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1">
        <span
          v-for="(_, i) in postStore.media"
          :key="i"
          class="w-1.5 h-1.5 rounded-full transition-colors duration-200"
          :class="i === 0 ? 'bg-blue-500' : 'bg-white/40'"
        ></span>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-between px-3 pt-2 pb-1 text-gray-900">
      <div class="flex gap-3.5">
        <button class="p-0.5">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </button>
        <button class="p-0.5">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
        </button>
        <button class="p-0.5">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
      <button class="p-0.5">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
      </button>
    </div>

    <!-- Likes -->
    <div class="px-3.5 pt-0.5 font-semibold text-gray-900">1,234 beğenme</div>

    <!-- Caption -->
    <div class="px-3.5 py-1 text-gray-900 leading-snug">
      <span class="font-semibold mr-1.5">kullanici_adi</span>
      <span class="font-normal">{{ displayCaption }}</span>
    </div>

    <!-- Hashtags -->
    <div v-if="postStore.hashtags.length" class="px-3.5 pb-1 flex flex-wrap gap-1">
      <span v-for="tag in postStore.hashtags" :key="tag" class="text-[#00376b]">#{{ tag }}</span>
    </div>

    <!-- Time -->
    <div class="px-3.5 pb-3 pt-1 text-[10px] text-gray-500 uppercase tracking-wide">ŞİMDİ</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../../stores/post'
import { usePublishSettingsStore } from '../../stores/publishSettings'

const postStore = usePostStore()
const publishSettings = usePublishSettingsStore()

const firstMedia = computed(() => postStore.media[0] || null)

const formattedAspectRatio = computed(() => {
  const ratio = publishSettings.settings?.instagram_aspect_ratio || '4:5'
  return ratio.replace(':', ' / ')
})

const displayCaption = computed(() => {
  const text = postStore.content || 'Buraya post içeriği gelecek...'
  return text.length > 150 ? text.substring(0, 150) + '... daha fazla' : text
})
</script>
