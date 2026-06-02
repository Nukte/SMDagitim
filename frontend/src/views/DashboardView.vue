<template>
  <div class="dashboard">

    <!-- ── Topbar ── -->
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
            <router-link to="/" class="nav-pill" :class="{ active: $route.path === '/' }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
              </svg>
              Dashboard
            </router-link>
            <router-link to="/create" class="nav-pill" :class="{ active: $route.path === '/create' }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              Post Oluştur
            </router-link>
            <router-link to="/settings" class="nav-pill" :class="{ active: $route.path === '/settings' }">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
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

    <main class="dash-main container">

      <!-- ── Hero ── -->
      <section class="dash-hero animate-fade-in-up">
        <div class="hero-text">
          <p class="section-label">Genel Bakış</p>
          <h2 class="hero-title">
            Merhaba, <span class="text-jade">{{ authStore.username }}</span> 👋
          </h2>
          <p class="hero-sub">Hesaplarını bağla, içeriklerini çeviri desteğiyle dünyayla paylaş.</p>
        </div>
        <router-link to="/create" class="btn btn-primary btn-lg hero-cta">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          Yeni Post
        </router-link>
      </section>

      <!-- ── Stats row ── -->
      <section class="stats-row animate-fade-in-up delay-100">
        <div class="stat-card">
          <p class="stat-label">Bağlı Hesap</p>
          <p class="stat-value text-jade">{{ postStore.connectedAccounts.length }}</p>
        </div>
      </section>

      <!-- ── Platform cards ── -->
      <section class="platforms-section animate-fade-in-up delay-200">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <p class="section-label" style="margin: 0;">Bağlı Hesaplar</p>
        </div>

        <div v-if="postStore.connectedAccounts.length === 0" class="empty-state">
           Henüz hiç hesap bağlamadın. Aşağıdan hesap ekleyebilirsin.
        </div>

        <div class="platform-grid">
          <div
            v-for="account in postStore.connectedAccounts"
            :key="account.account_id"
            class="platform-card card is-connected"
            :style="{ '--p-color': getPlatform(account.platform)?.color }"
          >
            <!-- Top accent line -->
            <div class="p-card-line"></div>

            <div class="p-card-body">
              <div class="p-card-header">
                <div class="p-icon-wrap">
                  <span class="p-icon">{{ getPlatform(account.platform)?.icon }}</span>
                </div>
                <div class="p-info">
                  <h3 class="p-name">{{ getPlatform(account.platform)?.name }}</h3>
                  <p class="p-account">{{ account.account_name || 'İsimsiz Hesap' }}</p>
                </div>
                <span class="p-badge badge-connected">
                  <span class="status-dot dot-success"></span>
                  Bağlı
                </span>
              </div>

              <!-- Hesap Ayarları (Ülke / Dil) -->
              <div class="account-settings">
                <div class="form-group mb-2">
                  <label style="font-size: 0.8rem; color: var(--text-tertiary);">Ülke</label>
                  <input type="text" v-model="account.country" placeholder="Örn: Türkiye" class="form-control" style="padding: 6px 12px; font-size: 0.85rem;" @blur="updateAccount(account)" />
                </div>
                <div class="form-group">
                  <label style="font-size: 0.8rem; color: var(--text-tertiary);">Hedef Çeviri Dili (Opsiyonel)</label>
                  <input type="text" v-model="account.target_language" placeholder="Örn: İngilizce" class="form-control" style="padding: 6px 12px; font-size: 0.85rem;" @blur="updateAccount(account)" />
                  <small style="font-size: 0.7rem; color: var(--text-tertiary); display: block; margin-top: 4px;">Dil girilirse paylaşım anında otomatik çeviri yapılır.</small>
                </div>
              </div>

              <div class="p-card-footer" style="margin-top: 1rem;">
                 <button class="btn btn-danger btn-sm" style="width: 100%; justify-content: center;" @click="disconnectAccount(account.account_id)">
                    Bağlantıyı Kes
                 </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Add Account Section ── -->
      <section class="add-account-section animate-fade-in-up delay-300" style="margin-top: 2rem;">
         <p class="section-label">Yeni Hesap Ekle</p>
         <div class="add-buttons" style="display: flex; gap: 1rem; flex-wrap: wrap;">
           <button 
             v-for="p in postStore.platforms" 
             :key="p.id" 
             class="btn btn-outline"
             :disabled="p.id === 'twitter'"
             @click="connectPlatform(p.id)"
           >
              <span style="font-size: 1.2rem;">{{ p.icon }}</span> 
              {{ p.id === 'twitter' ? 'Yakında' : p.name + ' Bağla' }}
           </button>
         </div>
      </section>

    </main>
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
.dashboard { min-height: 100vh; }

