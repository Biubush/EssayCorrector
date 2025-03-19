#!/bin/bash
# Docker启动脚本 - 论文纠错系统
# 
# 本脚本用于通过Docker Compose启动论文纠错系统
# 
# @author: Biubush

echo "正在启动论文纠错系统 Docker 容器..."

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "[错误] 未检测到Docker，请先安装Docker"
    echo "请访问 https://docs.docker.com/get-docker/ 获取安装指南"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "[错误] 未检测到Docker Compose，请先安装Docker Compose"
    echo "请访问 https://docs.docker.com/compose/install/ 获取安装指南"
    exit 1
fi

# 检查docker-compose命令的可用性
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    DOCKER_COMPOSE_CMD="docker compose"
fi

# 检查docker-compose.yml文件是否存在
if [ ! -f "docker-compose.yml" ]; then
    echo "[错误] 未找到docker-compose.yml文件"
    echo "请确保您在正确的目录下运行此脚本"
    exit 1
fi

# 启动容器
echo "正在启动服务..."
$DOCKER_COMPOSE_CMD up -d

# 检查启动结果
if [ $? -ne 0 ]; then
    echo "[错误] 启动服务失败，请查看上方错误信息"
    exit 1
fi

echo "服务已成功启动!"
echo "请访问 http://localhost:8329 使用论文纠错系统"
echo
echo "提示：如需修改配置，请编辑docker-compose.yml文件后重新运行此脚本" 