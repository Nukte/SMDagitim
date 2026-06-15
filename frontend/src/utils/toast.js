import { ref } from 'vue'

const toasts = ref([])
let toastIdCounter = 0

export function useToast() {
  const addToast = (message, type = 'info', duration = 3000) => {
    const id = toastIdCounter++
    const toast = { id, message, type }
    toasts.value.push(toast)

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }
  }

  const removeToast = (id) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index !== -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    toasts,
    success: (msg, duration) => addToast(msg, 'success', duration),
    error: (msg, duration) => addToast(msg, 'error', duration),
    info: (msg, duration) => addToast(msg, 'info', duration),
    warning: (msg, duration) => addToast(msg, 'warning', duration),
    removeToast
  }
}

// Global instance for non-component usage
export const toast = useToast()
