FROM python:3.9

# 安装系统依赖和 nginx
RUN apt update \
    && apt install -y libglib2.0-dev libhidapi-hidraw0 libhidapi-libusb0 libdbus-1-dev bluetooth usbutils git nginx \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY ./backend /backend
RUN pip3 install -r /backend/requirements.txt

# 复制构建好的前端文件到 nginx 目录
COPY ./frontend/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# 复制启动脚本
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 创建 amiibo 目录并设置为数据卷
RUN mkdir -p /amiibo
VOLUME ["/amiibo"]

WORKDIR /backend
EXPOSE 80

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
