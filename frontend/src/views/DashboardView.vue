<template>
  <div class="max-w-6xl mx-auto p-4 md:p-8 animate-fade-in">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
      <div>
        <h1 class="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2 tracking-tight">Dashboard</h1>
        <p class="text-slate-500 dark:text-slate-400">Hesaplarınızı bağlayın, içeriklerinizi dünyayla paylaşın.</p>
      </div>
      <router-link to="/create" class="btn btn-primary shadow-lg shadow-brand/20">
        <PenSquare class="w-5 h-5" />
        Yeni Gönderi
      </router-link>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
      <div class="card p-6 border-l-4 border-l-brand flex flex-col justify-center">
        <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Bağlı Hesap</p>
        <p class="text-4xl font-display font-bold text-slate-900 dark:text-white">{{ postStore.connectedAccounts.length }}</p>
      </div>
    </div>

    <!-- Connected Accounts -->
    <section class="mb-12">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Bağlı Hesaplar</h2>
      </div>

      <div v-if="postStore.connectedAccounts.length === 0" class="glass-panel rounded-2xl p-12 text-center border border-dashed border-slate-300 dark:border-slate-700">
        <div class="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-3xl mx-auto mb-4">🔗</div>
        <h3 class="text-lg font-medium text-slate-900 dark:text-white mb-2">Henüz hesap bağlanmadı</h3>
        <p class="text-slate-500 dark:text-slate-400">Aşağıdan sosyal medya hesaplarınızı bağlayarak başlayabilirsiniz.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="account in postStore.connectedAccounts"
          :key="account.account_id"
          class="card group overflow-hidden"
        >
          <!-- Platform accent bar -->
          <div class="h-1.5 w-full" :style="{ background: getPlatform(account.platform)?.color }"></div>

          <div class="p-6">
            <div class="flex items-start justify-between mb-6">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-sm" :style="{ background: getPlatform(account.platform)?.bgColor }">
                  <span>{{ getPlatform(account.platform)?.icon }}</span>
                </div>
                <div>
                  <h3 class="font-semibold text-slate-900 dark:text-white truncate max-w-[140px]">{{ account.account_name || 'İsimsiz Hesap' }}</h3>
                  <p class="text-xs text-slate-500 mt-1">{{ getPlatform(account.platform)?.name }}</p>
                </div>
              </div>
              <div class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 flex items-center gap-1.5">
                <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse"></div>
                <span class="text-xs font-medium text-emerald-700 dark:text-emerald-400">Bağlı</span>
              </div>
            </div>

            <!-- Account Settings -->
            <div class="pt-5 border-t border-slate-100 dark:border-slate-800 space-y-4 mb-6">
              <div class="space-y-1.5">
                <label class="text-xs font-medium text-slate-500">Ülke</label>
                <input
                  type="text"
                  v-model="account.country"
                  placeholder="Örn: Türkiye"
                  class="input py-2 text-sm"
                  @blur="updateAccount(account)"
                />
              </div>
              <div class="space-y-1.5">
                <label class="text-xs font-medium text-slate-500">Hedef Çeviri Dili</label>
                <input
                  type="text"
                  v-model="account.target_language"
                  placeholder="Örn: İngilizce"
                  class="input py-2 text-sm"
                  @blur="updateAccount(account)"
                />
                <p class="text-[11px] text-slate-400">Dil girilirse paylaşım anında otomatik çeviri yapılır.</p>
              </div>
            </div>

            <button class="btn btn-danger w-full py-2.5 text-sm" @click="disconnectAccount(account.account_id)">
              <Unlink class="w-4 h-4" />
              Bağlantıyı Kes
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Add Account -->
    <section>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">Yeni Hesap Ekle</h2>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          v-for="p in postStore.platforms"
          :key="p.id"
          class="card flex flex-col items-center justify-center p-6 gap-3 hover:border-brand hover:bg-brand/5 dark:hover:bg-brand/10 transition-all duration-300 group"
          :class="{ 'opacity-50 grayscale cursor-not-allowed hover:border-slate-200 hover:bg-white dark:hover:bg-slate-900': p.id === 'twitter' }"
          :disabled="p.id === 'twitter'"
          @click="connectPlatform(p.id)"
        >
          <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl transition-transform group-hover:scale-110 group-active:scale-95" :style="{ background: getPlatform(p.id)?.bgColor }">
            {{ p.icon }}
          </div>
          <span class="font-medium text-sm text-slate-700 dark:text-slate-300">
            {{ p.id === 'twitter' ? 'Yakında' : p.name + ' Bağla' }}
          </span>
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
import { PenSquare, Unlink } from 'lucide-vue-next'

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
  try {
    const response = await api.get(`/api/oauth/${platformId}/login`)
    window.location.href = response.data.url
  } catch (error) {
    console.error('Bağlantı hatası:', error)
    alert('Platform bağlantısı başlatılamadı.')
  }
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

onMounted(async () => {
  await postStore.fetchPlatformStatus()
  if (route.query.auth_success) {
    await postStore.fetchPlatformStatus()
    router.replace({ query: {} })
  }
})
</script>
