<template>
  <div class="admin-users-view">
    <div class="page-header">
      <h1 class="page-title">Kullanıcı Yönetimi</h1>
      <p class="page-subtitle">Sisteme kayıtlı tüm kullanıcıları ve yöneticileri görüntüleyin.</p>
    </div>

    <div class="card">
      <div v-if="loading" class="loading-state">
        <div class="skeleton-table">
          <div class="skeleton-row header"></div>
          <div class="skeleton-row" v-for="i in 5" :key="i"></div>
        </div>
      </div>

      <div v-else-if="error" class="empty-state">
        <svg class="empty-state-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <h3 class="empty-state-title">Hata Oluştu</h3>
        <p class="empty-state-text">{{ error }}</p>
        <button class="btn btn-primary mt-4" @click="fetchUsers">Tekrar Dene</button>
      </div>

      <div v-else class="table-responsive animate-fade-in-up">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>E-posta</th>
              <th>Durum</th>
              <th>Rol</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>#{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['badge', user.is_active ? 'badge-success' : 'badge-error']">
                  {{ user.is_active ? 'Aktif' : 'Pasif' }}
                </span>
              </td>
              <td>
                <span :class="['badge', user.is_superuser ? 'badge-primary' : 'badge-neutral']">
                  {{ user.is_superuser ? 'Admin' : 'Kullanıcı' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button 
                    v-if="user.email !== authStore.email"
                    class="btn btn-sm"
                    :class="user.is_active ? 'btn-danger' : 'btn-success'"
                    @click="toggleActive(user)"
                    :disabled="savingId === user.id"
                  >
                    {{ user.is_active ? 'Pasife Al' : 'Aktifleştir' }}
                  </button>
                </div>
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

<style scoped>
.admin-users-view {
  padding-bottom: var(--space-8);
}

.table-responsive {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.users-table th,
.users-table td {
  padding: var(--space-4);
  border-bottom: 1px solid var(--border-color);
}

.users-table th {
  font-weight: 500;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
}

.users-table tr {
  transition: background-color var(--transition-fast);
}

.users-table tr:hover {
  background-color: var(--bg-hover);
}

.users-table tr:last-child td {
  border-bottom: none;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-success { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.badge-error { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
.badge-primary { background: rgba(99, 102, 241, 0.1); color: #6366f1; }
.badge-neutral { background: var(--bg-secondary); color: var(--text-secondary); }

.action-buttons {
  display: flex;
  gap: var(--space-2);
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}

.btn-danger {
  background: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.btn-danger:hover {
  background: #ef4444;
  color: white;
}

.btn-success {
  background: transparent;
  color: #10b981;
  border: 1px solid #10b981;
}

.btn-success:hover {
  background: #10b981;
  color: white;
}
</style>
