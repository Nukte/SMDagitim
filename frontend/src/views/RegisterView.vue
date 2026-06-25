<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden bg-slate-50 dark:bg-slate-950 p-4 py-12">
    <!-- Ambient Background -->
    <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
      <div class="absolute top-[10%] -right-[10%] w-[50%] h-[50%] rounded-full bg-brand/20 dark:bg-brand/10 blur-[120px]"></div>
      <div class="absolute bottom-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-emerald-500/10 dark:bg-emerald-500/5 blur-[100px]"></div>
    </div>

    <div v-if="!loadingSettings" class="w-full max-w-md z-10 flex flex-col items-center gap-8 animate-slide-up">
      <template v-if="!registrationEnabled">
        <div class="w-full glass-panel rounded-3xl p-8 text-center">
          <div class="w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 mx-auto flex items-center justify-center mb-4">
            <Lock class="w-8 h-8" />
          </div>
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2 font-display">Kayıt Kapalı</h2>
          <p class="text-slate-500 dark:text-slate-400 mb-6">Şu anda sisteme yeni üye alımı geçici olarak durdurulmuştur.</p>
          <router-link to="/login" class="btn btn-secondary w-full">Giriş Sayfasına Dön</router-link>
        </div>
      </template>

      <template v-else>
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
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-2 font-display">Hesap Oluştur</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400">Ücretsiz hesabınızı oluşturup paneli kullanmaya başlayın.</p>
          </div>

          <form @submit.prevent="handleRegister" class="space-y-4" novalidate>
            <div class="grid grid-cols-2 gap-4">
              <!-- First Name -->
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300" for="firstName">Ad</label>
                <div class="relative group">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400 group-focus-within:text-brand transition-colors">
                    <User class="w-4 h-4" />
                  </div>
                  <input
                    id="firstName"
                    v-model="firstName"
                    type="text"
                    class="input pl-9"
                    :class="{ 'border-red-500 focus:ring-red-500/20': error }"
                    placeholder="Adınız"
                    autocomplete="given-name"
                    :disabled="loading"
                    @input="error = ''"
                  />
                </div>
              </div>

              <!-- Last Name -->
              <div class="space-y-1.5">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300" for="lastName">Soyad</label>
                <div class="relative group">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400 group-focus-within:text-brand transition-colors">
                    <User class="w-4 h-4" />
                  </div>
                  <input
                    id="lastName"
                    v-model="lastName"
                    type="text"
                    class="input pl-9"
                    :class="{ 'border-red-500 focus:ring-red-500/20': error }"
                    placeholder="Soyadınız"
                    autocomplete="family-name"
                    :disabled="loading"
                    @input="error = ''"
                  />
                </div>
              </div>
            </div>

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
                  autocomplete="new-password"
                  :disabled="loading"
                  @input="error = ''"
                />
                <button type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors focus:outline-none" @click="showPass = !showPass" tabindex="-1">
                  <EyeOff v-if="!showPass" class="w-5 h-5" />
                  <Eye v-else class="w-5 h-5" />
                </button>
              </div>
            </div>

            <!-- Confirm Password -->
            <div class="space-y-1.5">
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300" for="passwordConfirm">Şifre Tekrarı</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 group-focus-within:text-brand transition-colors">
                  <Lock class="w-5 h-5" />
                </div>
                <input
                  id="passwordConfirm"
                  v-model="passwordConfirm"
                  :type="showPass ? 'text' : 'password'"
                  class="input pl-10"
                  :class="{ 'border-red-500 focus:ring-red-500/20': error }"
                  placeholder="••••••••"
                  autocomplete="new-password"
                  :disabled="loading"
                  @input="error = ''"
                />
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
            <button type="submit" class="btn btn-primary w-full mt-4" :disabled="loading || !firstName || !lastName || !email || !password || !passwordConfirm">
              <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
              <span v-else>Kayıt Ol</span>
            </button>
          </form>
        </div>

        <p class="text-sm text-slate-500 dark:text-slate-400 animate-fade-in" style="animation-delay: 300ms;">
          Zaten hesabınız var mı? 
          <router-link to="/login" class="font-medium text-brand hover:text-brand-dark transition-colors">Giriş Yapın</router-link>
        </p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'
import { User, Mail, Lock, Eye, EyeOff, Loader2 } from 'lucide-vue-next'

const router  = useRouter()
const auth    = useAuthStore()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const showPass = ref(false)
const loading  = ref(false)
const error    = ref('')

const registrationEnabled = ref(true)
const loadingSettings = ref(true)

async function checkSettings() {
  try {
    const res = await api.get('/api/auth/public-settings')
    registrationEnabled.value = res.data.registration_enabled
  } catch (err) {
    console.error('Ayarlar alınamadı', err)
  } finally {
    loadingSettings.value = false
  }
}

onMounted(() => {
  checkSettings()
})

async function handleRegister() {
  if (!firstName.value || !lastName.value || !email.value || !password.value) return
  if (password.value !== passwordConfirm.value) {
    error.value = "Şifreler eşleşmiyor."
    return
  }

  loading.value = true
  error.value   = ''
  try {
    await auth.register(firstName.value, lastName.value, email.value, password.value)
    // Kayıt sonrası otomatik login ol
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Kayıt olurken bir hata oluştu.'
  } finally {
    loading.value = false
  }
}
</script>
