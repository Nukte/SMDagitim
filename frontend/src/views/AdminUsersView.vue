<template>
  <div class="max-w-6xl mx-auto p-4 md:p-8 animate-fade-in">
    <div class="mb-8">
      <h1 class="text-3xl font-display font-bold text-slate-900 dark:text-white mb-2 tracking-tight">Kullanıcı Yönetimi</h1>
      <p class="text-slate-500 dark:text-slate-400">Sisteme kayıtlı tüm kullanıcıları ve yöneticileri görüntüleyin.</p>
    </div>

    <div class="card overflow-hidden">
      <div v-if="loading" class="p-8">
        <div class="animate-pulse flex space-x-4">
          <div class="flex-1 space-y-4 py-1">
            <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
            <div class="space-y-2">
              <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded"></div>
              <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-5/6"></div>
              <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-4/6"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="p-12 text-center">
        <div class="w-16 h-16 bg-red-100 dark:bg-red-500/20 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <AlertCircle class="w-8 h-8" />
        </div>
        <h3 class="text-lg font-medium text-slate-900 dark:text-white mb-2">Hata Oluştu</h3>
        <p class="text-slate-500 dark:text-slate-400 mb-6">{{ error }}</p>
        <button class="btn btn-primary" @click="fetchUsers">Tekrar Dene</button>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-left text-sm whitespace-nowrap">
          <thead class="bg-slate-50 dark:bg-slate-900 text-slate-500 dark:text-slate-400 font-medium border-b border-slate-200 dark:border-slate-800">
            <tr>
              <th class="px-6 py-4">ID</th>
              <th class="px-6 py-4">E-posta</th>
              <th class="px-6 py-4">Durum</th>
              <th class="px-6 py-4">Rol</th>
              <th class="px-6 py-4 text-right">İşlemler</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
            <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
              <td class="px-6 py-4 font-medium text-slate-900 dark:text-white">#{{ user.id }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ user.email }}</td>
              <td class="px-6 py-4">
                <span :class="[
                  'px-2.5 py-1 rounded-full text-xs font-medium border',
                  user.is_active 
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20' 
                    : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20'
                ]">
                  {{ user.is_active ? 'Aktif' : 'Pasif' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span :class="[
                  'px-2.5 py-1 rounded-full text-xs font-medium border',
                  user.is_superuser 
                    ? 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-500/10 dark:text-indigo-400 dark:border-indigo-500/20' 
                    : 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700'
                ]">
                  {{ user.is_superuser ? 'Admin' : 'Kullanıcı' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button 
                  v-if="user.email !== authStore.email"
                  class="btn btn-sm"
                  :class="user.is_active ? 'btn-danger' : 'btn-secondary'"
                  @click="toggleActive(user)"
                  :disabled="savingId === user.id"
                >
                  <Loader2 v-if="savingId === user.id" class="w-4 h-4 animate-spin" />
                  <span v-else>{{ user.is_active ? 'Pasife Al' : 'Aktifleştir' }}</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <ConfirmModal 
      ref="confirmModalRef"
      :title="modalState.title"
      :message="modalState.message"
      :type="modalState.type"
      :confirmText="modalState.confirmText"
      :loading="savingId !== null"
      @confirm="executeToggle"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import api from '../api/client'
import { useAuthStore } from '../stores/auth'
import { toast } from '../utils/toast'
import ConfirmModal from '../components/ConfirmModal.vue'
import { AlertCircle, Loader2 } from 'lucide-vue-next'

const users = ref([])
const loading = ref(true)
const error = ref('')
const savingId = ref(null)

const authStore = useAuthStore()

const confirmModalRef = ref(null)
const userToToggle = ref(null)
const modalState = reactive({
  title: '',
  message: '',
  type: 'warning',
  confirmText: 'Onayla'
})

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.get('/api/admin/users')
    users.value = response.data
  } catch (err) {
    error.value = 'Kullanıcılar yüklenirken bir hata oluştu.'
    toast.error('Kullanıcılar yüklenemedi.')
    console.error(err)
  } finally {
    loading.value = false
  }
}

function toggleActive(user) {
  userToToggle.value = user
  if (user.is_active) {
    modalState.title = 'Kullanıcıyı Pasife Al'
    modalState.message = `${user.email} kullanıcısını pasife almak istediğinize emin misiniz? Kullanıcı artık sisteme giriş yapamayacak.`
    modalState.type = 'danger'
    modalState.confirmText = 'Pasife Al'
  } else {
    modalState.title = 'Kullanıcıyı Aktifleştir'
    modalState.message = `${user.email} kullanıcısı tekrar aktif edilecek ve sisteme giriş yapabilecek. Emin misiniz?`
    modalState.type = 'info'
    modalState.confirmText = 'Aktifleştir'
  }
  confirmModalRef.value.open()
}

async function executeToggle() {
  const user = userToToggle.value
  if (!user || savingId.value) return
  savingId.value = user.id
  
  try {
    const response = await api.put(`/api/admin/users/${user.id}`, {
      is_active: !user.is_active
    })
    
    // Listede güncelle
    const index = users.value.findIndex(u => u.id === user.id)
    if (index !== -1) {
      users.value[index] = response.data
    }
    toast.success(user.is_active ? 'Kullanıcı pasife alındı.' : 'Kullanıcı aktifleştirildi.')
    confirmModalRef.value.close()
  } catch (err) {
    toast.error(err.response?.data?.detail || 'İşlem başarısız oldu.')
    console.error(err)
  } finally {
    savingId.value = null
    userToToggle.value = null
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
