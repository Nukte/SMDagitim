<template>
  <div class="space-y-5">
    <!-- Text Area -->
    <div class="space-y-2">
      <div class="relative">
        <textarea
          v-model="postStore.content"
          class="input w-full min-h-[160px] resize-y p-4 bg-slate-50 dark:bg-slate-900 focus:bg-white dark:focus:bg-slate-800 transition-colors"
          placeholder="Bugün kitlenizle ne paylaşmak istersiniz?..."
          :maxlength="postStore.currentMinChars"
        ></textarea>
        <!-- Character Counter -->
        <div class="absolute bottom-3 right-3 text-xs font-medium bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm px-2 py-1 rounded-md border border-slate-200 dark:border-slate-700"
             :class="{ 'text-amber-500': charRatio > 0.9 && charRatio <= 0.95, 'text-red-500': charRatio > 0.95, 'text-slate-500': charRatio <= 0.9 }">
          {{ postStore.content.length }} / {{ postStore.currentMinChars }}
        </div>
      </div>
    </div>

    <!-- Hashtags -->
    <div class="space-y-2">
      <label class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-2">
        <Hash class="w-3.5 h-3.5" />
        Etiketler
      </label>
      <div class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus-within:ring-2 focus-within:ring-brand/20 focus-within:border-brand transition-all duration-200 min-h-[52px]">
        <div class="flex flex-wrap gap-2 mb-2" v-if="postStore.hashtags.length > 0">
          <span
            v-for="(tag, index) in postStore.hashtags"
            :key="index"
            class="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 dark:bg-indigo-500/10 text-brand dark:text-indigo-400 border border-indigo-100 dark:border-indigo-500/20 text-xs font-semibold rounded-full group transition-colors hover:bg-indigo-100 dark:hover:bg-indigo-500/20"
          >
            #{{ tag }}
            <button @click="removeHashtag(index)" class="w-4 h-4 rounded-full flex items-center justify-center text-indigo-400 hover:bg-indigo-200 dark:hover:bg-indigo-500/30 hover:text-indigo-600 dark:hover:text-white transition-colors">
              <X class="w-3 h-3" />
            </button>
          </span>
        </div>
        <input
          v-model="newHashtag"
          class="w-full bg-transparent border-none text-sm text-slate-900 dark:text-white focus:outline-none placeholder:text-slate-400"
          placeholder="Etiket yazıp Enter'a basın..."
          @keydown.enter.prevent="addHashtag"
          @keydown.space.prevent="addHashtag"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePostStore } from '../stores/post'
import { Hash, X } from 'lucide-vue-next'

const postStore = usePostStore()
const newHashtag = ref('')

const charRatio = computed(() => {
  return postStore.content.length / postStore.currentMinChars
})

function addHashtag() {
  const tag = newHashtag.value.trim().replace(/^#/, '')
  if (tag && !postStore.hashtags.includes(tag)) {
    postStore.hashtags.push(tag)
  }
  newHashtag.value = ''
}

function removeHashtag(index) {
  postStore.hashtags.splice(index, 1)
}
</script>
