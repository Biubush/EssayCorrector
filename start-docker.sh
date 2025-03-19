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

# 环境变量数组
ENV_VARS=()
ARG_COUNT=0

# 处理命令行参数（环境变量）
while [[ $# -gt 0 ]]; do
    case "$1" in
        -e)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "[错误] -e 参数后需要提供环境变量"
                exit 1
            fi
            # 添加到环境变量数组
            ENV_VARS+=("$2")
            ARG_COUNT=$((ARG_COUNT+1))
            shift 2
            ;;
        *)
            echo "[错误] 未知参数: $1"
            exit 1
            ;;
    esac
done

# 如果有参数，提示用户
if [ $ARG_COUNT -gt 0 ]; then
    echo "检测到 $ARG_COUNT 个环境变量参数"
fi

# 构建命令，为每个环境变量导出
for env_var in "${ENV_VARS[@]}"; do
    # 分割变量名和值
    IFS='=' read -r key value <<< "$env_var"
    # 导出变量到当前shell
    export "$key"="$value"
    echo "设置环境变量: $key=$value"
done

# 启动容器
echo "正在启动服务..."
echo "执行命令: $DOCKER_COMPOSE_CMD up -d"
$DOCKER_COMPOSE_CMD up -d

# 检查启动结果
if [ $? -ne 0 ]; then
    echo "[错误] 启动服务失败，请查看上方错误信息"
    exit 1
fi

echo "服务已成功启动!"
echo "请访问 http://localhost:8329 使用论文纠错系统" 