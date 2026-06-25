<template>
  <!-- Login sayfası sidebar olmadan render edilir -->
  <div v-if="isAuthPage" class="min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300 text-slate-900 dark:text-slate-100">
    <router-view />
  </div>

  <!-- Diğer sayfalar sidebar layout ile render edilir -->
  <div v-else class="flex min-h-screen bg-slate-50 dark:bg-slate-950 transition-colors duration-300 text-slate-900 dark:text-slate-100 font-sans">
    
    <!-- Mobile overlay -->
    <transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="sidebarOpen" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40 md:hidden" @click="sidebarOpen = false"></div>
    </transition>

    <!-- Sidebar -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-r border-slate-200/60 dark:border-slate-800/60 transition-transform duration-300 ease-in-out flex flex-col',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      ]"
    >
      <div class="h-16 flex items-center gap-3 px-6 border-b border-slate-200/60 dark:border-slate-800/60">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand to-brand-dark flex items-center justify-center text-white font-display font-bold shadow-lg shadow-brand/20">
          S
        </div>
        <span class="font-display font-semibold text-lg tracking-tight">SMD</span>
      </div>

      <nav class="flex-1 overflow-y-auto p-4 space-y-1 scrollbar-hide">
        <div class="px-3 py-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Ana Menü</div>

        <router-link to="/" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200 transition-colors group" active-class="bg-brand/10 dark:bg-brand/20 !text-brand dark:!text-brand-light font-medium" @click="sidebarOpen = false">
          <LayoutDashboard class="w-5 h-5 opacity-70 group-hover:opacity-100 transition-opacity" />
          <span>Dashboard</span>
        </router-link>

        <router-link to="/create" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200 transition-colors group" active-class="bg-brand/10 dark:bg-brand/20 !text-brand dark:!text-brand-light font-medium" @click="sidebarOpen = false">
          <PenSquare class="w-5 h-5 opacity-70 group-hover:opacity-100 transition-opacity" />
          <span>Gönderi Oluştur</span>
        </router-link>

        <div class="px-3 pt-6 pb-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Sistem</div>

        <router-link to="/settings" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200 transition-colors group" active-class="bg-brand/10 dark:bg-brand/20 !text-brand dark:!text-brand-light font-medium" @click="sidebarOpen = false">
          <Settings class="w-5 h-5 opacity-70 group-hover:opacity-100 transition-opacity" />
          <span>Ayarlar</span>
        </router-link>

        <template v-if="authStore.isSuperuser">
          <div class="px-3 pt-6 pb-2 text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">Admin Paneli</div>
          
          <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200 transition-colors group" active-class="bg-brand/10 dark:bg-brand/20 !text-brand dark:!text-brand-light font-medium" @click="sidebarOpen = false">
            <Users class="w-5 h-5 opacity-70 group-hover:opacity-100 transition-opacity" />
            <span>Kullanıcılar</span>
          </router-link>

          <router-link to="/admin/settings" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200 transition-colors group" active-class="bg-brand/10 dark:bg-brand/20 !text-brand dark:!text-brand-light font-medium" @click="sidebarOpen = false">
            <SlidersHorizontal class="w-5 h-5 opacity-70 group-hover:opacity-100 transition-opacity" />
            <span>Genel Ayarlar</span>
          </router-link>
        </template>
      </nav>

      <div class="p-4 border-t border-slate-200/60 dark:border-slate-800/60">
        <div class="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group">
          <div class="w-9 h-9 rounded-full bg-brand/10 dark:bg-brand/20 text-brand dark:text-brand-light flex items-center justify-center font-bold text-sm shrink-0">
            {{ userInitials }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-semibold truncate text-slate-900 dark:text-slate-100" :title="userFullName">{{ userFullName }}</div>
            <div class="text-xs text-slate-500 dark:text-slate-400">{{ userRole }}</div>
          </div>
          <button @click="handleLogout" class="p-2 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors" title="Çıkış Yap">
            <LogOut class="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile Header -->
    <div class="md:hidden fixed top-0 left-0 right-0 h-16 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-800 z-30 flex items-center justify-between px-4">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand to-brand-dark flex items-center justify-center text-white font-display font-bold shadow-sm">
          S
        </div>
        <span class="font-display font-semibold">SMD</span>
      </div>
      <button @click="sidebarOpen = true" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
        <Menu class="w-6 h-6" />
      </button>
    </div>

    <!-- Main Content Area -->
    <main class="flex-1 min-w-0 md:ml-64 pt-16 md:pt-0">
      <router-view v-slot="{ Component }">
        <transition 
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-4"
          mode="out-in"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <ToastContainer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import ToastContainer from './components/ToastContainer.vue'
import { LayoutDashboard, PenSquare, Settings, Users, SlidersHorizontal, LogOut, Menu } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const sidebarOpen = ref(false)

const isAuthPage = computed(() => ['/login', '/register'].includes(route.path))

const userFullName = computed(() => {
  if (authStore.firstName || authStore.lastName) {
    return `${authStore.firstName} ${authStore.lastName}`.trim()
  }
  return authStore.email ? authStore.email.split('@')[0] : 'Kullanıcı'
})

const userInitials = computed(() => {
  if (authStore.firstName && authStore.lastName) {
    return `${authStore.firstName.charAt(0)}${authStore.lastName.charAt(0)}`.toUpperCase()
  } else if (authStore.firstName) {
    return authStore.firstName.charAt(0).toUpperCase()
  } else if (authStore.email) {
    return authStore.email.charAt(0).toUpperCase()
  }
  return 'U'
})

const userRole = computed(() => {
  return authStore.isSuperuser ? 'Yönetici' : 'Üye'
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Scrollbar hide utility for sidebar */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
