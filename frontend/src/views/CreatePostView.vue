<template>
  <div class="page-container">
    <div class="create-header">
      <div>
        <h1 class="page-title">Gönderi Oluştur</h1>
        <p class="page-subtitle">İçeriğini hazırla, önizle ve paylaş.</p>
      </div>
      <button class="btn btn-secondary" @click="showAIModal = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z"/></svg>
        AI ile Üret
      </button>
    </div>

    <div class="create-layout">
      <!-- Left Column — Editor -->
      <div class="editor-col animate-fade-in-up">
        <MediaUploader />
        <PostEditor />
        <PlatformSelector />

        <button
          class="btn btn-primary btn-lg publish-btn"
          :disabled="!canPublish || postStore.isPublishing"
          @click="handlePublish"
        >
          <span v-if="postStore.isPublishing" class="spinner spinner-sm"></span>
          <template v-else>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z"/></svg>
            Şimdi Paylaş
          </template>
        </button>
      </div>

      <!-- Right Column — Preview -->
      <div class="preview-col animate-fade-in-up delay-200">
        <div class="preview-panel card">
          <div class="preview-header">
            <h3 class="preview-title">Ön İzleme</h3>
          </div>

          <!-- Tab selector -->
          <div class="preview-tabs">
            <button
              v-for="tab in previewTabs"
              :key="tab.id"
              class="preview-tab"
              :class="{ active: activePreview === tab.id }"
              @click="activePreview = tab.id"
            >
              <span class="tab-icon">{{ tab.icon }}</span>
              <span>{{ tab.name }}</span>
            </button>
          </div>

          <div class="preview-pane">
            <InstagramPreview v-if="activePreview === 'instagram'" />
            <FacebookPreview  v-if="activePreview === 'facebook'" />
            <TwitterPreview   v-if="activePreview === 'twitter'" />
            <LinkedInPreview  v-if="activePreview === 'linkedin'" />
          </div>
        </div>
      </div>
    </div>

    <PublishStatusModal v-if="showStatusModal" @close="closeModal" />
    <AIAssistantModal v-if="showAIModal" :show="showAIModal" @close="showAIModal = false" @generated="handleAIGenerated" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { usePostStore } from '../stores/post'
import MediaUploader    from '../components/MediaUploader.vue'
import PostEditor       from '../components/PostEditor.vue'
import PlatformSelector from '../components/PlatformSelector.vue'
import InstagramPreview from '../components/previews/InstagramPreview.vue'
import FacebookPreview  from '../components/previews/FacebookPreview.vue'
import TwitterPreview   from '../components/previews/TwitterPreview.vue'
import LinkedInPreview  from '../components/previews/LinkedInPreview.vue'
import PublishStatusModal from '../components/PublishStatusModal.vue'
import AIAssistantModal from '../components/AIAssistantModal.vue'

const router    = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()

const activePreview  = ref('instagram')
const showStatusModal = ref(false)
const showAIModal = ref(false)

const previewTabs = [
  { id: 'instagram', name: 'Instagram', icon: '📸', color: '#E1306C' },
  { id: 'facebook',  name: 'Facebook',  icon: '📘', color: '#1877F2' },
  { id: 'twitter',   name: 'X',         icon: '𝕏',  color: '#000' },
  { id: 'linkedin',  name: 'LinkedIn',  icon: '💼', color: '#0A66C2' },
]

const canPublish = computed(() =>
  postStore.selectedAccounts.length > 0 &&
  (postStore.content.trim().length > 0 || postStore.media.length > 0)
)

async function handlePublish() {
  showStatusModal.value = true
  try {
    const result = await postStore.publishPost()
    const interval = setInterval(async () => {
      const status = await postStore.pollPublishStatus(result.job_id)
      const done   = status.platforms.every(p => p.status === 'success' || p.status === 'error')
      if (done) { clearInterval(interval); postStore.isPublishing = false }
    }, 1500)
  } catch (e) {
    postStore.isPublishing = false
    alert('Paylaşım başlatılırken hata: ' + (e.response?.data?.detail || e.message))
  }
}

function closeModal() {
  showStatusModal.value = false
  if (!postStore.isPublishing) postStore.resetForm()
}

function handleAIGenerated(result) {
  postStore.content = result.content
  postStore.hashtags = result.hashtags || []
  if (result.media_url) {
    postStore.addMedia({
      public_url: result.media_url,
      object_key: result.media_key || 'ai-generated-' + Date.now(),
      media_type: 'image'
    })
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.create-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.create-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  align-items: start;
}

/* Editor Column */
.editor-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.publish-btn {
  width: 100%;
  padding: var(--space-4);
  font-size: var(--font-size-md);
  border-radius: var(--radius-lg);
  gap: var(--space-2);
  margin-top: var(--space-2);
}

/* Preview Column */
.preview-col {
  position: sticky;
  top: var(--space-8);
}

.preview-panel {
  overflow: hidden;
}

.preview-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--border);
}

.preview-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--text-primary);
}

.preview-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
}

.preview-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3);
  font-family: var(--font-sans);
  font-size: var(--font-size-xs);
  font-weight: 500;
  color: var(--text-tertiary);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.preview-tab:hover {
  color: var(--text-primary);
  background: var(--bg-body);
}

.preview-tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
  background: var(--bg-body);
}

.tab-icon {
  font-size: var(--font-size-sm);
}

.preview-pane {
  padding: var(--space-5);
  min-height: 400px;
  background: var(--bg-body);
}

/* Responsive */
@media (max-width: 1024px) {
  .create-layout {
    grid-template-columns: 1fr;
  }
  .preview-col {
    position: static;
  }
}

@media (max-width: 768px) {
  .create-header {
    flex-direction: column;
  }
}
</style>
