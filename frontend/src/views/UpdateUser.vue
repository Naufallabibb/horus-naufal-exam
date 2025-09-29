<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { usersAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()

const updateForm = ref({
  id: '',
  nama: '',
  email: '',
  username: ''
})

const isLoading = ref(false)
const isUpdateLoading = ref(false)
const userId = ref(null)

onMounted(async () => {
  // Check if user is authenticated
  const token = localStorage.getItem('auth_token')
  if (!token) {
    router.push('/login')
    return
  }

  // Get user ID from route params or use current user
  userId.value = route.params.id || getCurrentUserId()
  
  if (userId.value) {
    await loadUserData(userId.value)
  } else {
    // If no ID provided, pre-fill with demo data or current user data
    loadDemoData()
  }
})

const getCurrentUserId = () => {
  try {
    const userData = localStorage.getItem('user_data')
    if (userData) {
      const user = JSON.parse(userData)
      return user.id
    }
  } catch (error) {
    console.error('Error getting current user ID:', error)
  }
  return null
}

const loadUserData = async (id) => {
  isLoading.value = true
  try {
    const response = await usersAPI.getById(id)
    const userData = response.data.data
    updateForm.value = {
      id: userData.id,
      nama: userData.nama || '',
      email: userData.email || '',
      username: userData.username || ''
    }
    console.log('User data loaded successfully')
  } catch (error) {
    console.error('Error loading user data:', error)
    const errorMessage = error.response?.data?.error || "Failed to load user data"
    console.error(errorMessage)
    
    // If user not found or unauthorized, redirect to dashboard
    if (error.response?.status === 404 || error.response?.status === 401) {
      router.push('/dashboard')
    }
  } finally {
    isLoading.value = false
  }
}

const loadDemoData = () => {
  // Pre-filled data for demo (you can remove this and make it empty)
  updateForm.value = {
    id: '',
    nama: 'Budi Santoso',
    email: 'budi@email.com',
    username: 'budi_s'
  }
}

const handleUpdate = async () => {
  if (!updateForm.value.nama || !updateForm.value.email || !updateForm.value.username) {
    console.error("Please fill all fields")
    return
  }

  isUpdateLoading.value = true
  try {
    let response
    
    if (updateForm.value.id) {
      // Update existing user
      response = await usersAPI.update(updateForm.value.id, {
        username: updateForm.value.username,
        email: updateForm.value.email,
        nama: updateForm.value.nama
      })
    } else {
      // Create new user (if this is meant to be a create form)
      // eslint-disable-next-line no-unused-vars
      response = await usersAPI.create({
        username: updateForm.value.username,
        email: updateForm.value.email,
        nama: updateForm.value.nama,
        password: 'defaultpassword' // You might want to add a password field
      })
    }
    
    console.log("User updated successfully!")
    
    router.push('/dashboard')
  } catch (error) {
    console.error('Error updating user:', error)
    const errorMessage = error.response?.data?.error || "Update failed. Please try again."
    console.error(errorMessage)
  } finally {
    isUpdateLoading.value = false
  }
}

const goBack = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="min-h-screen bg-orange-50 flex items-center justify-center p-6">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg border border-gray-100">
      <!-- Header Section -->
      <div class="px-8 pt-10 pb-8 text-center">
        <div class="mb-6 flex justify-center">
          <img 
            src="@/assets/horus-logo.png" 
            alt="Horus Technology" 
            class="h-12 w-auto"
          >
        </div>
        <h1 class="text-2xl font-semibold text-gray-800 mb-2">
          UPDATE USER
        </h1>
        <p class="text-gray-500 text-sm">
          Perbarui informasi pengguna.
        </p>
      </div>

      <!-- Form Section -->
      <div class="px-8 pb-8">
        <div v-if="isLoading" class="text-center py-8">
          <i class="fas fa-spinner fa-spin text-red-500 text-2xl mb-3"></i>
          <p class="text-gray-500">Loading user data...</p>
        </div>

        <div v-else class="space-y-5">
          <!-- Nama Lengkap Field -->
          <div>
            <label for="nama" class="block text-sm font-medium text-gray-700 mb-2">
              Nama Lengkap
            </label>
            <input
              id="nama"
              v-model="updateForm.nama"
              type="text"
              class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
              placeholder="Masukkan nama lengkap"
              :disabled="isUpdateLoading"
            />
          </div>

          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="updateForm.email"
              type="email"
              class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
              placeholder="contoh@email.com"
              :disabled="isUpdateLoading"
            />
          </div>

          <!-- Username Field -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              id="username"
              v-model="updateForm.username"
              type="text"
              class="w-full h-12 px-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400"
              placeholder="username"
              :disabled="isUpdateLoading"
            />
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-4">
            <button 
              @click="handleUpdate" 
              :disabled="isUpdateLoading"
              class="flex-1 h-12 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 cursor-pointer"
            >
              <span v-if="isUpdateLoading" class="flex items-center justify-center">
                <i class="fas fa-spinner fa-spin mr-3"></i>
                Updating...
              </span>
              <span v-else>Update</span>
            </button>
            <button 
              @click="goBack" 
              :disabled="isUpdateLoading"
              class="flex-1 h-12 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200 disabled:cursor-not-allowed cursor-pointer"
            >
              Kembali
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>