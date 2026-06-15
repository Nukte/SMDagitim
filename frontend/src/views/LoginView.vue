<template>
  <div class="login-root">
    <div class="login-wrap">
      <!-- Brand -->
      <div class="brand animate-fade-in-up">
        <div class="brand-logo">S</div>
        <div class="brand-text">
          <h1 class="brand-name">SMD</h1>
          <span class="brand-tagline">Social Media Distribution</span>
        </div>
      </div>

      <!-- Card -->
      <div class="login-card animate-fade-in-up delay-100">
        <div class="card-inner">
          <div class="card-heading">
            <h2>Giriş Yap</h2>
            <p>Hesabına giriş yap ve yönetmeye başla</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form" novalidate>
            <!-- Email -->
            <div class="input-group">
              <label class="input-label" for="email">E-posta</label>
              <div class="input-wrapper" :class="{ 'has-error': error }">
                <span class="input-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                </span>
                <input
                  id="email"
                  v-model="email"
                  type="email"
                  class="input"
                  placeholder="ornek@sirket.com"
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
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
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
                <button type="button" class="pass-toggle" @click="showPass = !showPass" tabindex="-1">
                  <svg v-if="!showPass" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
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
            <button type="submit" class="btn btn-primary btn-submit" :disabled="loading || !email || !password">
              <span v-if="loading" class="spinner spinner-sm"></span>
              <span v-else>Giriş Yap</span>
            </button>
          </form>
        </div>
      </div>

      <p class="login-footer animate-fade-in delay-300">
        Hesabınız yok mu? <router-link to="/register" class="register-link">Hemen Kayıt Olun</router-link>
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

<style scoped>
.login-root {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  background: var(--bg-body);
  background-image:
    radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.04) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(99, 102, 241, 0.03) 0%, transparent 50%);
}

.login-wrap {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-8);
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.brand-logo {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-lg);
  background: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  font-size: var(--font-size-xl);
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
  letter-spacing: 0.03em;
  font-weight: 500;
}

/* Card */
.login-card {
  width: 100%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.card-inner {
  padding: var(--space-8);
}

.card-heading {
  margin-bottom: var(--space-6);
}

.card-heading h2 {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  letter-spacing: -0.025em;
  margin-bottom: var(--space-1);
  color: var(--text-primary);
}

.card-heading p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* Form */
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
  padding-left: 42px;
}

.input-icon {
  position: absolute;
  left: var(--space-3);
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
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.08);
}

.pass-toggle {
  position: absolute;
  right: var(--space-2);
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

/* Error */
.error-box {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--error-bg);
  border: 1px solid var(--error-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--error);
}

.error-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--error);
  flex-shrink: 0;
}

/* Submit */
.btn-submit {
  width: 100%;
  padding: var(--space-3);
  font-size: var(--font-size-base);
  border-radius: var(--radius-md);
  margin-top: var(--space-2);
}

/* Footer */
.login-footer {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  text-align: center;
}
.register-link {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.register-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

/* Transitions */
.err-enter-active { transition: all 250ms ease-out; }
.err-leave-active { transition: all 150ms ease-in; }
.err-enter-from  { opacity: 0; transform: translateY(-6px); }
.err-leave-to    { opacity: 0; transform: translateY(-4px); }
</style>
