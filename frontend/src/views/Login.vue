<template>
    <div class="flex items-center justify-center min-h-[80vh]">
      <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-gray-100">
        <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Acesso Médico</h2>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="email" type="email" class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none" required>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
            <input v-model="password" type="password" class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 outline-none" required>
          </div>
  
          <button :disabled="loading" type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50">
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
          
          <p v-if="error" class="text-red-500 text-sm text-center mt-2">{{ error }}</p>
        </form>
        
        <div class="mt-4 text-center text-xs text-gray-400">
          <p>Credenciais de Teste:</p>
          <p>doctor@medical-notes.local / password</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const email = ref('doctor@medical-notes.local')
  const password = ref('password')
  const loading = ref(false)
  const error = ref('')
  const router = useRouter()
  
  const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      try {
          const response = await axios.post('http://localhost:8085/api/v1/login', {
              email: email.value,
              password: password.value
          })
          
          localStorage.setItem('token', response.data.token)
          router.push('/')
      } catch (e) {
          error.value = 'Falha no login. Verifique suas credenciais.' + (e.response?.data?.message || '')
      } finally {
          loading.value = false
      }
  }
  </script>