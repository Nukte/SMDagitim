<template>
  <div class="toast-container">
    <transition-group name="toast-list">
      <div 
        v-for="item in toast.toasts.value" 
        :key="item.id" 
        class="toast-item"
        :class="[`toast-${item.type}`]"
      >
        <div class="toast-icon">
          <svg v-if="item.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          <svg v-else-if="item.type === 'error'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
          <svg v-else-if="item.type === 'warning'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        </div>
        <div class="toast-content">{{ item.message }}</div>
        <button class="toast-close" @click="toast.removeToast(item.id)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { toast } from '../utils/toast'
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  pointer-events: none;
  max-width: 360px;
  width: calc(100vw - var(--space-8));
}

.toast-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  pointer-events: auto;
  position: relative;
  overflow: hidden;
  border-left: 4px solid transparent;
}

.toast-item::after {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.05;
  pointer-events: none;
}

.toast-success { border-left-color: var(--success); }
.toast-success::after { background-color: var(--success); }
.toast-success .toast-icon { color: var(--success); }

.toast-error { border-left-color: var(--error); }
.toast-error::after { background-color: var(--error); }
.toast-error .toast-icon { color: var(--error); }

.toast-warning { border-left-color: var(--warning); }
.toast-warning::after { background-color: var(--warning); }
.toast-warning .toast-icon { color: var(--warning); }

.toast-info { border-left-color: var(--accent); }
.toast-info::after { background-color: var(--accent); }
.toast-info .toast-icon { color: var(--accent); }

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-content {
  flex: 1;
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  line-height: 1.5;
  font-weight: 500;
  padding-top: 1px;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-1);
  margin: -4px -4px -4px 0;
  border-radius: var(--radius-sm);
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-close:hover {
  background: var(--bg-input);
  color: var(--text-primary);
}

/* Animations */
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}

.toast-list-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.toast-list-leave-active {
  position: absolute;
  transition: all 0.3s ease;
}
</style>
