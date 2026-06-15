<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click="cancel">
      <div class="modal-content" @click.stop>
        <div class="modal-icon" :class="`icon-${type}`">
          <!-- Warning Icon -->
          <svg v-if="type === 'warning'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <!-- Danger Icon -->
          <svg v-else-if="type === 'danger'" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
          <!-- Info Icon -->
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        </div>
        
        <h3 class="modal-title">{{ title }}</h3>
        <p class="modal-message">{{ message }}</p>
        
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancel">{{ cancelText }}</button>
          <button class="btn" :class="`btn-${type === 'warning' ? 'primary' : type}`" @click="confirm">
            <span v-if="loading" class="spinner spinner-sm"></span>
            <span v-else>{{ confirmText }}</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Emin misiniz?' },
  message: { type: String, default: 'Bu işlemi onaylıyor musunuz?' },
  confirmText: { type: String, default: 'Onayla' },
  cancelText: { type: String, default: 'İptal' },
  type: { type: String, default: 'warning' }, // warning, danger, info
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['confirm', 'cancel'])

const isOpen = ref(false)

const open = () => {
  isOpen.value = true
}

const close = () => {
  isOpen.value = false
}

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
  close()
}

defineExpose({ open, close })
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
}

.modal-content {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  width: 100%;
  max-width: 400px;
  padding: var(--space-6);
  text-align: center;
  border: 1px solid var(--border);
}

.modal-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-4);
}

.icon-warning { background: var(--warning-bg); color: var(--warning); }
.icon-danger { background: var(--error-bg); color: var(--error); }
.icon-info { background: var(--accent-bg); color: var(--accent); }

.modal-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.modal-message {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: var(--space-6);
}

.modal-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
}

.modal-actions .btn {
  flex: 1;
}

/* Animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content {
  transform: scale(0.95) translateY(10px);
}

.modal-fade-leave-to .modal-content {
  transform: scale(0.95) translateY(10px);
}
</style>
