<template>
    <div class="min-h-screen">
      <nav v-if="$route.name !== 'Login'" class="bg-blue-600 text-white p-4 shadow-md">
        <div class="container mx-auto flex justify-between items-center">
          <h1 class="text-xl font-bold flex items-center gap-2">
            Medical AI Gateway
          </h1>
          <button @click="logout" class="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded text-sm">
            Sair
          </button>
        </div>
      </nav>
      <main class="container mx-auto p-4">
        <router-view></router-view>
      </main>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const logout = () => {
      localStorage.removeItem('token')
      router.push('/login')
  }
  </script>