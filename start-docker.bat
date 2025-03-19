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

REM 初始化命令字符串
SET CMD_STR=%DOCKER_COMPOSE_CMD% up -d

REM 处理命令行参数（环境变量）
SET PARSING_ARGS=true
SET ARG_COUNT=0

:parse_args
IF "%~1"=="" GOTO execute_command
IF "%~1"=="-e" (
    IF "%~2"=="" (
        echo [错误] -e 参数后需要提供环境变量
        pause
        exit /b 1
    )
    SET /A ARG_COUNT+=1
    SET CMD_STR=%CMD_STR% -e %~2
    SHIFT
    SHIFT
    GOTO parse_args
)

echo [错误] 未知参数: %~1
pause
exit /b 1

:execute_command
REM 如果有参数，提示用户
IF %ARG_COUNT% GTR 0 (
    echo 检测到 %ARG_COUNT% 个环境变量参数
)

REM 启动容器
echo 正在启动服务...
echo 执行命令: %CMD_STR%
%CMD_STR%

REM 检查启动结果
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 启动服务失败，请查看上方错误信息
    pause
    exit /b 1
)

echo 服务已成功启动!
echo 请访问 http://localhost:8329 使用论文纠错系统
pause 