/* ── Topbar ── */
.topbar {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: rgba(6, 6, 10, 0.85);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.topbar-inner {
  display: flex;
  align-items: center;
  gap: var(--space-6);
  padding: var(--space-4) 0;
}

.topbar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}
.brand-mark {
  width: 30px; height: 30px;
  border-radius: 7px;
  background: var(--accent-subtle);
  border: 1px solid var(--border-accent);
  display: flex; align-items: center; justify-content: center;
}
.brand-mark-inner {
  width: 11px; height: 11px;
  border-radius: 3px;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent-glow);
  display: block;
}
.brand-name {
  font-size: var(--font-size-base);
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-primary);
}

.topbar-nav {
  display: flex;
  gap: var(--space-1);
  flex: 1;
}

.nav-pill {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 6px var(--space-3);
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-tertiary);
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
  text-decoration: none;
}
.nav-pill:hover { color: var(--text-primary); background: var(--bg-input); }
.nav-pill.active {
  color: var(--accent);
  background: var(--accent-subtle);
}
.nav-pill.active svg { stroke: var(--accent); }

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-left: auto;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3) var(--space-1) var(--space-1);
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
}
.user-avatar {
  width: 24px; height: 24px;
  border-radius: 50%;
  background: var(--accent-subtle);
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.user-name {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--text-secondary);
}

/* ── Main ── */
.dash-main {
  padding-top: var(--space-12);
  padding-bottom: var(--space-16);
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

/* ── Hero ── */
.dash-hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-6);
}
.hero-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin: var(--space-2) 0 var(--space-3);
}
.hero-sub {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
}

/* ── Stats ── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}
.stat-card {
  padding: var(--space-5) var(--space-6);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
.stat-label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: var(--space-2);
}
.stat-value {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  font-family: var(--font-mono);
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

/* ── Platforms section ── */
.empty-state {
  padding: var(--space-8);
  text-align: center;
  background: var(--bg-card);
  border: 1px dashed var(--border);
  border-radius: var(--radius-lg);
  color: var(--text-tertiary);
}

.platform-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

/* ── Platform Card ── */
.platform-card {
  overflow: hidden;
  transition: all var(--transition-base);
}

.platform-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.platform-card.is-connected {
  border-color: rgba(var(--p-color), 0.2);
}

.p-card-line {
  height: 2px;
  background: var(--p-color);
  opacity: 0;
  transition: opacity var(--transition-base);
}
.platform-card:hover .p-card-line,
.platform-card.is-connected .p-card-line {
  opacity: 0.6;
}

.p-card-body { padding: var(--space-5); }

.p-card-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.p-icon-wrap {
  width: 40px; height: 40px;
  border-radius: var(--radius-md);
  background: var(--bg-input);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.p-info { flex: 1; min-width: 0; }
.p-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  letter-spacing: -0.01em;
}
.p-account {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.p-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: 600;
  flex-shrink: 0;
}
.badge-connected {
  background: var(--success-bg);
  color: var(--success);
}
.badge-disconnected {
  background: var(--bg-input);
  color: var(--text-tertiary);
}
.badge-disconnected .status-dot {
  background: var(--text-tertiary);
}

.account-settings {
  padding-top: var(--space-4);
  border-top: 1px solid var(--border);
}

.mb-2 { margin-bottom: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-5 { margin-top: 2rem; }
.w-100 { width: 100%; }

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-outline:hover {
  background: var(--bg-input);
  border-color: var(--border-accent);
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .dash-hero { flex-direction: column; align-items: flex-start; }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .topbar-nav { display: none; }
  .stats-row  { grid-template-columns: 1fr; }
  .hero-title { font-size: var(--font-size-2xl); }
}
</style>
