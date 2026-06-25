<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden bg-slate-50 dark:bg-slate-950 p-4">
    <!-- Ambient Background -->
    <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-brand/20 dark:bg-brand/10 blur-[120px]"></div>
      <div class="absolute top-[60%] -right-[10%] w-[40%] h-[40%] rounded-full bg-purple-500/10 dark:bg-purple-500/5 blur-[100px]"></div>
    </div>

    <div class="w-full max-w-md z-10 flex flex-col items-center gap-8 animate-slide-up">
      <!-- Brand -->
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-brand to-brand-dark flex items-center justify-center text-white font-display font-bold text-2xl shadow-lg shadow-brand/25">
          S
        </div>
        <div class="flex flex-col">
          <h1 class="font-display font-bold text-2xl leading-none text-slate-900 dark:text-white tracking-tight">SMD</h1>
          <span class="text-xs font-medium text-slate-500 tracking-wide uppercase mt-1">Social Media Distribution</span>
        </div>
      </div>

      <!-- Card -->
      <div class="w-full glass-panel rounded-3xl p-8">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2 font-display">Tekrar Hoş Geldiniz</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400">Hesabınıza giriş yapın ve yönetmeye başlayın.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5" novalidate>
          <!-- Email -->
          <div class="space-y-1.5">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300" for="email">E-posta</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 group-focus-within:text-brand transition-colors">
                <Mail class="w-5 h-5" />
              </div>
              <input
                id="email"
                v-model="email"
                type="email"
                class="input pl-10"
                :class="{ 'border-red-500 focus:ring-red-500/20': error }"
                placeholder="ornek@sirket.com"
                autocomplete="username"
                :disabled="loading"
                @input="error = ''"
              />
            </div>
          </div>

          <!-- Password -->
          <div class="space-y-1.5">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300" for="password">Şifre</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 group-focus-within:text-brand transition-colors">
                <Lock class="w-5 h-5" />
              </div>
              <input
                id="password"
                v-model="password"
                :type="showPass ? 'text' : 'password'"
                class="input pl-10 pr-10"
                :class="{ 'border-red-500 focus:ring-red-500/20': error }"
                placeholder="••••••••"
                autocomplete="current-password"
                :disabled="loading"
                @input="error = ''"
              />
              <button type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors focus:outline-none" @click="showPass = !showPass" tabindex="-1">
                <EyeOff v-if="!showPass" class="w-5 h-5" />
                <Eye v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Error -->
          <transition 
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="opacity-0 -translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <div v-if="error" class="flex items-center gap-2 p-3 rounded-xl bg-red-50 dark:bg-red-500/10 border border-red-100 dark:border-red-500/20 text-sm text-red-600 dark:text-red-400">
              <div class="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0"></div>
              {{ error }}
            </div>
          </transition>

          <!-- Submit -->
          <button type="submit" class="btn btn-primary w-full mt-2" :disabled="loading || !email || !password">
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <span v-else>Giriş Yap</span>
          </button>
        </form>
      </div>

      <p class="text-sm text-slate-500 dark:text-slate-400 animate-fade-in" style="animation-delay: 300ms;">
        Hesabınız yok mu? 
        <router-link to="/register" class="font-medium text-brand hover:text-brand-dark transition-colors">Hemen Kayıt Olun</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Mail, Lock, Eye, EyeOff, Loader2 } from 'lucide-vue-next'

const router  = useRouter()
const auth    = useAuthStore()

const email = ref('')
const password = ref('')
const showPass = ref(false)
const loading  = ref(false)
const error    = ref('')

async function handleLogin() {
  if (!email.value || !password.value) return
  loading.value = true
  error.value   = ''
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Kullanıcı adı veya şifre hatalı.'
  } finally {
    loading.value = false
  }
}
</script>
