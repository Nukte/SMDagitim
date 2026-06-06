<template>
  <div>
    <div class="modal-backdrop" @click="$emit('close')"></div>

    <div class="modal publish-modal">
      <!-- Header -->
      <div class="modal-header">
        <div class="modal-title-wrap">
          <span class="modal-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z"/></svg>
          </span>
          <h3 class="modal-title">Paylaşım Durumu</h3>
        </div>
        <button class="btn-icon close-btn" @click="$emit('close')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Platform list -->
      <div class="modal-body">
        <div
          v-for="p in postStore.publishJob?.platforms || []"
          :key="p.platform"
          class="platform-row"
          :class="p.status"
        >
          <!-- Status indicator -->
          <div class="row-indicator">
            <span v-if="p.status === 'pending' || p.status === 'publishing'" class="spinner spinner-sm"></span>
            <span v-else-if="p.status === 'success'" class="row-icon success-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            </span>
            <span v-else class="row-icon error-icon">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M18 6L6 18M6 6l12 12"/></svg>
            </span>
          </div>

          <!-- Info -->
          <div class="row-info">
            <span class="row-platform">{{ platformName(p.platform) }}</span>
            <span class="row-status" :class="'s-' + p.status">{{ statusText(p.status) }}</span>
            <span v-if="p.error_message" class="row-error">{{ p.error_message }}</span>
          </div>

          <!-- Link -->
          <a v-if="p.post_url" :href="p.post_url" target="_blank" class="row-link">
            Görüntüle
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </a>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="allDone" class="modal-footer">
        <div class="all-done-msg" v-if="allSuccess">
          <span class="done-dot"></span>
          Tüm paylaşımlar tamamlandı!
        </div>
        <button class="btn btn-primary" @click="$emit('close')">Kapat</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePostStore } from '../stores/post'

const postStore = usePostStore()
defineEmits(['close'])

const allDone = computed(() => {
  const ps = postStore.publishJob?.platforms || []
  return ps.length > 0 && ps.every(p => p.status === 'success' || p.status === 'error')
})

const allSuccess = computed(() =>
  (postStore.publishJob?.platforms || []).every(p => p.status === 'success')
)

const PLATFORM_NAMES = {
  instagram: '📸 Instagram',
  facebook:  '📘 Facebook',
  twitter:   '𝕏  Twitter',
  linkedin:  '💼 LinkedIn',
}
const STATUS_TEXT = {
  pending:    'Bekliyor...',
  publishing: 'Gönderiliyor...',
  success:    'Başarıyla Paylaşıldı',
  error:      'Hata Oluştu',
}

function platformName(id) { return PLATFORM_NAMES[id] || id }
function statusText(s)    { return STATUS_TEXT[s] || s }
</script>

<style scoped>
.publish-modal {
  max-width: 480px;
}

.modal-title-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.modal-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--accent-light);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.close-btn:hover {
  background: var(--bg-input);
  color: var(--text-primary);
}

/* Platform Row */
.platform-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  background: var(--bg-body);
  border: 1px solid var(--border);
  transition: all var(--transition-fast);
}

.platform-row + .platform-row {
  margin-top: var(--space-2);
}

.platform-row.success {
  border-color: var(--success-border);
  background: var(--success-bg);
}

.platform-row.error {
  border-color: var(--error-border);
  background: var(--error-bg);
}

.row-indicator {
  width: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.row-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.success-icon { background: var(--success-bg); color: var(--success); }
.error-icon   { background: var(--error-bg);   color: var(--error); }

.row-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.row-platform {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.row-status {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
}

.s-publishing { color: var(--warning); }
.s-success    { color: var(--success); font-weight: 600; }
.s-error      { color: var(--error);   font-weight: 600; }

.row-error {
  font-size: var(--font-size-xs);
  color: var(--error);
  opacity: 0.8;
}

.row-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: var(--space-1) var(--space-3);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--accent);
  background: var(--accent-light);
  border: 1px solid transparent;
  border-radius: var(--radius-full);
  text-decoration: none;
  white-space: nowrap;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.row-link:hover {
  background: var(--accent);
  color: white;
}

/* Footer */
.all-done-msg {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--success);
  font-weight: 500;
}

.done-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  animation: pulse 2s ease-in-out infinite;
}
</style>
