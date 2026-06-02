<template>
  <div class="create-post">

    <!-- Topbar — aynı Dashboard'daki ile -->
    <header class="topbar">
      <div class="container">
        <div class="topbar-inner">
          <div class="topbar-brand">
            <div class="brand-mark">
              <span class="brand-mark-inner"></span>
            </div>
            <span class="brand-name">SMD</span>
          </div>
          <nav class="topbar-nav">
            <router-link to="/" class="nav-pill">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
              </svg>
              Dashboard
            </router-link>
            <router-link to="/create" class="nav-pill active">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              Post Oluştur
            </router-link>
            <router-link to="/settings" class="nav-pill">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              Ayarlar
            </router-link>
          </nav>
          <div class="topbar-right">
            <div class="user-chip">
              <span class="user-avatar">{{ authStore.username?.[0]?.toUpperCase() }}</span>
              <span class="user-name">{{ authStore.username }}</span>
            </div>
            <button class="btn btn-ghost btn-sm" @click="handleLogout">Çıkış</button>
          </div>
        </div>
      </div>
    </header>

    <main class="create-main container">
      <div class="create-layout">

        <!-- ── Sol Panel — Editör ── -->
        <div class="editor-col animate-fade-in-up">
          <div class="col-header" style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
              <p class="section-label">İçerik Oluştur</p>
              <h2 class="col-title">Post Düzenleyici</h2>
            </div>
            <button class="btn btn-primary btn-sm" @click="showAIModal = true" style="padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.9rem;">
              ✨ AI ile Üret
            </button>
          </div>

          <MediaUploader />
          <PostEditor />
          <PlatformSelector />

          <button
            class="btn btn-primary publish-btn"
            :disabled="!canPublish || postStore.isPublishing"
            @click="handlePublish"
          >
            <span v-if="postStore.isPublishing" class="spinner spinner-sm"></span>
            <template v-else>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z"/>
              </svg>
              Paylaş
            </template>
          </button>
        </div>

        <!-- ── Sağ Panel — Önizleme ── -->
        <div class="preview-col animate-fade-in-up delay-200">
          <div class="col-header">
            <p class="section-label">Önizleme</p>
            <h2 class="col-title">Platform Görünümü</h2>
          </div>

          <!-- Tab seçici -->
          <div class="preview-tabs">
            <button
              v-for="tab in previewTabs"
              :key="tab.id"
              class="preview-tab"
              :class="{ active: activePreview === tab.id }"
              :style="{ '--t-color': tab.color }"
              @click="activePreview = tab.id"
            >
              {{ tab.icon }} {{ tab.name }}
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
    </main>

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
  { id: 'twitter',   name: 'X',         icon: '𝕏',  color: '#e7e9ea' },
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
.create-post { min-height: 100vh; }

/* ── Topbar (aynı stil, scoped copy) ── */
.topbar {
  position: sticky; top: 0; z-index: var(--z-sticky);
  background: rgba(6, 6, 10, 0.85);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}
.topbar-inner {
  display: flex; align-items: center;
  gap: var(--space-6); padding: var(--space-4) 0;
}
.topbar-brand { display: flex; align-items: center; gap: var(--space-3); flex-shrink: 0; }
.brand-mark {
  width: 30px; height: 30px; border-radius: 7px;
  background: var(--accent-subtle); border: 1px solid var(--border-accent);
  display: flex; align-items: center; justify-content: center;
}
.brand-mark-inner {
  width: 11px; height: 11px; border-radius: 3px;
  background: var(--accent); box-shadow: 0 0 8px var(--accent-glow); display: block;
}
.brand-name { font-size: var(--font-size-base); font-weight: 700; letter-spacing: -0.01em; }
.topbar-nav { display: flex; gap: var(--space-1); flex: 1; }
.nav-pill {
  display: flex; align-items: center; gap: var(--space-2);
  padding: 6px var(--space-3);
  font-size: var(--font-size-sm); font-weight: 500;
  color: var(--text-tertiary); border-radius: var(--radius-full);
  transition: all var(--transition-fast); text-decoration: none;
}
.nav-pill:hover { color: var(--text-primary); background: var(--bg-input); }
.nav-pill.active { color: var(--accent); background: var(--accent-subtle); }
.topbar-right { display: flex; align-items: center; gap: var(--space-3); margin-left: auto; }
.user-chip {
  display: flex; align-items: center; gap: var(--space-2);
  padding: var(--space-1) var(--space-3) var(--space-1) var(--space-1);
  background: var(--bg-input); border: 1px solid var(--border); border-radius: var(--radius-full);
}
.user-avatar {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--accent-subtle); color: var(--accent);
  font-size: var(--font-size-xs); font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.user-name { font-size: var(--font-size-xs); font-weight: 600; color: var(--text-secondary); }

/* ── Layout ── */
.create-main { padding: var(--space-10) var(--space-6) var(--space-16); }

.create-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  align-items: start;
}

.col-header { margin-bottom: var(--space-6); }
.col-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-top: var(--space-1);
}

/* ── Editor col ── */
.editor-col { display: flex; flex-direction: column; gap: var(--space-4); }

.publish-btn {
  width: 100%;
  padding: var(--space-4);
  font-size: var(--font-size-base);
  border-radius: var(--radius-lg);
  letter-spacing: 0.02em;
  gap: var(--space-2);
}

/* ── Preview col ── */
.preview-col {
  position: sticky;
  top: calc(60px + var(--space-6));
}

.preview-tabs {
  display: flex;
  gap: var(--space-1);
  margin-bottom: var(--space-4);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-2);
  overflow-x: auto;
}

.preview-tab {
  flex: 1;
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-sans);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--text-tertiary);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
  letter-spacing: 0.01em;
}
.preview-tab:hover { color: var(--text-primary); background: var(--bg-input); }
.preview-tab.active {
  color: var(--t-color);
  background: var(--bg-card-hover);
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--t-color) 30%, transparent);
}

.preview-pane { min-height: 400px; }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .create-layout { grid-template-columns: 1fr; }
  .preview-col { position: static; }
}
@media (max-width: 640px) {
  .topbar-nav { display: none; }
  .create-main { padding-inline: var(--space-4); }
}
</style>
