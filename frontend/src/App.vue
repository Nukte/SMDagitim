<template>
  <div :data-theme="theme">
    <!-- Theme Toggle -->
    <button class="theme-toggle btn-icon" @click="toggleTheme" :title="theme === 'dark' ? 'Açık Tema' : 'Koyu Tema'">
      <span v-if="theme === 'dark'">☀️</span>
      <span v-else>🌙</span>
    </button>

    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', theme.value)
}

onMounted(() => {
  document.documentElement.setAttribute('data-theme', theme.value)
})
</script>

<style scoped>
.theme-toggle {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  z-index: var(--z-sticky);
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(10px);
  font-size: 1.1rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.theme-toggle:hover {
  background: var(--bg-card-hover);
  transform: scale(1.1);
}
</style>
