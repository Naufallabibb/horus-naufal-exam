<script setup>
const props = defineProps({
  users: {
    type: Array,
    required: true,
    default: () => []
  },
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  },
  totalUsers: {
    type: Number,
    default: 0
  },
  perPage: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['edit', 'delete', 'page-change', 'per-page-change'])

const handleEdit = (user) => {
  emit('edit', user)
}

const handleDelete = (user) => {
  emit('delete', user)
}

const changePage = (page) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('page-change', page)
  }
}

// Hitung nomor urut yang benar berdasarkan halaman dan perPage
const getRowNumber = (index) => {
  return (props.currentPage - 1) * props.perPage + index + 1
}
</script>

<template>
  <div class="overflow-hidden">
    <table class="w-full">
      <thead>
        <tr class="bg-orange-100 border-b border-orange-100">
          <th class="px-6 py-4 text-left text-sm font-semibold text-gray-800">ID</th>
          <th class="px-6 py-4 text-left text-sm font-semibold text-gray-800">Username</th>
          <th class="px-6 py-4 text-left text-sm font-semibold text-gray-800">Nama Lengkap</th>
          <th class="px-6 py-4 text-left text-sm font-semibold text-gray-800">Email</th>
          <th class="px-6 py-4 text-center text-sm font-semibold text-gray-800">Aksi</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-if="users.length === 0">
          <td colspan="5" class="px-6 py-12 text-center text-gray-500">
            <i class="fas fa-users text-3xl mb-2 block opacity-50 text-gray-400"></i>
            <span class="text-gray-600 font-medium">Tidak ada data pengguna</span>
          </td>
        </tr>
        <tr v-for="(user, index) in users" :key="user.id" class="hover:bg-orange-25 transition-colors duration-200">
          <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ getRowNumber(index) }}</td>
          <td class="px-6 py-4 text-sm text-gray-800">{{ user.username }}</td>
          <td class="px-6 py-4 text-sm text-gray-800">{{ user.nama }}</td>
          <td class="px-6 py-4 text-sm text-gray-800">{{ user.email }}</td>
          <td class="px-6 py-4">
            <div class="flex justify-center gap-2">
              <button 
                @click="handleEdit(user)" 
                class="inline-flex items-center justify-center w-9 h-9 rounded-lg bg-orange-100 hover:bg-orange-200 text-orange-600 hover:text-orange-700 transition-all duration-200 cursor-pointer hover:shadow-sm"
                title="Edit"
              >
                <i class="fas fa-pencil-alt text-sm"></i>
              </button>
              <button 
                @click="handleDelete(user)" 
                class="inline-flex items-center justify-center w-9 h-9 rounded-lg bg-red-100 hover:bg-red-200 text-red-600 hover:text-red-700 transition-all duration-200 cursor-pointer hover:shadow-sm"
                title="Hapus"
              >
                <i class="fas fa-trash text-sm"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination Controls -->
    <div v-if="totalUsers > 0" class="px-6 py-4 border-t border-gray-200 bg-gray-50">
      <div class="flex items-center justify-between">
        <!-- Info Text -->
        <div class="text-sm text-gray-600">
          Menampilkan halaman <span class="font-semibold">{{ currentPage }}</span> dari 
          <span class="font-semibold">{{ totalPages }}</span> 
          (Total: <span class="font-semibold">{{ totalUsers }}</span> pengguna)
        </div>

        <!-- Center: Per Page Selector -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 font-medium">Tampilkan:</label>
          <select
            :value="perPage"
            @change="$emit('per-page-change', parseInt($event.target.value))"
            class="h-9 px-3 pr-8 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent cursor-pointer transition-all duration-200 hover:border-orange-300"
          >
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
          <span class="text-sm text-gray-600">per halaman</span>
        </div>

        <!-- Pagination Buttons -->
        <div class="flex items-center gap-2">
          <!-- First Page Button -->
          <button
            @click="changePage(1)"
            :disabled="currentPage === 1"
            class="inline-flex items-center justify-center w-9 h-9 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-orange-50 hover:border-orange-300 hover:text-orange-600 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white disabled:hover:border-gray-300 disabled:hover:text-gray-600"
            title="Halaman Pertama"
          >
            <i class="fas fa-angle-double-left text-sm"></i>
          </button>

          <!-- Previous Page Button -->
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="inline-flex items-center justify-center w-9 h-9 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-orange-50 hover:border-orange-300 hover:text-orange-600 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white disabled:hover:border-gray-300 disabled:hover:text-gray-600"
            title="Halaman Sebelumnya"
          >
            <i class="fas fa-angle-left text-sm"></i>
          </button>

          <!-- Page Numbers -->
          <div class="flex items-center gap-1">
            <template v-for="page in totalPages" :key="page">
              <!-- Show first page, last page, current page and adjacent pages -->
              <button
                v-if="page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)"
                @click="changePage(page)"
                :class="[
                  'inline-flex items-center justify-center min-w-[36px] h-9 px-3 rounded-lg border transition-all duration-200 cursor-pointer',
                  page === currentPage
                    ? 'bg-orange-500 border-orange-500 text-white font-semibold shadow-sm'
                    : 'border-gray-300 bg-white text-gray-600 hover:bg-orange-50 hover:border-orange-300 hover:text-orange-600'
                ]"
              >
                {{ page }}
              </button>
              <!-- Show ellipsis -->
              <span
                v-else-if="page === currentPage - 2 || page === currentPage + 2"
                class="inline-flex items-center justify-center w-9 h-9 text-gray-400"
              >
                ...
              </span>
            </template>
          </div>

          <!-- Next Page Button -->
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="inline-flex items-center justify-center w-9 h-9 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-orange-50 hover:border-orange-300 hover:text-orange-600 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white disabled:hover:border-gray-300 disabled:hover:text-gray-600"
            title="Halaman Berikutnya"
          >
            <i class="fas fa-angle-right text-sm"></i>
          </button>

          <!-- Last Page Button -->
          <button
            @click="changePage(totalPages)"
            :disabled="currentPage === totalPages"
            class="inline-flex items-center justify-center w-9 h-9 rounded-lg border border-gray-300 bg-white text-gray-600 hover:bg-orange-50 hover:border-orange-300 hover:text-orange-600 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white disabled:hover:border-gray-300 disabled:hover:text-gray-600"
            title="Halaman Terakhir"
          >
            <i class="fas fa-angle-double-right text-sm"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom orange-25 background for subtle hover effect */
.hover\:bg-orange-25:hover {
  background-color: #fffbf5;
}
</style>