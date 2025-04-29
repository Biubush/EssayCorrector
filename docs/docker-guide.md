# Docker部署指南 - 论文纠错系统

本文档详细介绍如何使用Docker和Docker Compose部署论文纠错系统。

## 文档导航
- [返回项目主页](../README.md)
- **当前文档**：Docker部署指南
- [Docker环境变量配置指南](docker-config-guide.md)

## 前提条件

在开始之前，请确保您的系统已安装：

1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/install/)（新版Docker已内置）

## 快速开始

最简单的部署方式是使用我们提供的脚本：

### Windows平台

双击项目根目录下的`start-docker.bat`文件，或在命令行中执行：

```bash
start-docker.bat
```

### Linux/macOS平台

```bash
chmod +x start-docker.sh
./start-docker.sh
```

部署完成后，打开浏览器访问：http://localhost:8329

## 手动部署步骤

如果您希望手动部署，可以按照以下步骤操作：

1. **克隆项目**（如果尚未克隆）：

   ```bash
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **构建并启动容器**：

   ```bash
   docker-compose up -d
   ```

   初次运行可能需要一些时间来下载和构建镜像。

3. **查看容器状态**：

   ```bash
   docker-compose ps
   ```

   确保容器状态为"Up"。

4. **访问应用**：
   
   打开浏览器，访问 http://localhost:8329

## 运行模式

本应用支持两种运行模式：

- **生产模式**（默认）：使用Gunicorn和Eventlet作为WSGI服务器，提供更好的性能和稳定性
- **开发模式**：使用Flask内置的Werkzeug服务器，方便调试

### 切换运行模式

修改`docker-compose.yml`文件中的环境变量：

```yaml
environment:
  # 设置工作模式，可选值：production, development
  - MODE=development  # 改为开发模式
```

## 自定义配置

### 自定义AI校对规则

系统支持通过提示词文件自定义AI校对规则。默认情况下，提示词文件已挂载到容器中：

```yaml
volumes:
  # 提示词文件挂载
  - ./prompts.txt:/app/prompts.txt
```

您可以直接编辑项目根目录下的`prompts.txt`文件来修改校对规则。该文件支持多种格式，包括但不限于：

- 简单的列表格式（每行一条规则）
- Markdown格式（支持标题、列表、粗体等）
- 结构化内容（如分类规则、处理流程等）
- JSON示例（系统会正确处理文件中的大括号）

例如，您可以使用以下内容结构进行组织：

```
# 基础校对规则

## 语法校对
1. 校对学术论文中的语法错误，包括标点符号、拼写错误和语法结构问题
2. 修正不恰当的学术表达，使其更加专业和准确

## 格式校对
- 维护文档格式的一致性
- 确保引用格式正确

## 特殊处理
专业术语、公式、代码片段等不做修改
```

编辑完成后，无需重启容器，系统会在下一次处理文档时自动加载最新的提示词。

如果您希望使用不同路径的提示词文件，可以通过环境变量和卷挂载来配置：

```yaml
volumes:
  # 使用自定义路径的提示词文件
  - /path/to/your/custom_prompts.txt:/app/custom_prompts.txt
  
environment:
  # 设置提示词文件路径
  - PROMPTS_FILE=/app/custom_prompts.txt
```

### 修改端口

如果您想更改默认端口（8329），可以编辑`docker-compose.yml`文件中的端口映射：

```yaml
ports:
  - "自定义端口:8329"  # 例如：8080:8329
```

### 配置AI API密钥

要配置您自己的AI API密钥，可以取消注释并修改`docker-compose.yml`中的环境变量：

```yaml
environment:
  - AI_API_KEY=your_api_key_here  # 将your_api_key_here替换为您的实际API密钥
```

### 资源限制

可以调整容器的资源限制，根据您的服务器情况配置：

```yaml
deploy:
  resources:
    limits:
      cpus: '2'        # 最多使用2个CPU核心
      memory: 2G       # 最多使用2GB内存
    reservations:
      cpus: '0.5'      # 保证分配0.5个CPU核心
      memory: 512M     # 保证分配512MB内存
```

### 数据持久化

默认情况下，数据库和临时文件已配置为持久化存储：

```yaml
volumes:
  # 持久化存储数据库
  - ./database:/app/database
  # 持久化存储临时文件
  - essay_corrector_temp:/tmp/essay_corrector_temp
```

数据库文件存储在项目根目录的`database`文件夹中，临时文件存储在Docker卷中。系统会自动创建数据库文件`database/tasks.db`。

## 常用操作

### 启动服务

```bash
docker-compose up -d
```

### 停止服务

```bash
docker-compose down
```

### 查看日志

```bash
docker-compose logs -f
```

### 查看容器健康状态

```bash
docker inspect --format='{{.State.Health.Status}}' essay-corrector
```

### 重启服务

```bash
docker-compose restart
```

### 重建服务

如果您修改了代码或配置并希望重新构建镜像：

```bash
docker-compose build
docker-compose up -d
```

## 故障排除

### 服务无法启动

1. 检查端口是否被占用

   ```bash
   # Windows
   netstat -ano | findstr 8329
   
   # Linux/macOS
   lsof -i :8329
   ```

2. 检查Docker错误日志

   ```bash
   docker-compose logs -f
   ```

### 如果遇到Werkzeug相关错误

如果您在使用开发模式时遇到以下错误：

```
RuntimeError: The Werkzeug web server is not designed to run in production. Pass allow_unsafe_werkzeug=True to the run() method to disable this error.
```

请切换到生产模式（MODE=production），或者在app.py中添加`allow_unsafe_werkzeug=True`参数：

```python
socketio.run(app, debug=DEBUG, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
```

### 服务启动但无法访问

1. 确认容器正在运行

   ```bash
   docker-compose ps
   ```

2. 确认端口映射正确

   ```bash
   docker-compose port essay-corrector 8329
   ```

3. 检查防火墙设置，确保允许该端口的访问

## 性能调优

如果您在处理大量文档时遇到性能问题，可以考虑增加容器的资源限制：

```yaml
services:
  essay-corrector:
    # 其他配置...
    deploy:
      resources:
        limits:
          memory: 4G  # 增加内存限制
          cpus: '2'   # 分配2个CPU核心
```

## 安全注意事项

1. 避免在生产环境中使用默认的API密钥
2. 如果将服务暴露在公网，请考虑使用HTTPS和身份验证
3. 定期更新Docker镜像以获取安全补丁
4. 在生产环境中使用MODE=production以避免使用不安全的开发服务器

## 更多信息

如需更多信息，请访问：
- [Docker文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [Gunicorn文档](https://docs.gunicorn.org/)
- [项目README](../README.md)
- [Docker环境变量配置指南](docker-config-guide.md) 