#!/bin/bash
set -e

# 启动 dbus
service dbus start

# 启动 bluetoothd
echo "Starting bluetoothd"
bluetoothd --noplugin=input > /var/log/bluetoothd.log 2>&1 &
echo "Bluetoothd started"

# 启动后端 API 服务（后台运行）
echo "Starting backend API server"
cd /backend
python3 ./api_server.py > /var/log/api_server.log 2>&1 &
echo "Backend API server started on port 8000"

# 等待后端服务启动
sleep 2

# 执行传入的命令（通常是 nginx）
exec "$@"
