<script setup>
// eslint-disable-next-line no-unused-vars
const props = defineProps({
  users: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['edit', 'delete'])

const handleEdit = (user) => {
  emit('edit', user)
}

const handleDelete = (user) => {
  emit('delete', user)
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
          <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ index + 1 }}</td>
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
  </div>
</template>

<style scoped>
/* Custom orange-25 background for subtle hover effect */
.hover\:bg-orange-25:hover {
  background-color: #fffbf5;
}
</style>