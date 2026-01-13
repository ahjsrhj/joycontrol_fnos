<template>
  <div class="app">
    <PairingView v-if="!status.connected" ref="pairingView" />
    <ControllerView v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { apiService, type Status } from './api'
import PairingView from './components/PairingView.vue'
import ControllerView from './components/ControllerView.vue'

const status = ref<Status>({
  paired: false,
  connected: false,
  pairing: false,
})

const pairingView = ref<InstanceType<typeof PairingView> | null>(null)

let statusInterval: number | null = null

const updateStatus = async () => {
  try {
    status.value = await apiService.getStatus()
  } catch (error) {
    console.error('Failed to get status:', error)
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
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f5f5f5;
}

.app {
  min-height: 100vh;
}
</style>
