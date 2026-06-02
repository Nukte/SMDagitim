<template>
  <div class="platform-selector card">
    <h3 class="selector-title">📱 Hesaplar</h3>

    <div v-if="postStore.connectedAccounts.length === 0" style="font-size: 0.8rem; color: var(--text-tertiary);">
      Hesap bulunamadı. Lütfen önce dashboard'dan hesap bağlayın.
    </div>

    <div class="platform-list">
      <label
        v-for="account in postStore.connectedAccounts"
        :key="account.account_id"
        class="platform-option"
        :class="{
          'option-selected': postStore.selectedAccounts.includes(account.account_id)
        }"
        :style="{ '--p-color': getPlatform(account.platform)?.color }"
      >
        <input
          type="checkbox"
          :value="account.account_id"
          v-model="postStore.selectedAccounts"
          hidden
        />
        <div class="option-check">
          <span v-if="postStore.selectedAccounts.includes(account.account_id)">✓</span>
        </div>
        <span class="option-icon">{{ getPlatform(account.platform)?.icon }}</span>
        <span class="option-name">
           {{ getPlatform(account.platform)?.name }}
           <small style="display:block; font-size: 0.7rem; color: var(--text-tertiary); font-weight: normal;">
             {{ account.account_name || 'İsimsiz' }}
             <span v-if="account.target_language">({{ account.target_language }})</span>
           </small>
        </span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { usePostStore } from '../stores/post'

const postStore = usePostStore()

function getPlatform(platformId) {
  return postStore.platforms.find(p => p.id === platformId)
}
</script>

<style scoped>
.platform-selector {
  padding: var(--space-5);
}

.selector-title {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.platform-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.platform-option {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.platform-option:hover {
  border-color: var(--border-hover);
  background: var(--bg-card-hover);
}

.option-selected {
  border-color: var(--p-color) !important;
  background: var(--bg-card-hover);
}

.option-check {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.option-selected .option-check {
  background: var(--p-color);
  border-color: var(--p-color);
  color: white;
}

.option-icon {
  font-size: 1.1rem;
}

.option-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  flex: 1;
}
</style>
