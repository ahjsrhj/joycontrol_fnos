<template>
  <div class="nfc-dialog-overlay" @click.self="handleClose">
    <div class="nfc-dialog">
      <div class="dialog-header">
        <h2>选择 Amiibo 文件</h2>
        <button @click="handleClose" class="close-btn">×</button>
      </div>
      <div class="dialog-content">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="files.length === 0" class="empty">
          <p>未找到 Amiibo 文件</p>
          <p class="hint">请将 .bin 文件放置在 ~/amiibo 目录下</p>
        </div>
        <div v-else class="file-list">
          <div
            v-for="file in files"
            :key="file.path"
            class="file-item"
            :class="{ selected: selectedFile?.path === file.path }"
            @click="selectedFile = file"
          >
            <div class="file-info">
              <div class="file-name">{{ file.name }}</div>
              <div class="file-path">{{ file.relative_path }}</div>
              <div class="file-size">{{ formatSize(file.size) }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="dialog-footer">
        <button @click="handleClose" class="btn btn-secondary">取消</button>
        <button 
          @click="handleConfirm" 
          :disabled="!selectedFile"
          class="btn btn-primary"
        >
          确认
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService, type AmiiboFile } from '../api'

const emit = defineEmits<{
  close: []
  load: [filePath: string]
}>()

const files = ref<AmiiboFile[]>([])
const selectedFile = ref<AmiiboFile | null>(null)
const loading = ref(true)

const formatSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
}

const loadFiles = async () => {
  try {
    loading.value = true
    const response = await apiService.listNFCFiles()
    files.value = response.files
  } catch (error) {
    console.error('Failed to load files:', error)
    alert('加载文件列表失败: ' + (error as Error).message)
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('close')
}

const handleConfirm = () => {
  if (selectedFile.value) {
    emit('load', selectedFile.value.path)
  }
}

onMounted(() => {
  loadFiles()
})
</script>

<style scoped>
.nfc-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.nfc-dialog {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.dialog-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #000;
}

.dialog-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.loading,
.empty {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.hint {
  font-size: 0.875rem;
  color: #999;
  margin-top: 0.5rem;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.file-item:hover {
  border-color: #007bff;
  background: #f0f7ff;
}

.file-item.selected {
  border-color: #007bff;
  background: #e7f3ff;
}

.file-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.file-name {
  font-weight: bold;
  color: #333;
}

.file-path {
  font-size: 0.875rem;
  color: #666;
}

.file-size {
  font-size: 0.75rem;
  color: #999;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
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

.btn-secondary:hover {
  background: #545b62;
}
</style>

