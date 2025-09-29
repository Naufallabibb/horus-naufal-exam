<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])

const searchQuery = ref('')

const handleSearch = () => {
  emit('search', searchQuery.value.trim())
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('search', '')
}

const onKeyup = (event) => {
  if (event.key === 'Enter') {
    handleSearch()
  }
}
</script>

<template>
  <div class="flex items-center gap-3">
    <div class="relative flex-1 max-w-md">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <i class="fas fa-search text-gray-400"></i>
      </div>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari pengguna..."
        class="w-full h-12 pl-10 pr-4 text-gray-900 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent placeholder-gray-400 transition-all duration-200"
        @keyup="onKeyup"
      />
    </div>
    <button 
      v-if="searchQuery"
      @click="clearSearch" 
      class="inline-flex items-center justify-center h-12 px-4 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
      title="Clear"
    >
      <i class="fas fa-times mr-2"></i>
      Clear
    </button>
  </div>
</template>