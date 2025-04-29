#!/bin/bash
# Docker容器入口脚本 - 论文纠错系统
# 
# 本脚本用于在Docker容器内部启动应用程序
# 支持生产和开发两种模式
# 
# @author: Biubush

set -e

# 创建必要的目录
mkdir -p /app/database
mkdir -p $TEMP_FOLDER

echo "=== 论文纠错系统启动 ==="
echo "工作模式: ${MODE:-production}"

# 检测运行模式
if [ "$MODE" = "development" ]; then
    echo "使用开发模式启动..."
    exec python app.py
else
    echo "使用生产模式启动..."
    # 启动gunicorn
    exec gunicorn --worker-class eventlet \
                 -w 1 \
                 --bind ${HOST:-0.0.0.0}:${PORT:-8329} \
                 --log-level info \
                 --access-logfile - \
                 --error-logfile - \
                 app:app
fi 