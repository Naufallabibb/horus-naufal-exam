import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const token = ref(null)

  const login = (userData, authToken) => {
    user.value = userData
    token.value = authToken
    isAuthenticated.value = true
    
    // Store in localStorage for persistence
    localStorage.setItem('auth_token', authToken)
    localStorage.setItem('user_data', JSON.stringify(userData))
  }

  const logout = () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    
    // Remove from localStorage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  }

  const checkAuth = () => {
    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('user_data')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
      isAuthenticated.value = true
      return true
    }
    
    return false
  }

  return {
    user,
    isAuthenticated,
    token,
    login,
    logout,
    checkAuth
  }
})