FROM python:3.10-slim

LABEL maintainer="biubush"
LABEL description="论文纠错系统 - AI驱动的论文语法纠错工具"

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    antiword \
    catdoc \
    libreoffice \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装可选的textract (使用特定版本的pip)
RUN pip install pip==23.3.2 && \
    pip install --no-cache-dir textract && \
    pip install --upgrade pip

# 安装gunicorn和eventlet（用于生产环境）
RUN pip install --no-cache-dir gunicorn eventlet

# 复制应用代码
COPY . .

# 设置环境变量
ENV HOST=0.0.0.0
ENV PORT=8329
ENV TEMP_FOLDER=/tmp/essay_corrector_temp
ENV MODE=production

# 创建临时目录
RUN mkdir -p $TEMP_FOLDER && chmod 777 $TEMP_FOLDER

# 设置入口脚本权限
RUN chmod +x docker-entrypoint.sh

# 暴露端口
EXPOSE 8329

# 使用入口脚本
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# 开发环境启动命令（如需使用，替换上面的ENTRYPOINT）
# CMD ["python", "app.py"] 