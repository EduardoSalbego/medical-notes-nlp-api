<template>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <div class="bg-white p-6 rounded-lg shadow-md h-fit">
        <h2 class="text-lg font-semibold mb-4 text-gray-700">Nova Nota Médica</h2>
        <textarea 
          v-model="noteText" 
          class="w-full h-64 p-4 border rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
          placeholder="Digite o relato do paciente aqui..."
        ></textarea>
        
        <div class="mt-4 flex justify-between items-center">
          <span class="text-xs text-gray-400">{{ noteText.length }} caracteres</span>
          <button 
            @click="analyzeNote" 
            :disabled="loading || noteText.length < 10"
            class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50 flex items-center gap-2"
          >
            <span v-if="loading" class="animate-spin">↻</span>
            {{ loading ? 'Processando IA...' : 'Analisar Risco' }}
          </button>
        </div>
      </div>
  
      <div v-if="result" class="bg-white p-6 rounded-lg shadow-md border-t-4" :class="riskColorBorder">
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-lg font-semibold text-gray-700">Resultado da Análise</h2>
          <span class="px-3 py-1 rounded-full text-sm font-bold text-white uppercase" :class="riskColorBg">
            {{ result.risk_classification }}
          </span>
        </div>
  
        <div class="grid grid-cols-2 gap-4 mb-6 text-sm">
          <div class="bg-gray-50 p-3 rounded">
            <span class="text-gray-500 block">Confiança</span>
            <span class="font-mono font-bold text-gray-800">
              {{ (result.confidence_score[result.risk_classification.toLowerCase()] * 100).toFixed(1) }}%
            </span>
          </div>
          <div class="bg-gray-50 p-3 rounded">
            <span class="text-gray-500 block">Tempo Processamento</span>
            <span class="font-mono font-bold text-gray-800">{{ result.processing_time_ms }}ms</span>
          </div>
        </div>
  
        <div class="space-y-4">
          <div v-if="result.entities.symptoms.length">
            <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Sintomas Detectados</h3>
            <div class="flex flex-wrap gap-2">
              <span v-for="s in result.entities.symptoms" :key="s" class="bg-red-100 text-red-700 px-2 py-1 rounded text-sm">
                {{ s }}
              </span>
            </div>
          </div>
          
          <div v-if="result.entities.medications.length">
            <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Medicamentos</h3>
            <div class="flex flex-wrap gap-2">
              <span v-for="m in result.entities.medications" :key="m" class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-sm">
                {{ m }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="mt-6 pt-6 border-t">
          <h3 class="text-xs font-bold text-gray-400 uppercase mb-2">Texto Anonimizado (LGPD/HIPAA)</h3>
          <p class="text-sm text-gray-600 bg-gray-50 p-3 rounded italic">
            "{{ noteText }}" </p>
          <div v-if="result.removed_entities && Object.keys(result.removed_entities).length" class="mt-2 text-xs text-gray-400">
             Proteção aplicada: Nomes, CPFs e Datas ocultados.
          </div>
        </div>
      </div>
      
      <div v-else class="flex items-center justify-center bg-gray-50 rounded-lg border-2 border-dashed border-gray-200 text-gray-400">
        Aguardando análise...
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const noteText = ref('Paciente João Silva, 45 anos, apresenta dor severa no peito e dispneia. Suspeita de infarto.')
  const loading = ref(false)
  const result = ref(null)
  const router = useRouter()
  
  const riskColorBg = computed(() => {
      if (!result.value) return 'bg-gray-500'
      const risk = result.value.risk_classification.toLowerCase()
      if (['high', 'critical'].includes(risk)) return 'bg-red-500'
      if (risk === 'moderate') return 'bg-yellow-500'
      return 'bg-green-500'
  })
  
  const riskColorBorder = computed(() => {
      if (!result.value) return 'border-gray-200'
      const risk = result.value.risk_classification.toLowerCase()
      if (['high', 'critical'].includes(risk)) return 'border-red-500'
      if (risk === 'moderate') return 'border-yellow-500'
      return 'border-green-500'
  })
  
  const analyzeNote = async () => {
      loading.value = true
      try {
          const token = localStorage.getItem('token')
          const response = await axios.post('http://localhost:8085/api/v1/medical-notes/process', {
              medical_note: noteText.value
          }, {
              headers: { Authorization: `Bearer ${token}` }
          })
          
          result.value = response.data.data
      } catch (e) {
          if (e.response && e.response.status === 401) {
              router.push('/login')
          }
          alert('Erro ao processar nota.')
      } finally {
          loading.value = false
      }
  }
  </script>