<template>
  <div class="ai-modal-overlay" v-if="show" @click.self="close">
    <div class="ai-modal">
      <header class="modal-header">
        <h2>✨ AI İçerik Üreticisi</h2>
        <button class="close-btn" @click="close">&times;</button>
      </header>
      
      <div class="modal-body">
        <div class="form-group">
          <label>Konu veya İstek</label>
          <textarea 
            v-model="topic" 
            rows="3" 
            placeholder="Örn: Yeni ürünümüz hakkında heyecan verici bir duyuru..."
            :disabled="aiStore.isLoading"
          ></textarea>
        </div>
        
        <div class="form-group checkbox-group">
          <label>
            <input type="checkbox" v-model="generateImage" :disabled="aiStore.isLoading" />
            AI ile Görsel Üret
          </label>
        </div>

        <div v-if="aiStore.isLoading" class="loader-container">
          <div class="spinner"></div>
          <p>AI içeriği hazırlıyor, lütfen bekleyin...</p>
        </div>

        <div v-if="aiStore.error" class="error-message">
          {{ aiStore.error }}
        </div>
      </div>

      <footer class="modal-footer">
        <button class="btn btn-secondary" @click="close" :disabled="aiStore.isLoading">İptal</button>
        <button class="btn btn-primary" @click="generate" :disabled="!topic.trim() || aiStore.isLoading">
          ✨ İçerik Üret
        </button>
      </footer>
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
.ai-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.ai-modal {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--accent-danger);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(0,0,0,0.2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: inherit;
  resize: vertical;
}

.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 0;
  color: var(--text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--accent-danger);
  color: var(--accent-danger);
  border-radius: 8px;
  font-size: 0.9rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.btn-secondary {
  background: transparent;
  color: var(--text-secondary);
}

.btn-secondary:hover {
  color: var(--text-primary);
}

.btn-primary {
  background: var(--accent-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-secondary);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
