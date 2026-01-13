#!/bin/bash
set -e

# 启动 dbus
service dbus start

# 启动 bluetoothd
echo "Starting bluetoothd"
bluetoothd --noplugin=input > /var/log/bluetoothd.log 2>&1 &
echo "Bluetoothd started"

# 启动 nginx（后台运行）
echo "Starting nginx"
nginx > /var/log/nginx.log 2>&1 &
echo "Nginx started on port 80"

# 等待 nginx 启动
sleep 1

# 执行传入的命令（通常是后端 API 服务，前台运行以便查看日志）
exec "$@"
