@echo off
REM Docker启动脚本 - 论文纠错系统
REM 
REM 本脚本用于通过Docker Compose启动论文纠错系统
REM 
REM @author: Biubush

echo 正在启动论文纠错系统 Docker 容器...

REM 检查Docker是否安装
docker --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Docker，请先安装Docker
    echo 请访问 https://docs.docker.com/get-docker/ 获取安装指南
    pause
    exit /b 1
)

REM 检查Docker Compose是否可用 (新版Docker已集成)
docker compose version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    docker-compose --version > nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [错误] 未检测到Docker Compose，请先安装Docker Compose
        echo 请访问 https://docs.docker.com/compose/install/ 获取安装指南
        pause
        exit /b 1
    ) else (
        SET DOCKER_COMPOSE_CMD=docker-compose
    )
) else (
    SET DOCKER_COMPOSE_CMD=docker compose
)

REM 检查docker-compose.yml文件是否存在
if not exist docker-compose.yml (
    echo [错误] 未找到docker-compose.yml文件
    echo 请确保您在正确的目录下运行此脚本
    pause
    exit /b 1
)

REM 启动容器
echo 正在启动服务...
%DOCKER_COMPOSE_CMD% up -d

REM 检查启动结果
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 启动服务失败，请查看上方错误信息
    pause
    exit /b 1
)

echo 服务已成功启动!
echo 请访问 http://localhost:8329 使用论文纠错系统
echo.
echo 提示：如需修改配置，请编辑docker-compose.yml文件后重新运行此脚本
pause 