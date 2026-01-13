<template>
  <div class="controller-view">
    <div class="header">
      <h1>Switch Pro 手柄</h1>
      <div class="header-actions">
        <button @click="handleDisconnect" class="btn btn-secondary">断开连接</button>
      </div>
    </div>

    <div class="controller-container">
      <!-- 左摇杆 -->
      <div class="left-stick-area">
        <div 
          class="stick l-stick"
          :class="{ active: leftStickActive }"
          @mousedown="handleStickStart('l', $event)"
          @touchstart="handleStickStart('l', $event)"
        >
          <div class="stick-cap"></div>
        </div>
      </div>

      <!-- 左侧按钮 -->
      <div class="left-buttons">
        <button 
          class="btn-controller dpad-up"
          @mousedown="handleButtonDown('up')"
          @mouseup="handleButtonUp('up')"
          @mouseleave="handleButtonUp('up')"
          @touchstart="handleButtonDown('up')"
          @touchend="handleButtonUp('up')"
        ></button>
        <button 
          class="btn-controller dpad-down"
          @mousedown="handleButtonDown('down')"
          @mouseup="handleButtonUp('down')"
          @mouseleave="handleButtonUp('down')"
          @touchstart="handleButtonDown('down')"
          @touchend="handleButtonUp('down')"
        ></button>
        <button 
          class="btn-controller dpad-left"
          @mousedown="handleButtonDown('left')"
          @mouseup="handleButtonUp('left')"
          @mouseleave="handleButtonUp('left')"
          @touchstart="handleButtonDown('left')"
          @touchend="handleButtonUp('left')"
        ></button>
        <button 
          class="btn-controller dpad-right"
          @mousedown="handleButtonDown('right')"
          @mouseup="handleButtonUp('right')"
          @mouseleave="handleButtonUp('right')"
          @touchstart="handleButtonDown('right')"
          @touchend="handleButtonUp('right')"
        ></button>
      </div>

      <!-- 中间按钮 -->
      <div class="center-buttons">
        <button 
          class="btn-controller btn-minus"
          @mousedown="handleButtonDown('minus')"
          @mouseup="handleButtonUp('minus')"
          @mouseleave="handleButtonUp('minus')"
          @touchstart="handleButtonDown('minus')"
          @touchend="handleButtonUp('minus')"
        >-</button>
        <button 
          class="btn-controller btn-capture"
          @mousedown="handleButtonDown('capture')"
          @mouseup="handleButtonUp('capture')"
          @mouseleave="handleButtonUp('capture')"
          @touchstart="handleButtonDown('capture')"
          @touchend="handleButtonUp('capture')"
        >📷</button>
        <button 
          class="btn-controller btn-home"
          @mousedown="handleButtonDown('home')"
          @mouseup="handleButtonUp('home')"
          @mouseleave="handleButtonUp('home')"
          @touchstart="handleButtonDown('home')"
          @touchend="handleButtonUp('home')"
        >🏠</button>
        <button 
          class="btn-controller btn-plus"
          @mousedown="handleButtonDown('plus')"
          @mouseup="handleButtonUp('plus')"
          @mouseleave="handleButtonUp('plus')"
          @touchstart="handleButtonDown('plus')"
          @touchend="handleButtonUp('plus')"
        >+</button>
      </div>

      <!-- 右侧按钮 -->
      <div class="right-buttons">
        <button 
          class="btn-controller btn-y"
          @mousedown="handleButtonDown('y')"
          @mouseup="handleButtonUp('y')"
          @mouseleave="handleButtonUp('y')"
          @touchstart="handleButtonDown('y')"
          @touchend="handleButtonUp('y')"
        >Y</button>
        <button 
          class="btn-controller btn-x"
          @mousedown="handleButtonDown('x')"
          @mouseup="handleButtonUp('x')"
          @mouseleave="handleButtonUp('x')"
          @touchstart="handleButtonDown('x')"
          @touchend="handleButtonUp('x')"
        >X</button>
        <button 
          class="btn-controller btn-b"
          @mousedown="handleButtonDown('b')"
          @mouseup="handleButtonUp('b')"
          @mouseleave="handleButtonUp('b')"
          @touchstart="handleButtonDown('b')"
          @touchend="handleButtonUp('b')"
        >B</button>
        <button 
          class="btn-controller btn-a"
          @mousedown="handleButtonDown('a')"
          @mouseup="handleButtonUp('a')"
          @mouseleave="handleButtonUp('a')"
          @touchstart="handleButtonDown('a')"
          @touchend="handleButtonUp('a')"
        >A</button>
      </div>

      <!-- 右摇杆 -->
      <div class="right-stick-area">
        <div 
          class="stick r-stick"
          :class="{ active: rightStickActive }"
          @mousedown="handleStickStart('r', $event)"
          @touchstart="handleStickStart('r', $event)"
        >
          <div class="stick-cap"></div>
        </div>
      </div>

      <!-- 肩键 -->
      <div class="shoulder-buttons">
        <button 
          class="btn-controller btn-l"
          @mousedown="handleButtonDown('l')"
          @mouseup="handleButtonUp('l')"
          @mouseleave="handleButtonUp('l')"
          @touchstart="handleButtonDown('l')"
          @touchend="handleButtonUp('l')"
        >L</button>
        <button 
          class="btn-controller btn-zl"
          @mousedown="handleButtonDown('zl')"
          @mouseup="handleButtonUp('zl')"
          @mouseleave="handleButtonUp('zl')"
          @touchstart="handleButtonDown('zl')"
          @touchend="handleButtonUp('zl')"
        >ZL</button>
        <button 
          class="btn-controller btn-r"
          @mousedown="handleButtonDown('r')"
          @mouseup="handleButtonUp('r')"
          @mouseleave="handleButtonUp('r')"
          @touchstart="handleButtonDown('r')"
          @touchend="handleButtonUp('r')"
        >R</button>
        <button 
          class="btn-controller btn-zr"
          @mousedown="handleButtonDown('zr')"
          @mouseup="handleButtonUp('zr')"
          @mouseleave="handleButtonUp('zr')"
          @touchstart="handleButtonDown('zr')"
          @touchend="handleButtonUp('zr')"
        >ZR</button>
      </div>
    </div>

    <!-- NFC 控制 -->
    <div class="nfc-section">
      <button @click="showNFCDialog = true" class="btn btn-primary">NFC / Amiibo</button>
      <div v-if="nfcStatus.loaded" class="nfc-status">
        <span>已加载: {{ nfcStatus.source?.split('/').pop() }}</span>
        <button @click="handleRemoveNFC" class="btn btn-small">移除</button>
      </div>
    </div>

    <!-- NFC 弹窗 -->
    <NFCDialog 
      v-if="showNFCDialog"
      @close="showNFCDialog = false"
      @load="handleLoadNFC"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { apiService, type NFCStatus } from '../api'
