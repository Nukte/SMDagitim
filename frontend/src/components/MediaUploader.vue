<template>
  <div class="space-y-4">
    <!-- Drop Zone -->
    <div
      class="border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200"
      :class="[
        isDragOver ? 'border-brand bg-brand/5 scale-[1.02]' : 'border-slate-200 dark:border-slate-700 hover:border-brand hover:bg-slate-50 dark:hover:bg-slate-800/50',
        postStore.media.length > 0 ? 'p-6' : 'p-12'
      ]"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <template v-if="postStore.media.length === 0 && !isUploading">
        <div class="flex flex-col items-center gap-3">
          <div class="w-16 h-16 rounded-2xl bg-brand/10 dark:bg-brand/20 text-brand dark:text-brand-light flex items-center justify-center mb-2">
            <UploadCloud class="w-8 h-8" />
          </div>
          <p class="font-medium text-slate-900 dark:text-white">Dosyaları sürükle & bırak veya seçmek için tıkla</p>
          <p class="text-xs text-slate-500 dark:text-slate-400">JPG, PNG, GIF, MP4, MOV • Maks 500MB</p>
        </div>
      </template>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/*,video/*"
      multiple
      class="hidden"
      @change="handleFileSelect"
    />

    <!-- Upload Progress -->
    <div v-if="isUploading" class="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4 border border-slate-100 dark:border-slate-800">
      <div class="flex justify-between items-center mb-2 text-sm">
        <span class="font-medium text-slate-700 dark:text-slate-300 truncate max-w-[80%]">{{ currentFileName }}</span>
        <span class="font-bold text-brand">{{ uploadProgress }}%</span>
      </div>
      <div class="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <div class="h-full bg-brand transition-all duration-300 ease-out rounded-full" :style="{ width: uploadProgress + '%' }"></div>
      </div>
    </div>

    <!-- Uploaded Media Grid -->
    <div v-if="postStore.media.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mt-4">
      <div
        v-for="(item, index) in postStore.media"
        :key="index"
        class="group relative aspect-square rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm"
      >
        <img v-if="item.media_type === 'image'" :src="item.localPreview || item.public_url" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" alt="" />
        <div v-else class="w-full h-full flex items-center justify-center bg-slate-800 text-white">
          <Play class="w-10 h-10 opacity-80" />
        </div>
        
        <!-- Overlay & Actions -->
        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button @click.stop="postStore.removeMedia(index)" class="absolute top-2 right-2 w-8 h-8 rounded-lg bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transform transition-transform hover:scale-110 shadow-lg">
            <X class="w-4 h-4" />
          </button>
        </div>
        
        <!-- Type Badge -->
        <div class="absolute bottom-2 left-2 px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider backdrop-blur-md bg-black/50 text-white border border-white/20">
          {{ item.media_type === 'image' ? 'Görsel' : 'Video' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePostStore } from '../stores/post'
import { UploadCloud, Play, X } from 'lucide-vue-next'

const postStore = usePostStore()
const fileInput = ref(null)
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const currentFileName = ref('')

function triggerFileInput() {
  fileInput.value?.click()
}

function handleDrop(event) {
  isDragOver.value = false
  const files = event.dataTransfer?.files
  if (files) processFiles(files)
}

function handleFileSelect(event) {
  const files = event.target?.files
  if (files) processFiles(files)
  event.target.value = ''
}

async function processFiles(files) {
  for (const file of files) {
    await uploadFile(file)
  }
}

async function uploadFile(file) {
  isUploading.value = true
  uploadProgress.value = 0
  currentFileName.value = file.name

  try {
    const confirmData = await postStore.uploadDirect(file, (progress) => {
      uploadProgress.value = progress
    })

    const localPreview = file.type.startsWith('image/') ? URL.createObjectURL(file) : null

    postStore.addMedia({
      public_url: confirmData.public_url,
      object_key: confirmData.object_key,
      media_type: confirmData.media_type,
      localPreview
    })

  } catch (error) {
    console.error('Dosya yükleme hatası:', error)
    alert('Dosya yüklenirken hata oluştu.')
  } finally {
    isUploading.value = false
    uploadProgress.value = 0
  }
}
</script>
