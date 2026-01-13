#!/bin/bash
# 启动 API 服务器脚本

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then 
    echo "请使用 sudo 运行此脚本（需要 root 权限操作蓝牙）"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查依赖
echo "检查依赖..."
python3 -c "import fastapi" 2>/dev/null || {
    echo "安装依赖..."
    pip3 install -r requirements.txt
}

# 启动服务器
echo "启动 API 服务器..."
python3 api_server.py

