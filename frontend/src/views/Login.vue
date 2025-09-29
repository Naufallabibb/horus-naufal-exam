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
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                </svg>
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
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
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

    <!-- Custom Alert dengan Pure Tailwind -->
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
            <svg v-if="alertType === 'success'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
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
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>