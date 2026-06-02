<template>
  <div class="login-root">
    <!-- Ambient background elements -->
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>
    <div class="grid-overlay"></div>

    <div class="login-wrap">
      <!-- Brand -->
      <div class="brand animate-fade-in-down">
        <div class="brand-mark">
          <span class="brand-mark-inner"></span>
        </div>
        <div class="brand-text">
          <h1 class="brand-name">SMD</h1>
          <span class="brand-tagline">Social Media Distribution</span>
        </div>
      </div>

      <!-- Card -->
      <div class="login-card glass-card animate-fade-in-up">
        <div class="card-top-line"></div>

        <div class="card-inner">
          <div class="card-heading">
            <h2>Giriş Yap</h2>
            <p>Hesabına giriş yap ve yönetmeye başla</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form" novalidate>
            <!-- Username -->
            <div class="input-group">
              <label class="input-label" for="username">Kullanıcı Adı</label>
              <div class="input-wrapper" :class="{ 'has-error': error }">
                <span class="input-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
                  </svg>
                </span>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  class="input"
                  placeholder="kullanici_adi"
                  autocomplete="username"
                  :disabled="loading"
                  @input="error = ''"
                />
              </div>
            </div>

            <!-- Password -->
            <div class="input-group">
              <label class="input-label" for="password">Şifre</label>
              <div class="input-wrapper" :class="{ 'has-error': error }">
                <span class="input-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </span>
                <input
                  id="password"
                  v-model="password"
                  :type="showPass ? 'text' : 'password'"
                  class="input"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  :disabled="loading"
                  @input="error = ''"
                />
                <button
                  type="button"
                  class="pass-toggle"
                  @click="showPass = !showPass"
                  tabindex="-1"
                >
                  <svg v-if="!showPass" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Error -->
            <transition name="err">
              <div v-if="error" class="error-box">
                <span class="error-dot"></span>
                {{ error }}
              </div>
            </transition>

            <!-- Submit -->
            <button
              type="submit"
              class="btn btn-primary btn-submit"
              :disabled="loading || !username || !password"
            >
              <span v-if="loading" class="spinner spinner-sm"></span>
              <span v-else>Giriş Yap</span>
            </button>
          </form>
        </div>
      </div>

      <!-- Footer note -->
      <p class="login-footer animate-fade-in delay-400">
        Sosyal medyanı tek yerden yönet
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router  = useRouter()
const auth    = useAuthStore()

const username = ref('')
const password = ref('')
const showPass = ref(false)
const loading  = ref(false)
const error    = ref('')

async function handleLogin() {
  if (!username.value || !password.value) return
  loading.value = true
  error.value   = ''
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Kullanıcı adı veya şifre hatalı.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ── Root ── */
.login-root {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
  background: var(--bg-primary);
}

/* ── Ambient orbs ── */
.ambient-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
  opacity: 0.12;
}
.orb-1 {
  width: 500px; height: 500px;
  background: var(--accent);
  top: -120px; left: -120px;
  animation: float 8s ease-in-out infinite;
}
.orb-2 {
  width: 360px; height: 360px;
  background: #0066FF;
  bottom: -80px; right: -80px;
  animation: float 10s ease-in-out infinite reverse;
}

/* ── Grid overlay ── */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black 0%, transparent 100%);
  pointer-events: none;
}

/* ── Wrap ── */
.login-wrap {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-8);
  position: relative;
  z-index: 1;
}

/* ── Brand ── */
.brand {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.brand-mark {
  width: 44px; height: 44px;
  border-radius: var(--radius-md);
  background: var(--accent-subtle);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.brand-mark-inner {
  width: 18px; height: 18px;
  border-radius: 4px;
  background: var(--accent);
  box-shadow: 0 0 16px var(--accent-glow);
  display: block;
}

.brand-text { display: flex; flex-direction: column; }
.brand-name {
  font-size: var(--font-size-xl);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}
.brand-tagline {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  letter-spacing: 0.04em;
  font-weight: 500;
}

/* ── Card ── */
.login-card {
  width: 100%;
  padding: 0;
  overflow: hidden;
}

.card-top-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent-dim), transparent);
}

.card-inner {
  padding: var(--space-8) var(--space-8);
}

.card-heading {
  margin-bottom: var(--space-8);
}
.card-heading h2 {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-bottom: var(--space-1);
  line-height: 1.2;
}
.card-heading p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* ── Form ── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper .input {
  padding-left: calc(var(--space-4) + 28px);
}

.input-icon {
  position: absolute;
  left: var(--space-4);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  pointer-events: none;
  transition: color var(--transition-fast);
}

.input-wrapper:focus-within .input-icon {
  color: var(--accent);
}

.input-wrapper.has-error .input {
  border-color: var(--error);
  box-shadow: 0 0 0 3px var(--error-bg);
}

.pass-toggle {
  position: absolute;
  right: var(--space-3);
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  transition: color var(--transition-fast);
}
.pass-toggle:hover { color: var(--text-primary); }

/* ── Error box ── */
.error-box {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--error-bg);
  border: 1px solid rgba(255, 92, 92, 0.2);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--error);
}
.error-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--error);
  flex-shrink: 0;
}

/* ── Submit ── */
.btn-submit {
  width: 100%;
  padding: var(--space-4);
  font-size: var(--font-size-base);
  border-radius: var(--radius-md);
  letter-spacing: 0.02em;
}

/* ── Footer ── */
.login-footer {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  letter-spacing: 0.05em;
  text-align: center;
}

/* ── Error transition ── */
.err-enter-active { transition: all 250ms cubic-bezier(0.34, 1.56, 0.64, 1); }
.err-leave-active { transition: all 150ms ease-in; }
.err-enter-from  { opacity: 0; transform: translateY(-6px); }
.err-leave-to    { opacity: 0; transform: translateY(-4px); }
</style>
