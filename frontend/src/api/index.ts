import axios from 'axios'

const api = axios.create({
  baseURL: import.mode === 'development' ? '' : 'http://localhost:8000',
  timeout: 30000,
})

export interface Status {
  paired: boolean
  connected: boolean
  pairing: boolean
  paired_switch_address?: string
}

export interface AmiiboFile {
  path: string
  name: string
  relative_path: string
  size: number
}

export interface NFCStatus {
  loaded: boolean
  source?: string
}

export const apiService = {
  // 获取状态
  async getStatus(): Promise<Status> {
    const response = await api.get<Status>('/api/status')
    return response.data
  },

  // 配对
  async pair(reconnect: boolean = false): Promise<{ success: boolean; message: string }> {
    const response = await api.post<{ success: boolean; message: string }>('/api/pair', { reconnect })
    return response.data
  },

  // 连接
  async connect(): Promise<{ success: boolean; message: string }> {
    const response = await api.post<{ success: boolean; message: string }>('/api/connect')
    return response.data
  },

  // 断开连接
  async disconnect(): Promise<{ success: boolean; message: string }> {
    const response = await api.post<{ success: boolean; message: string }>('/api/disconnect')
    return response.data
  },

  // 按下按钮
  async pressButton(buttons: string[]): Promise<{ success: boolean }> {
    const response = await api.post<{ success: boolean }>('/api/button/press', { buttons })
    return response.data
  },

  // 释放按钮
  async releaseButton(buttons: string[]): Promise<{ success: boolean }> {
    const response = await api.post<{ success: boolean }>('/api/button/release', { buttons })
    return response.data
  },

  // 点击按钮
  async clickButton(buttons: string[]): Promise<{ success: boolean }> {
    const response = await api.post<{ success: boolean }>('/api/button/click', { buttons })
    return response.data
  },

  // 设置摇杆
  async setStick(stick: 'l' | 'r', x: number, y: number): Promise<{ success: boolean }> {
    const response = await api.post<{ success: boolean }>('/api/stick', { stick, x, y })
    return response.data
  },

  // 列出 NFC 文件
  async listNFCFiles(): Promise<{ files: AmiiboFile[] }> {
    const response = await api.get<{ files: AmiiboFile[] }>('/api/nfc/files')
    return response.data
  },

  // 加载 NFC
  async loadNFC(filePath: string): Promise<{ success: boolean; message: string }> {
    const response = await api.post<{ success: boolean; message: string }>('/api/nfc/load', null, {
      params: { file_path: filePath }
    })
    return response.data
  },

  // 移除 NFC
  async removeNFC(): Promise<{ success: boolean; message: string }> {
    const response = await api.post<{ success: boolean; message: string }>('/api/nfc/remove')
    return response.data
  },

  // 获取 NFC 状态
  async getNFCStatus(): Promise<NFCStatus> {
    const response = await api.get<NFCStatus>('/api/nfc/status')
    return response.data
  },
}

