<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/services/api'

const router = useRouter()

const loginForm = ref({
  username: '',
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref('success') // 'success' or 'error'

// Field validation states
const fieldErrors = ref({
  username: false,
  password: false
})

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const validateField = (fieldName) => {
  fieldErrors.value[fieldName] = !loginForm.value[fieldName]
}

const validateAllFields = () => {
  Object.keys(loginForm.value).forEach(field => {
    fieldErrors.value[field] = !loginForm.value[field]
  })
  return !Object.values(fieldErrors.value).some(error => error)
}

const showAlertMessage = (message, type = 'success') => {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
  
  // Auto hide alert after 8 seconds (longer duration)
  setTimeout(() => {
    showAlert.value = false
  }, 8000)
}

const handleLogin = async () => {
  // Validate all fields first
  if (!validateAllFields()) {
    showAlertMessage('Mohon lengkapi username dan password', 'error')
    return
  }

  isLoading.value = true
  
  try {
    const response = await authAPI.login({
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    // Store auth token and user data
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token)
      localStorage.setItem('user_data', JSON.stringify(response.data.user))
    }
    
    console.log("Login successful!")
    
    // Show success alert with message from API
    showAlertMessage(response.data.message || 'Login berhasil', 'success')
    
    // Redirect to dashboard after 2 seconds
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)
    
  } catch (error) {
    console.error('Login error:', error)
    
    // SECURITY: Always show same generic message for any login failure
    // This prevents user enumeration attacks and SQL injection attempts
    // Never reveal whether username exists or password is wrong
    let errorMessage = "Username atau password salah"
    
    // Only handle server errors differently
    if (error.response?.status === 500 || error.code === 'NETWORK_ERROR') {
      errorMessage = "Terjadi kesalahan server. Silakan coba lagi"
    }
    
    showAlertMessage(errorMessage, 'error')
  } finally {
    isLoading.value = false
  }
}

const goToRegister = () => {
  router.push('/register')
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
          LOGIN
        </h1>
        <p class="text-gray-500 text-sm">
          Silahkan masuk dengan akun Anda.
        </p>
      </div>

      <!-- Form Section -->
      <div class="px-8 pb-8">
        <div class="space-y-5">
          <!-- Username Field -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Username <span class="text-red-500">*</span>
            </label>
            <input
              id="username"
              v-model="loginForm.username"
              type="text"
              :class="[
                'w-full h-12 px-4 text-gray-900 bg-white border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400',
                fieldErrors.username ? 'border-red-500' : 'border-gray-300'
              ]"
              placeholder="Masukkan username Anda"
              :disabled="isLoading"
              @blur="validateField('username')"
              @input="fieldErrors.username = false"
              @keyup.enter="handleLogin"
            />
            <p class="text-xs text-gray-500 mt-1">
              Masukkan username yang terdaftar
            </p>
            <p v-if="fieldErrors.username" class="text-xs text-red-500 mt-1">
              Username wajib diisi
            </p>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                :class="[
                  'w-full h-12 px-4 pr-12 text-gray-900 bg-white border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200 disabled:bg-gray-50 disabled:text-gray-400',
                  fieldErrors.password ? 'border-red-500' : 'border-gray-300'
                ]"
                placeholder="Masukkan password Anda"
                :disabled="isLoading"
                @blur="validateField('password')"
                @input="fieldErrors.password = false"
                @keyup.enter="handleLogin"
              />
              <button
                type="button"
                @click="togglePasswordVisibility"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                :disabled="isLoading"
              >
                <i v-if="!showPassword" class="fas fa-eye text-lg"></i>
                <i v-else class="fas fa-eye-slash text-lg"></i>
              </button>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              Masukkan password akun Anda
            </p>
            <p v-if="fieldErrors.password" class="text-xs text-red-500 mt-1">
              Password wajib diisi
            </p>
          </div>
        </div>

        <!-- Login Button -->
        <button
          @click="handleLogin"
          :disabled="isLoading"
          class="w-full h-12 mt-6 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 cursor-pointer"
        >
          <span v-if="isLoading" class="flex items-center justify-center">
            <i class="fas fa-spinner fa-spin mr-3"></i>
            Processing...
          </span>
          <span v-else>Login</span>
        </button>

        <!-- Footer Links -->
        <div class="text-center mt-6">
          <p class="text-sm text-gray-600">
            Belum punya akun? 
            <button 
              @click="goToRegister" 
              class="text-red-500 font-medium hover:text-red-600 transition-colors duration-200 disabled:text-gray-400 cursor-pointer"
              :disabled="isLoading"
            >
              Registrasi di sini
            </button>
          </p>
        </div>
      </div>
    </div>

    <!-- Custom Alert dengan Font Awesome -->
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
  </div>
</template>