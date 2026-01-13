<template>
  <div class="pairing-view">
    <h1>Switch Pro 手柄模拟器</h1>
    <div class="status-card">
      <div v-if="status.paired" class="status-section">
        <p class="status-text">已配对</p>
        <div class="button-group">
          <button 
            @click="handleConnect" 
            :disabled="status.connected || status.pairing"
            class="btn btn-primary"
          >
            {{ status.connected ? '已连接' : '连接' }}
          </button>
          <button 
            @click="handleRepair" 
            :disabled="status.pairing"
            class="btn btn-secondary"
          >
            重新配对
          </button>
        </div>
      </div>
      <div v-else class="status-section">
        <p class="status-text">未配对</p>
        <button 
          @click="handlePair" 
          :disabled="status.pairing"
          class="btn btn-primary"
        >
          {{ status.pairing ? '配对中...' : '开始配对' }}
        </button>
      </div>
      <div v-if="status.pairing" class="pairing-hint">
        <p>请在 Switch 上打开"更改握法/顺序"菜单</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { apiService, type Status } from '../api'

const status = ref<Status>({
  paired: false,
  connected: false,
  pairing: false,
})

let statusInterval: number | null = null

const updateStatus = async () => {
  try {
    status.value = await apiService.getStatus()
  } catch (error) {
    console.error('Failed to get status:', error)
  }
}

const handlePair = async () => {
  try {
    await apiService.pair(false)
    await updateStatus()
  } catch (error) {
    console.error('Failed to pair:', error)
    alert('配对失败: ' + (error as Error).message)
  }
}

const handleConnect = async () => {
  try {
    await apiService.connect()
    await updateStatus()
  } catch (error) {
    console.error('Failed to connect:', error)
    alert('连接失败: ' + (error as Error).message)
  }
}

const handleRepair = async () => {
  try {
    await apiService.pair(true)
    await updateStatus()
  } catch (error) {
    console.error('Failed to repair:', error)
    alert('重新配对失败: ' + (error as Error).message)
  }
}

onMounted(() => {
  updateStatus()
  statusInterval = window.setInterval(updateStatus, 2000)
})

onUnmounted(() => {
  if (statusInterval) {
    clearInterval(statusInterval)
  }
})

defineExpose({
  updateStatus,
})
</script>

<style scoped>
.pairing-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #333;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 300px;
}

.status-section {
  text-align: center;
}

.status-text {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #666;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #545b62;
}

.pairing-hint {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #fff3cd;
  border-radius: 6px;
  color: #856404;
}
</style>

