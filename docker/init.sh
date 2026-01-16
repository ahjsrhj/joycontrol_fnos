#!/bin/bash


# 前端构建
cd ../frontend
npm run build
cd ../docker


# 构建前端镜像
docker build -t joycontrol-frontend -f Dockerfile.frontend .

# 构建后端镜像
docker build -t joycontrol-backend -f Dockerfile.backend .