import NFCDialog from './NFCDialog.vue'

const showNFCDialog = ref(false)
const nfcStatus = ref<NFCStatus>({ loaded: false })
const leftStickActive = ref(false)
const rightStickActive = ref(false)

const pressedButtons = new Set<string>()

let nfcStatusInterval: number | null = null

const updateNFCStatus = async () => {
  try {
    nfcStatus.value = await apiService.getNFCStatus()
  } catch (error) {
    console.error('Failed to get NFC status:', error)
  }
}

const handleButtonDown = async (button: string) => {
  if (pressedButtons.has(button)) return
  pressedButtons.add(button)
  try {
    await apiService.pressButton([button])
  } catch (error) {
    console.error(`Failed to press button ${button}:`, error)
    pressedButtons.delete(button)
  }
}

const handleButtonUp = async (button: string) => {
  if (!pressedButtons.has(button)) return
  pressedButtons.delete(button)
  try {
    await apiService.releaseButton([button])
  } catch (error) {
    console.error(`Failed to release button ${button}:`, error)
  }
}

const handleStickStart = (stick: 'l' | 'r', event: MouseEvent | TouchEvent) => {
  event.preventDefault()
  const isLeft = stick === 'l'
  if (isLeft) {
    leftStickActive.value = true
  } else {
    rightStickActive.value = true
  }

  const stickElement = event.currentTarget as HTMLElement
  const rect = stickElement.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  const maxRadius = Math.min(rect.width, rect.height) / 2

  const handleMove = (e: MouseEvent | TouchEvent) => {
    e.preventDefault()
    const clientX = 'touches' in e && e.touches.length > 0 ? e.touches[0]!.clientX : (e as MouseEvent).clientX
    const clientY = 'touches' in e && e.touches.length > 0 ? e.touches[0]!.clientY : (e as MouseEvent).clientY
    
    const deltaX = clientX - centerX
    const deltaY = centerY - clientY
    const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY)
    
    // 限制在圆形范围内
    const clampedDistance = Math.min(distance, maxRadius)
    const angle = Math.atan2(deltaY, deltaX)
    const clampedX = Math.cos(angle) * clampedDistance
    const clampedY = Math.sin(angle) * clampedDistance
    
    // 转换为 -32768 到 32767 的范围
    const x = Math.round((clampedX / maxRadius) * 32767)
    const y = Math.round((clampedY / maxRadius) * 32767)
    
    apiService.setStick(stick, x, y).catch(console.error)
  }

  const handleEnd = () => {
    if (isLeft) {
      leftStickActive.value = false
    } else {
      rightStickActive.value = false
    }
    apiService.setStick(stick, 0, 0).catch(console.error)
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  // 初始位置
  handleMove(event)

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove, { passive: false })
  document.addEventListener('touchend', handleEnd)
}

