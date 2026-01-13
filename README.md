# JoyControl 飞牛OS应用

这是一个前后端分离的 Switch Pro 手柄模拟器应用，用于飞牛OS平台。

## 功能特性

- ✅ Switch Pro 手柄模拟
- ✅ 配对和连接管理
- ✅ 可视化手柄界面，支持点击和按住操作
- ✅ 摇杆控制
- ✅ NFC/Amiibo 模拟
- ✅ Amiibo 文件管理

## 项目结构

```
joycontrol_fnos/
├── backend/          # 后端代码（Python + FastAPI）
│   ├── joycontrol/   # JoyControl 库
│   ├── api_server.py # API 服务器
│   └── requirements.txt
├── frontend/         # 前端代码（Vue3 + TypeScript + Vite）
└── docs/            # 文档
```

## 环境要求

### 后端
- Python 3.8+
- 需要 root 权限（用于蓝牙操作）
- Linux 系统（需要 bluez）

### 前端
- Node.js 16+
- npm 或 yarn

## 安装和运行

### 后端

1. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

2. 安装系统依赖（Ubuntu/Debian）：
```bash
sudo apt-get install bluez python3-dbus
```

3. 运行服务器（需要 root 权限）：
```bash
sudo python3 api_server.py
```

服务器将在 `http://0.0.0.0:8000` 启动。

### 前端

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 开发模式运行：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

## 使用说明

### 配对 Switch

1. 打开应用，如果未配对，点击"开始配对"
2. 在 Switch 上打开"更改握法/顺序"菜单
3. 等待配对完成

### 连接已配对的设备

如果已经配对过，可以直接点击"连接"按钮连接。

### 使用手柄

- **点击按钮**：鼠标点击按钮，松开即释放
- **按住按钮**：鼠标按下按钮并保持，松开时释放
- **摇杆**：点击摇杆区域并拖动，松开时回中

### NFC/Amiibo 功能

1. 点击"NFC / Amiibo"按钮
2. 在弹窗中选择要加载的 .bin 文件
3. 确认后，Amiibo 将被加载到控制器
4. 可以随时点击"移除"来停止 NFC 模拟

### Amiibo 文件位置

默认情况下，应用会在 `~/amiibo` 目录下查找 .bin 文件。你可以将 Amiibo 文件放在该目录或其子目录中。

## API 接口

### 状态相关
- `GET /api/status` - 获取连接状态
- `POST /api/pair` - 配对
- `POST /api/connect` - 连接
- `POST /api/disconnect` - 断开连接

### 按键控制
- `POST /api/button/press` - 按下按钮
- `POST /api/button/release` - 释放按钮
- `POST /api/button/click` - 点击按钮

### 摇杆控制
- `POST /api/stick` - 设置摇杆位置

### NFC 相关
- `GET /api/nfc/files` - 列出 Amiibo 文件
- `POST /api/nfc/load` - 加载 NFC
- `POST /api/nfc/remove` - 移除 NFC
- `GET /api/nfc/status` - 获取 NFC 状态

## 注意事项

1. **权限要求**：后端需要 root 权限才能操作蓝牙
2. **蓝牙适配器**：确保系统有可用的蓝牙适配器
3. **配对状态**：配对信息保存在 `~/.joycontrol_config.json`
4. **Amiibo 文件**：确保 .bin 文件格式正确（540 或 572 字节）

## 开发

### 后端开发

后端使用 FastAPI，支持自动重载（需要安装 `uvicorn[standard]`）：

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

前端使用 Vite，支持热重载：

```bash
npm run dev
```

## 许可证

查看 LICENSE 文件了解详情。

