# 快速开始指南

## 1. 安装后端依赖

```bash
cd backend
pip3 install -r requirements.txt
```

## 2. 安装系统依赖（Linux）

```bash
sudo apt-get update
sudo apt-get install bluez python3-dbus
```

## 3. 启动后端服务器

**注意：需要 root 权限**

```bash
cd backend
sudo python3 api_server.py
```

或者使用启动脚本：

```bash
sudo ./start_server.sh
```

服务器将在 `http://0.0.0.0:12389` 启动。

## 4. 启动前端

打开新的终端窗口：

```bash
cd frontend
npm install  # 首次运行需要
npm run dev
```

前端将在 `http://localhost:5173` 启动（或 Vite 显示的端口）。

## 5. 使用应用

1. 在浏览器中打开前端地址
2. 如果未配对，点击"开始配对"
3. 在 Switch 上打开"更改握法/顺序"菜单
4. 等待配对完成
5. 配对成功后，界面会自动切换到手柄控制界面

## 6. 准备 Amiibo 文件（可选）

将 .bin 格式的 Amiibo 文件放置在 `~/amiibo` 目录下：

```bash
mkdir -p ~/amiibo
# 将 .bin 文件复制到此目录
```

## 故障排除

### 后端无法启动

- 确保使用 `sudo` 运行（需要 root 权限）
- 检查蓝牙适配器是否可用：`hciconfig`
- 检查 Python 依赖是否安装：`pip3 list | grep fastapi`

### 前端无法连接后端

- 确保后端服务器正在运行
- 检查防火墙设置
- 在开发模式下，Vite 会自动代理 `/api` 请求

### 配对失败

- 确保 Switch 在"更改握法/顺序"菜单中
- 检查蓝牙适配器是否正常工作
- 查看后端日志获取详细错误信息

### NFC 功能不可用

- 确保使用的是 Pro Controller（不是 Joy-Con L）
- 检查 Amiibo 文件格式（应为 540 或 572 字节）
- 确保文件路径正确