const handleDisconnect = async () => {
  try {
    await apiService.disconnect()
    // 触发父组件更新
    window.location.reload()
  } catch (error) {
    console.error('Failed to disconnect:', error)
  }
}

const handleLoadNFC = async (filePath: string) => {
  try {
    await apiService.loadNFC(filePath)
    await updateNFCStatus()
    showNFCDialog.value = false
  } catch (error) {
    console.error('Failed to load NFC:', error)
    alert('加载 NFC 失败: ' + (error as Error).message)
  }
}

const handleRemoveNFC = async () => {
  try {
    await apiService.removeNFC()
    await updateNFCStatus()
  } catch (error) {
    console.error('Failed to remove NFC:', error)
    alert('移除 NFC 失败: ' + (error as Error).message)
  }
}

onMounted(() => {
  updateNFCStatus()
  nfcStatusInterval = window.setInterval(updateNFCStatus, 2000)
})

onUnmounted(() => {
  if (nfcStatusInterval) {
    clearInterval(nfcStatusInterval)
  }
  // 释放所有按下的按钮
  pressedButtons.forEach(button => {
    apiService.releaseButton([button]).catch(console.error)
  })
})
</script>

<style scoped>
.controller-view {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.controller-container {
  position: relative;
  width: 800px;
  height: 400px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 40px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.left-stick-area,
.right-stick-area {
  position: absolute;
  width: 120px;
  height: 120px;
}

.left-stick-area {
  left: 80px;
  top: 140px;
}

.right-stick-area {
  right: 80px;
  top: 140px;
}

.stick {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
  position: relative;
  cursor: pointer;
  transition: all 0.2s;
}

.stick.active {
  background: rgba(255, 255, 255, 0.4);
}

.stick-cap {
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: white;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.left-buttons {
  position: absolute;
  left: 220px;
  top: 140px;
  display: grid;
  grid-template-columns: repeat(3, 50px);
  grid-template-rows: repeat(3, 50px);
  gap: 5px;
}

.dpad-up {
  grid-column: 2;
  grid-row: 1;
}

.dpad-down {
  grid-column: 2;
  grid-row: 3;
}

.dpad-left {
  grid-column: 1;
  grid-row: 2;
}

.dpad-right {
  grid-column: 3;
  grid-row: 2;
}

.center-buttons {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 10px;
  align-items: center;
}

.right-buttons {
  position: absolute;
  right: 220px;
  top: 140px;
  display: grid;
  grid-template-columns: repeat(2, 60px);
  grid-template-rows: repeat(2, 60px);
  gap: 10px;
}

.btn-y {
  grid-column: 1;
  grid-row: 1;
  background: #ff6b6b;
}

.btn-x {
  grid-column: 2;
  grid-row: 1;
  background: #4ecdc4;
}

.btn-b {
  grid-column: 1;
  grid-row: 2;
  background: #ffe66d;
}

.btn-a {
  grid-column: 2;
  grid-row: 2;
  background: #95e1d3;
}

.shoulder-buttons {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}

.btn-controller {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.1s;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-controller:active {
  transform: scale(0.9);
  background: rgba(255, 255, 255, 0.4);
}

.dpad-up::before {
  content: '▲';
}

.dpad-down::before {
  content: '▼';
}

.dpad-left::before {
  content: '◄';
}

.dpad-right::before {
  content: '►';
}

.nfc-section {
  margin-top: 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.nfc-status {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
}

.btn-small {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}
</style>

