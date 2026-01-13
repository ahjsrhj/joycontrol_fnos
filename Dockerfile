FROM nginx

# 创建 www 目录
RUN mkdir -p /www

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
