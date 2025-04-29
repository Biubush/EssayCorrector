#!/bin/bash
# Docker容器入口脚本 - 论文纠错系统
# 
# 本脚本用于在Docker容器内部启动应用程序
# 支持生产和开发两种模式
# 
# @author: Biubush

set -e

# 检测运行模式
if [ "$MODE" = "development" ]; then
    echo "以开发模式启动应用..."
    exec python app.py
else
    echo "以生产模式启动应用..."
    # 启动gunicorn
    exec gunicorn --worker-class eventlet \
                 -w 1 \
                 --bind 0.0.0.0:${PORT:-8329} \
                 --log-level info \
                 --access-logfile - \
                 --error-logfile - \
                 app:app
fi 