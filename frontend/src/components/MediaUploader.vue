<template>
  <div class="media-uploader card">
    <h3 class="uploader-title">📎 Medya</h3>

    <!-- Drop Zone -->
    <div
      class="drop-zone"
      :class="{ 'drop-zone-active': isDragOver, 'drop-zone-has-files': postStore.media.length > 0 }"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <template v-if="postStore.media.length === 0 && !isUploading">
        <div class="drop-zone-content">
          <div class="drop-icon-wrapper">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
          </div>
          <p class="drop-text">Dosyaları sürükle & bırak veya tıkla</p>
          <p class="drop-hint">JPG, PNG, GIF, MP4, MOV • Maks 500MB</p>
        </div>
      </template>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/*,video/*"
      multiple
      hidden
      @change="handleFileSelect"
    />

    <!-- Upload Progress -->
    <div v-if="isUploading" class="upload-progress">
      <div class="upload-file-info">
        <span class="upload-filename">{{ currentFileName }}</span>
        <span class="upload-percent">{{ uploadProgress }}%</span>
      </div>
      <div class="progress-bar">
        <div class="progress-bar-fill" :style="{ width: uploadProgress + '%' }"></div>
      </div>
    </div>

    <!-- Uploaded Media Grid -->
    <div v-if="postStore.media.length > 0" class="media-grid">
      <div
        v-for="(item, index) in postStore.media"
        :key="index"
        class="media-item"
      >
        <div class="media-thumb">
          <img v-if="item.media_type === 'image'" :src="item.localPreview || item.public_url" alt="" />
          <div v-else class="media-video-placeholder">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
          </div>
          <button class="media-remove" @click="postStore.removeMedia(index)" title="Kaldır">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <span class="media-type-badge badge" :class="item.media_type === 'image' ? 'badge-accent' : 'badge-warning'">
          {{ item.media_type === 'image' ? '📷' : '🎬' }} {{ item.media_type }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePostStore } from '../stores/post'

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
  // Input'u sıfırla
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
    // 1. Doğrudan backend üzerinden yükle (Presigned URL sorunlarını atlar)
    const confirmData = await postStore.uploadDirect(file, (progress) => {
      uploadProgress.value = progress
    })

    // 2. Local preview URL oluştur
    const localPreview = file.type.startsWith('image/') ? URL.createObjectURL(file) : null

    // 5. Store'a ekle
    postStore.addMedia({
      public_url: confirmData.public_url,
      object_key: confirmData.object_key,
      media_type: confirmData.media_type,
      localPreview
    })

  } catch (error) {
    console.error('Dosya yükleme hatası:', error)
    alert('Dosya yüklenirken hata oluştu. MinIO çalışıyor mu?')
  } finally {
    isUploading.value = false
    uploadProgress.value = 0
  }
}
</script>

<style scoped>
.media-uploader {
  padding: var(--space-5);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}

.uploader-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
  letter-spacing: -0.01em;
}

/* ── Drop Zone ── */
.drop-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--bg-card);
}

.drop-zone:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.drop-zone-active {
  border-color: var(--accent);
  background: var(--accent-light);
  transform: scale(1.01);
}

.drop-zone-has-files {
  padding: var(--space-4);
  border-style: solid;
  border-color: var(--border);
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
}

.drop-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-2);
}

.drop-text {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.drop-hint {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

/* ── Upload Progress ── */
.upload-progress {
  margin-top: var(--space-4);
}

.upload-file-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.upload-filename {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-percent {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--accent);
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: var(--bg-input);
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
  transition: width var(--transition-base) ease;
}

/* ── Media Grid ── */
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: var(--space-3);
  margin-top: var(--space-4);
}

.media-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.media-thumb {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-input);
  border: 1px solid var(--border);
}

.media-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  background: var(--bg-input);
}

.media-remove {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  color: var(--text-secondary);
  border: 1px solid var(--border);
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-xs);
}

.media-remove:hover {
  background: var(--error);
  color: white;
  border-color: var(--error);
}

.media-thumb:hover .media-remove {
  opacity: 1;
}

.media-type-badge {
  align-self: flex-start;
  font-size: 10px;
}
</style>
