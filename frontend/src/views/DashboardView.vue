<template>
  <div class="page-container">

    <!-- Page Header -->
    <div class="page-header dash-header">
      <div>
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Hesaplarını bağla, içeriklerini çeviri desteğiyle dünyayla paylaş.</p>
      </div>
      <router-link to="/create" class="btn btn-primary btn-lg">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
        Yeni Gönderi
      </router-link>
    </div>

    <!-- Stats -->
    <div class="stats-row animate-fade-in-up">
      <div class="stat-card card">
        <p class="stat-label">Bağlı Hesap</p>
        <p class="stat-value">{{ postStore.connectedAccounts.length }}</p>
      </div>
    </div>

    <!-- Connected Accounts -->
    <section class="section animate-fade-in-up delay-100">
      <h2 class="section-label">Bağlı Hesaplar</h2>

      <div v-if="postStore.connectedAccounts.length === 0" class="empty-state">
        <div class="empty-state-icon">🔗</div>
        <p class="empty-state-title">Henüz hesap bağlanmadı</p>
        <p class="empty-state-text">Aşağıdan sosyal medya hesaplarını bağlayarak başla.</p>
      </div>

      <div class="account-grid">
        <div
          v-for="account in postStore.connectedAccounts"
          :key="account.account_id"
          class="account-card card"
        >
          <!-- Platform accent bar -->
          <div class="account-accent" :style="{ background: getPlatform(account.platform)?.color }"></div>

          <div class="account-body">
            <div class="account-header">
              <div class="account-icon" :style="{ background: getPlatform(account.platform)?.bgColor }">
                <span>{{ getPlatform(account.platform)?.icon }}</span>
              </div>
              <div class="account-info">
                <h3 class="account-name">{{ account.account_name || 'İsimsiz Hesap' }}</h3>
                <p class="account-platform">{{ getPlatform(account.platform)?.name }}</p>
              </div>
              <span class="badge badge-success">
                <span class="status-dot dot-success"></span>
                Bağlı
              </span>
            </div>

            <!-- Account Settings -->
            <div class="account-settings">
              <div class="setting-row">
                <label>Ülke</label>
                <input
                  type="text"
                  v-model="account.country"
                  placeholder="Örn: Türkiye"
                  class="input"
                  @blur="updateAccount(account)"
                />
              </div>
              <div class="setting-row">
                <label>Hedef Çeviri Dili</label>
                <input
                  type="text"
                  v-model="account.target_language"
                  placeholder="Örn: İngilizce"
                  class="input"
                  @blur="updateAccount(account)"
                />
                <span class="input-hint">Dil girilirse paylaşım anında otomatik çeviri yapılır.</span>
              </div>
            </div>

            <div class="account-footer">
              <button class="btn btn-danger btn-sm" @click="disconnectAccount(account.account_id)">
                Bağlantıyı Kes
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Add Account -->
    <section class="section animate-fade-in-up delay-200">
      <h2 class="section-label">Yeni Hesap Ekle</h2>
      <div class="connect-buttons">
        <button
          v-for="p in postStore.platforms"
          :key="p.id"
          class="connect-btn"
          :class="{ disabled: p.id === 'twitter' }"
          :disabled="p.id === 'twitter'"
          @click="connectPlatform(p.id)"
        >
          <span class="connect-icon">{{ p.icon }}</span>
          <span>{{ p.id === 'twitter' ? 'Yakında' : p.name + ' Bağla' }}</span>
        </button>
      </div>
    </section>

  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { usePostStore } from '../stores/post'
import api from '../api/client'

const router    = useRouter()
const route     = useRoute()
const authStore = useAuthStore()
const postStore = usePostStore()

function getPlatform(platformId) {
  return postStore.platforms.find(p => p.id === platformId)
}

async function updateAccount(account) {
  try {
    await api.put(`/api/oauth/account/${account.account_id}`, {
      country: account.country,
      target_language: account.target_language
    })
  } catch (error) {
    console.error('Hesap ayarları güncellenemedi:', error)
  }
}

async function connectPlatform(platformId) {
  if (platformId === 'twitter') return
  const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  window.location.href = `${baseURL}/api/oauth/${platformId}/login`
}

async function disconnectAccount(accountId) {
  if (!confirm(`Bu hesabın bağlantısını kesmek istediğinize emin misiniz?`)) return
  try {
    await api.delete(`/api/oauth/account/${accountId}/disconnect`)
    await postStore.fetchPlatformStatus()
  } catch {
    alert('Bağlantı kesilirken hata oluştu.')
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

onMounted(async () => {
  await postStore.fetchPlatformStatus()
  if (route.query.auth_success) {
    await postStore.fetchPlatformStatus()
    router.replace({ query: {} })
  }
})
</script>

<style scoped>
/* Page Header */
.dash-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
}

/* Stats */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-8);
}

.stat-card {
  padding: var(--space-5) var(--space-6);
}

.stat-label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: var(--space-2);
}

.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.02em;
}

/* Section */
.section {
  margin-bottom: var(--space-8);
}

/* Account Grid */
.account-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
}

.account-card {
  overflow: hidden;
  position: relative;
}

.account-card:hover {
  box-shadow: var(--shadow-md);
}

.account-accent {
  height: 3px;
}

.account-body {
  padding: var(--space-5);
}

.account-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.account-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.account-info {
  flex: 1;
  min-width: 0;
}

.account-name {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-platform {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: 2px;
}

/* Account Settings */
.account-settings {
  padding-top: var(--space-4);
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.setting-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.setting-row label {
  font-size: var(--font-size-xs);
  font-weight: 500;
  color: var(--text-secondary);
}

.setting-row .input {
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-sm);
}

.account-footer {
  padding-top: var(--space-3);
}

.account-footer .btn {
  width: 100%;
  justify-content: center;
}

/* Connect Buttons */
.connect-buttons {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.connect-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-5);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.connect-btn:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--accent-light);
  color: var(--accent);
}

.connect-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.connect-icon {
  font-size: 1.25rem;
}

/* Responsive */
@media (max-width: 768px) {
  .dash-header {
    flex-direction: column;
  }

  .account-grid {
    grid-template-columns: 1fr;
  }
}
</style>
