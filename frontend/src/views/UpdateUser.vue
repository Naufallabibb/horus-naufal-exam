<script setup>
import { ref, watch } from 'vue'
import { usersAPI } from '@/services/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  user: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'updated'])

const updateForm = ref({
  id: '',
  nama: '',
  email: '',
  username: ''
})

const isUpdateLoading = ref(false)

// Watch for prop changes to populate form
watch(() => props.user, (newUser) => {
  if (newUser && newUser.id) {
    updateForm.value = {
      id: newUser.id,
      nama: newUser.nama || '',
      email: newUser.email || '',
      username: newUser.username || ''
    }
  }
}, { immediate: true })

// Reset form when modal is closed
watch(() => props.show, (show) => {
  if (!show) {
    resetForm()
  }
})

const resetForm = () => {
  updateForm.value = {
    id: '',
    nama: '',
    email: '',
    username: ''
  }
}

const handleUpdate = async () => {
  if (!updateForm.value.nama || !updateForm.value.email || !updateForm.value.username) {
    emit('updated', { 
      success: false, 
      message: "Mohon lengkapi semua field" 
    })
    return
  }

  isUpdateLoading.value = true
  try {
    const response = await usersAPI.update(updateForm.value.id, {
      username: updateForm.value.username,
      email: updateForm.value.email,
      nama: updateForm.value.nama
    })
    
    emit('updated', { 
      success: true, 
      message: "Data pengguna berhasil diperbarui!",
      data: response.data.data
    })
    
    handleClose()
  } catch (error) {
    console.error('Error updating user:', error)
    const errorMessage = error.response?.data?.error || "Gagal memperbarui data. Silakan coba lagi."
    emit('updated', { 
      success: false, 
      message: errorMessage 
    })
  } finally {
    isUpdateLoading.value = false
  }
}

const handleClose = () => {
  resetForm()
  emit('close')
}
</script>

<template>
  <!-- Edit User Modal -->
  <div 
    v-if="show" 
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click.self="handleClose"
  >
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md transform transition-all">
      <!-- Modal Header -->
      <div class="px-8 pt-8 pb-6 text-center border-b border-gray-100">
        <div class="mb-4 flex justify-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
            <i class="fas fa-user-edit text-red-600 text-xl"></i>
          </div>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">UPDATE USER</h3>
        <p class="text-sm text-gray-500">Halaman untuk mengubah informasi pengguna yang sudah ada.</p>
      </div>

      <!-- Modal Body -->
      <div class="px-8 py-6 space-y-5">
        <!-- Nama Lengkap Field -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Nama Lengkap
          </label>
          <input
            v-model="updateForm.nama"
            type="text"
            class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
            placeholder="Budi Santoso"
            :disabled="isUpdateLoading"
          />
        </div>

        <!-- Email Field -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            v-model="updateForm.email"
            type="email"
            class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
            placeholder="budi@email.com"
            :disabled="isUpdateLoading"
          />
        </div>

        <!-- Username Field -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Username
          </label>
          <input
            v-model="updateForm.username"
            type="text"
            class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
            placeholder="budi_s"
            :disabled="isUpdateLoading"
          />
        </div>
      </div>

      <!-- Modal Footer - Action Buttons -->
      <div class="px-8 py-6 border-t border-gray-100 flex gap-3">
        <button 
          @click="handleUpdate" 
          :disabled="isUpdateLoading"
          class="flex-1 h-12 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 cursor-pointer"
        >
          <span v-if="isUpdateLoading" class="flex items-center justify-center">
            <i class="fas fa-spinner fa-spin mr-2"></i>
            Update...
          </span>
          <span v-else class="flex items-center justify-center">
            <i class="fas fa-save mr-2"></i>
            Update
          </span>
        </button>
        <button 
          @click="handleClose" 
          :disabled="isUpdateLoading"
          class="flex-1 h-12 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200 disabled:cursor-not-allowed cursor-pointer"
        >
          Kembali
        </button>
      </div>
    </div>
  </div>
</template>