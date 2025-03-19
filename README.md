# 论文纠错系统 (Essay Corrector)

一个基于AI的论文语法纠错工具，支持多种文档格式、实时进度反馈和批量处理功能。

作者：[biubush](https://github.com/biubush)

## 项目介绍

论文纠错系统是一个面向学术写作的智能辅助工具，通过结合先进的AI技术，帮助作者识别并修正论文中的语法错误、拼写错误、表达不准确等问题，提高学术写作质量。

### 项目功能

- **多格式文档支持**：支持Word、PDF、TXT、Excel、Markdown、PowerPoint等多种文档格式
- **AI驱动的语法检查**：利用先进的AI模型分析文本，检测语法和表达问题
- **实时进度反馈**：通过WebSocket技术实时向用户展示处理进度
- **详细的纠错报告**：提供可视化的纠错结果，包括错误定位、错误类型和修改建议
- **多线程处理**：使用多线程技术提高处理大文档的效率
- **任务持久化存储**：将任务状态存储到数据库
- **定期清理临时文件**：自动清理过期的临时文件，节省存储空间

## 项目特色

1. **用户友好的Web界面**：直观简洁的上传和结果展示界面，无需安装客户端
2. **实时进度展示**：精确显示处理进度、已用时间和预计剩余时间
3. **跨平台兼容性**：支持Windows、Linux和macOS等多种操作系统
4. **高效的文本提取**：针对不同文档格式优化的文本提取算法
5. **深度AI分析**：使用专业的AI模型进行语法和表达分析，支持学术写作场景
6. **可扩展架构**：模块化设计，易于扩展支持新的文档格式和AI模型
7. **多种部署方式**：支持本地安装和Docker容器化部署

## 如何运行

我们提供了多种方式运行论文纠错系统，您可以根据自己的需求选择最适合的方式。

### 方法1：Docker一键部署（推荐）

如果您已安装Docker和Docker Compose，可以使用以下命令快速部署：

```bash
# 克隆项目
git clone https://github.com/biubush/EssayCorrector.git
cd EssayCorrector

# 启动服务
docker-compose up -d
```

然后访问 http://localhost:8329 即可使用服务。

#### 自定义Docker配置

您可以通过编辑`docker-compose.yml`文件来自定义Docker部署：

```yaml
# 修改端口映射
ports:
  - "8080:8329"  # 改为使用8080端口访问

# 设置自定义API密钥
environment:
  - AI_API_KEY=your_api_key_here  # 取消注释并设置您的API密钥
```

### 方法2：通用引导脚本安装

无论您使用的是Windows、Linux还是macOS，只需运行Python引导脚本即可：

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **运行通用引导脚本**：
   ```
   python install.py
   ```
   
   该脚本将自动检测您的操作系统类型，并调用相应的安装脚本。

   如需安装可选依赖，可以传递参数：
   ```
   python install.py --with-textract
   ```

3. **启动应用**：
   安装完成后，使用生成的启动脚本启动应用：
   - Windows: 双击`start.bat`
   - Linux/macOS: 执行`./start.sh`

4. **访问应用**：
   打开浏览器，访问 http://localhost:8329

### 方法3：平台特定脚本安装

#### Windows平台

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **运行配置脚本**：
   双击`scripts/setup.bat`文件，或在命令行中执行：
   ```
   scripts\setup.bat
   ```
   
   脚本将自动检测您的系统，安装必要的依赖，并创建启动脚本。

3. **启动应用**：
   配置完成后，双击`start.bat`文件，或在命令行中执行：
   ```
   start.bat
   ```

4. **访问应用**：
   打开浏览器，访问 http://localhost:8329

#### Linux/macOS平台

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **运行配置脚本**：
   ```
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```
   
   脚本将自动检测您的系统，安装必要的依赖，并创建启动脚本。
   
   如果需要安装可选依赖，可以使用：
   ```
   ./scripts/setup.sh --with-textract
   ```

3. **启动应用**：
   配置完成后，执行：
   ```
   ./start.sh
   ```

4. **访问应用**：
   打开浏览器，访问 http://localhost:8329

### 高级配置选项

自动配置脚本支持以下命令行参数：

- `--no-venv`: 不创建虚拟环境，使用系统Python
- `--venv-dir PATH`: 指定虚拟环境目录（默认: .venv）
- `--recreate-venv`: 如果虚拟环境已存在，重新创建
- `--with-textract`: 安装textract包（可选但建议）
- `--no-system-deps`: 跳过系统依赖安装

例如：
```
python install.py --venv-dir custom_env --with-textract
```

### 手动安装

如果您希望手动安装，请按照以下步骤操作：

#### Windows平台

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```
   
   注意：某些依赖可能需要特定版本的pip进行安装，详见requirements.txt中的注释

3. **运行应用**：
   直接双击`entrance.bat`文件，或在命令行中执行：
   ```
   .conda\python.exe app.py
   ```

#### Linux/macOS平台

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```
   
   对于Linux，可能需要额外安装一些系统依赖：
   ```
   sudo apt-get install antiword catdoc libreoffice
   ```

3. **运行应用**：
   ```
   python app.py
   ```

## 配置说明

系统的主要配置位于`config.py`文件中，您可以根据需要修改以下配置：

- **服务器配置**：修改HOST和PORT调整服务器监听地址和端口
- **AI模型配置**：更换AI_API_KEY和AI_MODEL以使用不同的AI模型
- **文件类型配置**：通过ALLOWED_EXTENSIONS修改支持的文件格式
- **清理配置**：调整CLEANUP_INTERVAL_HOURS设置临时文件清理频率
- **AI提示词配置**：通过`prompts.txt`文件自定义校对规则，系统会自动加载该文件

### 自定义校对规则

您可以通过修改项目根目录下的`prompts.txt`文件来自定义AI校对规则。系统支持多种格式的提示词文件：

**基础列表格式**：
```
1. 校对学术论文中的语法错误，包括标点符号、拼写错误和语法结构问题
2. 修正不恰当的学术表达，使其更加专业和准确
3. 纠正不一致的时态和语态
```

**结构化Markdown格式**：
```
# 校对规则

## 语法校对
- 修正主谓不一致问题
- 调整不连贯或不流畅的句子

## 内容保护
- 保留所有专业术语和公式
```

**包含JSON示例的复杂格式**：
```
# 输出格式示例
用这种格式表示修改：[{"theorigin":"原句","corrected":"修正句"}]
```

修改后，系统会在下一次处理文档时自动加载新的规则。您也可以通过修改`config.py`中的`PROMPTS_FILE`配置项来指定不同的提示词文件路径。

### Docker环境变量配置

在Docker环境中，您可以通过环境变量覆盖配置：

- `HOST`: 监听地址（默认：0.0.0.0）
- `PORT`: 监听端口（默认：8329）
- `TEMP_FOLDER`: 临时文件夹路径
- `AI_API_KEY`: AI API密钥
- `AI_MODEL`: 使用的AI模型
- `PROMPTS_FILE`: 提示词文件路径（默认：prompts.txt）

详细配置指南请参考[Docker环境变量配置指南](docs/docker-config-guide.md)。

## 技术栈

- **后端**：Python, Flask, Socket.IO, SQLAlchemy
- **前端**：HTML, CSS, JavaScript, Bootstrap
- **AI**：基于多种AI模型（如deepseek-chat, deepseek-reasoner等）
- **数据处理**：PyPDF2, python-docx, markdown, openpyxl等
- **容器化**：Docker, Docker Compose

## 项目结构

```
EssayCorrector/
├── app.py              # 主应用入口
├── config.py           # 配置文件
├── models.py           # 数据模型
├── requirements.txt    # 依赖列表
├── Dockerfile          # Docker镜像构建文件
├── docker-compose.yml  # Docker Compose配置
├── core/               # 核心功能模块
│   ├── __init__.py
│   ├── AI_solver.py    # AI求解器
│   ├── corrector.py    # 纠错器
│   └── data_processor.py # 文档处理器
├── scripts/            # 安装脚本
│   ├── install.py      # 安装引导脚本
│   ├── setup.py        # 主安装脚本
│   ├── setup.bat       # Windows安装脚本
│   └── setup.sh        # Linux/macOS安装脚本
└── templates/          # 前端模板
    └── index.html      # 主页面
```

## 注意事项

1. 首次运行时会自动创建数据库和临时文件夹
2. 默认使用8329端口，请确保该端口未被占用
3. 对于大型文档，处理时间可能较长，请耐心等待
4. AI模型需要有效的API密钥才能正常使用
5. 安装脚本需要Python 3.6+环境
6. Docker部署需要安装Docker和Docker Compose

## 许可证

本项目遵循MIT许可证。

感谢您对本项目的关注和支持！ 