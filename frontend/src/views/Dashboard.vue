<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { usersAPI, authAPI } from '@/services/api'
import UserTable from '@/components/UserTable.vue'
import SearchBar from '@/components/SearchBar.vue'
import UpdateUser from '@/views/UpdateUser.vue'

const router = useRouter()

const users = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const totalUsers = ref(0)
const perPage = ref(10)

const editDialog = ref(false)
const deleteDialog = ref(false)
const logoutDialog = ref(false)
const userToDelete = ref(null)
const userToEdit = ref(null)
const isLoading = ref(false)
const isDeleteLoading = ref(false)
const isLogoutLoading = ref(false)
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref('success')

const showAlertMessage = (message, type = 'success') => {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
  
  setTimeout(() => {
    showAlert.value = false
  }, 5000)
}

// Load users data with pagination
const loadUsers = async (page = 1, search = '') => {
  isLoading.value = true
  try {
    const response = await usersAPI.getAll({
      page: page,
      per_page: perPage.value,
      search: search
    })
    
    users.value = response.data.data || []
    totalUsers.value = response.data.total || 0
    currentPage.value = response.data.page || 1
    
    // Calculate total pages
    totalPages.value = Math.ceil(totalUsers.value / perPage.value)
    
    console.log('Users loaded successfully:', {
      total: totalUsers.value,
      page: currentPage.value,
      pages: totalPages.value,
      perPage: perPage.value
    })
  } catch (error) {
    console.error('Error loading users:', error)
    const errorMessage = error.response?.data?.error || "Failed to load users"
    console.error(errorMessage)
    
    // If unauthorized, redirect to login
    if (error.response?.status === 401) {
      logout()
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Check if user is authenticated
  const token = localStorage.getItem('auth_token')
  if (!token) {
    router.push('/login')
    return
  }
  
  loadUsers(1, searchQuery.value)
})

// Watch for search query changes and reload from page 1
watch(searchQuery, (newQuery) => {
  currentPage.value = 1
  loadUsers(1, newQuery)
})

const handleSearch = (query) => {
  searchQuery.value = query
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadUsers(page, searchQuery.value)
  
  // Scroll to top of table
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Handler untuk perubahan jumlah data per halaman
const handlePerPageChange = (newPerPage) => {
  perPage.value = newPerPage
  currentPage.value = 1 // Reset ke halaman pertama
  loadUsers(1, searchQuery.value)
}

const editUser = (user) => {
  userToEdit.value = { ...user }
  editDialog.value = true
}

const handleUpdateResult = (result) => {
  if (result.success) {
    // Reload current page to get updated data
    loadUsers(currentPage.value, searchQuery.value)
    showAlertMessage(result.message, 'success')
  } else {
    showAlertMessage(result.message, 'error')
  }
}

const confirmDelete = (user) => {
  userToDelete.value = user
  deleteDialog.value = true
}

const deleteUser = async () => {
  if (!userToDelete.value) return
  
  isDeleteLoading.value = true
  try {
    await usersAPI.delete(userToDelete.value.id)
    
    deleteDialog.value = false
    userToDelete.value = null
    showAlertMessage("Pengguna berhasil dihapus!", 'success')
    
    // Reload current page after deletion
    // If current page becomes empty and it's not page 1, go to previous page
    if (users.value.length === 1 && currentPage.value > 1) {
      handlePageChange(currentPage.value - 1)
    } else {
      loadUsers(currentPage.value, searchQuery.value)
    }
  } catch (error) {
    console.error('Error deleting user:', error)
    const errorMessage = error.response?.data?.error || "Gagal menghapus pengguna. Silakan coba lagi."
    showAlertMessage(errorMessage, 'error')
  } finally {
    isDeleteLoading.value = false
  }
}

const confirmLogout = () => {
  logoutDialog.value = true
}

const logout = async () => {
  isLogoutLoading.value = true
  
  try {
    await authAPI.logout()
    
    logoutDialog.value = false
    showAlertMessage("Logout berhasil! Mengalihkan...", 'success')
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    console.error('Logout error:', error)
    logoutDialog.value = false
    showAlertMessage("Logout berhasil! Mengalihkan...", 'success')
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  }
}

const closeEditDialog = () => {
  editDialog.value = false
  userToEdit.value = null
}

const closeDeleteDialog = () => {
  deleteDialog.value = false
  userToDelete.value = null
}

const closeLogoutDialog = () => {
  logoutDialog.value = false
}
</script>

<template>
  <!-- Main Content -->
  <div class="min-h-screen bg-orange-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Dashboard Pengguna</h1>
            <p class="text-gray-600">Kelola data pengguna sistem</p>
          </div>
          <button 
            @click="confirmLogout"
            class="inline-flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors duration-200 cursor-pointer"
            title="Logout"
          >
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>
      </div>

      <!-- Search Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 mb-6">
        <SearchBar @search="handleSearch" />
      </div>

      <!-- Users Table Section -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Data Pengguna</h2>
            <div class="text-sm text-gray-500">
              Total: {{ totalUsers }} pengguna
            </div>
          </div>
        </div>
        
        <div v-if="isLoading" class="flex items-center justify-center py-12">
          <div class="text-center">
            <i class="fas fa-spinner fa-spin text-red-500 text-2xl mb-3"></i>
            <p class="text-gray-600">Memuat data pengguna...</p>
          </div>
        </div>
        <UserTable 
          v-else
          :users="users"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-users="totalUsers"
          :per-page="perPage"
          @edit="editUser" 
          @delete="confirmDelete"
          @page-change="handlePageChange"
          @per-page-change="handlePerPageChange"
        />
      </div>
    </div>
  </div>

  <!-- Update User Modal Component -->
  <UpdateUser 
    :show="editDialog"
    :user="userToEdit"
    @close="closeEditDialog"
    @updated="handleUpdateResult"
  />

  <!-- Delete Confirmation Modal -->
  <div 
    v-if="deleteDialog" 
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click.self="closeDeleteDialog"
  >
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md transform transition-all">
      <!-- Modal Header -->
      <div class="px-8 pt-8 pb-6 text-center border-b border-gray-100">
        <div class="mb-4 flex justify-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
            <i class="fas fa-exclamation-triangle text-red-600 text-xl"></i>
          </div>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Konfirmasi Hapus</h3>
        <p class="text-sm text-gray-500">Tindakan ini tidak dapat dibatalkan</p>
      </div>

      <!-- Modal Body -->
      <div class="px-8 py-6">
        <p class="text-gray-600 leading-relaxed text-center">
          Apakah Anda yakin ingin menghapus pengguna 
          <span class="font-semibold text-gray-900">"{{ userToDelete?.nama }}"</span>? 
          Data yang telah dihapus tidak dapat dikembalikan.
        </p>
      </div>

      <!-- Modal Footer -->
      <div class="px-8 py-6 border-t border-gray-100 flex gap-3">
        <button 
          @click="closeDeleteDialog"
          class="flex-1 h-12 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
          :disabled="isDeleteLoading"
        >
          Batal
        </button>
        <button 
          @click="deleteUser" 
          class="flex-1 h-12 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed cursor-pointer"
          :disabled="isDeleteLoading"
        >
          <span v-if="isDeleteLoading" class="flex items-center justify-center">
            <i class="fas fa-spinner fa-spin mr-2"></i>
            Menghapus...
          </span>
          <span v-else class="flex items-center justify-center">
            <i class="fas fa-trash mr-2"></i>
            Hapus
          </span>
        </button>
      </div>
    </div>
  </div>

  <!-- Logout Confirmation Modal -->
  <div 
    v-if="logoutDialog" 
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click.self="closeLogoutDialog"
  >
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md transform transition-all">
      <!-- Modal Header -->
      <div class="px-8 pt-8 pb-6 text-center border-b border-gray-100">
        <div class="mb-4 flex justify-center">
          <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center">
            <i class="fas fa-sign-out-alt text-orange-600 text-xl"></i>
          </div>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Konfirmasi Logout</h3>
        <p class="text-sm text-gray-500">Apakah Anda yakin ingin keluar?</p>
      </div>

      <!-- Modal Body -->
      <div class="px-8 py-6">
        <p class="text-gray-600 leading-relaxed text-center">
          Anda akan keluar dari sistem dan perlu login kembali untuk mengakses dashboard.
        </p>
      </div>

      <!-- Modal Footer -->
      <div class="px-8 py-6 border-t border-gray-100 flex gap-3">
        <button 
          @click="closeLogoutDialog"
          class="flex-1 h-12 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
          :disabled="isLogoutLoading"
        >
          Kembali
        </button>
        <button 
          @click="logout" 
          class="flex-1 h-12 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed cursor-pointer"
          :disabled="isLogoutLoading"
        >
          <span v-if="isLogoutLoading" class="flex items-center justify-center">
            <i class="fas fa-spinner fa-spin mr-2"></i>
            Logging out...
          </span>
          <span v-else class="flex items-center justify-center">
            <i class="fas fa-sign-out-alt mr-2"></i>
            Ya, Logout
          </span>
        </button>
      </div>
    </div>
  </div>

  <!-- Alert Notification -->
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-x-full"
    enter-to-class="opacity-100 translate-x-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 translate-x-0"
    leave-to-class="opacity-0 translate-x-full"
  >
    <div 
      v-if="showAlert"
      class="fixed bottom-6 right-6 z-50 max-w-sm"
    >
      <div 
        :class="[
          'flex items-center p-4 rounded-lg shadow-lg border backdrop-blur-sm',
          alertType === 'success' 
            ? 'bg-green-50/95 border-green-200 text-green-800' 
            : 'bg-red-50/95 border-red-200 text-red-800'
        ]"
      >
        <!-- Icon -->
        <div 
          :class="[
            'flex-shrink-0 w-5 h-5 mr-3',
            alertType === 'success' ? 'text-green-500' : 'text-red-500'
          ]"
        >
          <i v-if="alertType === 'success'" class="fas fa-check-circle text-xl"></i>
          <i v-else class="fas fa-exclamation-triangle text-xl"></i>
        </div>
        
        <!-- Message -->
        <div class="flex-1 text-sm font-medium">
          {{ alertMessage }}
        </div>
        
        <!-- Close Button -->
        <button 
          @click="showAlert = false"
          :class="[
            'flex-shrink-0 ml-4 p-1.5 rounded-md transition-colors duration-150',
            alertType === 'success' 
              ? 'text-green-500 hover:bg-green-100 hover:text-green-600' 
              : 'text-red-500 hover:bg-red-100 hover:text-red-600'
          ]"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </Transition>
</template>