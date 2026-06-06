<template>
  <div class="ai-overlay" v-if="show" @click.self="close">
    <div class="ai-modal">
      <div class="ai-header">
        <div class="ai-header-left">
          <div class="ai-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z"/></svg>
          </div>
          <h3>AI İçerik Üreticisi</h3>
        </div>
        <button class="btn-icon close-btn" @click="close">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>

      <div class="ai-body">
        <div class="input-group">
          <label class="input-label">Konu veya İstek</label>
          <textarea
            v-model="topic"
            rows="3"
            class="input"
            placeholder="Örn: Yeni ürünümüz hakkında heyecan verici bir duyuru..."
            :disabled="aiStore.isLoading"
          ></textarea>
        </div>

        <div class="checkbox-row">
          <label class="checkbox-label">
            <input type="checkbox" v-model="generateImage" :disabled="aiStore.isLoading" />
            <span>AI ile Görsel Üret</span>
          </label>
        </div>

        <div v-if="aiStore.isLoading" class="loader-area">
          <div class="spinner spinner-lg"></div>
          <p>AI içeriği hazırlıyor, lütfen bekleyin...</p>
        </div>

        <div v-if="aiStore.error" class="error-box">
          {{ aiStore.error }}
        </div>
      </div>

      <div class="ai-footer">
        <button class="btn btn-secondary" @click="close" :disabled="aiStore.isLoading">İptal</button>
        <button class="btn btn-primary" @click="generate" :disabled="!topic.trim() || aiStore.isLoading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z"/></svg>
          İçerik Üret
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAiStore } from '../stores/ai'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close', 'generated'])

const aiStore = useAiStore()
const topic = ref('')
const generateImage = ref(true)

const close = () => {
  if (aiStore.isLoading) return
  emit('close')
}

const generate = async () => {
  if (!topic.value.trim()) return

  try {
    const result = await aiStore.generateContent(topic.value, generateImage.value)
    emit('generated', result)
    close()
    topic.value = ''
  } catch (e) {
    // Error is handled in the store
  }
}
</script>

<style scoped>
.ai-overlay {
  position: fixed;
  inset: 0;
  background: var(--bg-overlay);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
}

.ai-modal {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  width: 92%;
  max-width: 500px;
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  animation: modalIn 250ms ease-out;
}

/* Header */
.ai-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--border);
}

.ai-header-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.ai-header h3 {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--text-primary);
}

.ai-icon {
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

/* Body */
.ai-body {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.checkbox-row {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  accent-color: var(--accent);
  width: 16px;
  height: 16px;
}

.loader-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-6) 0;
}

.loader-area p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.error-box {
  padding: var(--space-3) var(--space-4);
  background: var(--error-bg);
  border: 1px solid var(--error-border);
  color: var(--error);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

/* Footer */
.ai-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--border);
}
</style>
