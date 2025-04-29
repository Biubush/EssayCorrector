# 论文纠错助手 (Essay Corrector)

一个基于AI的论文语法纠错工具，支持多种文档格式、实时进度反馈和批量处理功能。

作者：[Biubush](https://github.com/biubush) × [Cursor](https://www.cursor.com)

## 文档导航
- **当前文档**：项目主要说明文档 (README.md)
- [Docker部署指南](docs/docker-guide.md)
- [Docker环境变量配置指南](docs/docker-config-guide.md)

## 项目介绍

论文纠错系统是一个面向学术写作的智能辅助工具，通过结合先进的AI技术，帮助作者识别并修正论文中的语法错误、拼写错误、表达不准确等问题，提高学术写作质量。它特别适合非母语写作者和需要提升学术文章质量的研究人员使用。

### 项目功能

- **多格式文档支持**：支持包括Word (.doc/.docx/.docm/.dotm)、PDF、TXT、Excel (.xls/.xlsx/.xlsm)、CSV、Markdown (.md/.markdown)、PowerPoint (.ppt/.pptx/.pptm) 等多种文档格式
- **AI驱动的语法检查**：利用DeepSeek AI模型分析文本，检测语法和表达问题，提供专业修改建议
- **实时进度反馈**：通过WebSocket技术实时向用户展示处理进度、已用时间和预计剩余时间
- **详细的纠错报告**：提供可视化的纠错结果，包括错误定位、错误类型和修改建议，易于理解和采纳
- **多线程处理**：使用多线程技术提高处理大文档的效率，缩短等待时间
- **任务持久化存储**：将任务状态和结果存储到SQLite数据库，支持会话之间的任务查询和结果访问
- **定期清理临时文件**：通过后台定时任务自动清理过期的临时文件，节省存储空间
- **自定义校对规则**：支持通过编辑prompts.txt文件自定义AI校对规则和指令

## 项目特色

1. **用户友好的Web界面**：
   - 简洁直观的拖放式文件上传界面
   - 实时进度条和时间估计显示
   - 交互式的结果展示，支持对比查看原文和修改后的文本
   - 响应式设计，适配不同设备屏幕

2. **精确的实时进度展示**：
   - 显示处理百分比进度
   - 展示已用处理时间
   - 预估剩余处理时间
   - 处理段落计数（当前/总数）

3. **跨平台兼容性**：
   - 完全支持Windows系统
   - 支持Linux和macOS系统（带特定依赖）
   - 通过Docker容器化实现全平台无差别体验

4. **专业的文本提取技术**：
   - 针对不同文档格式优化的文本提取算法
   - 多层次的格式检测和兼容处理
   - 智能的段落合并与文本预处理
   - 对特殊字符和公式的保护机制

5. **深度AI分析**：
   - 使用专业的DeepSeek AI模型进行语法分析
   - 支持中英文混合文本的校对
   - 尊重学术领域专业术语和表达习惯
   - 可自定义的校对规则和语言风格

6. **模块化架构**：
   - 清晰的代码组织和模块划分
   - 可扩展的文档处理器接口
   - 灵活的AI模型配置
   - 易于添加新的文档格式支持

7. **完善的部署方案**：
   - 支持本地安装（Windows/Linux/macOS）
   - Docker容器化一键部署
   - 详细的安装指南和故障排除文档
   - 多种配置选项，适应不同环境需求

## 系统架构

论文纠错系统采用模块化设计，主要包含以下核心组件：

1. **Web服务器**：基于Flask框架，提供HTTP接口和WebSocket实时通信
2. **文档处理模块**：包含多种文档格式的处理器，负责提取文本内容
3. **AI求解器**：与DeepSeek API交互，发送文本段落并获取修改建议
4. **纠错器**：协调文档处理和AI分析流程，生成最终结果
5. **数据存储**：使用SQLite数据库存储任务状态和结果
6. **前端界面**：基于HTML/CSS/JavaScript构建的用户界面

### 工作流程

1. 用户通过Web界面上传文档
2. 系统创建任务并保存到数据库
3. 后台线程启动处理流程：
   - 根据文件类型选择合适的文档处理器
   - 提取文本内容并分割为段落
   - 合并段落以优化AI处理
   - 对每个段落请求AI分析
   - 实时向前端报告进度
4. 处理完成后，生成包含原文和修改建议的结果
5. 结果存储到数据库并通知前端
6. 用户可在界面上查看和应用修改建议

## 如何运行

我们提供了多种方式运行论文纠错系统，您可以根据自己的需求选择最适合的方式。

### 方法1：Docker一键部署（推荐）

Docker部署是最简单、兼容性最好的方法，无需担心环境配置问题。

#### 前提条件
- 已安装Docker和Docker Compose
- 拥有可用的DeepSeek API密钥（可选，也可使用默认测试密钥）

#### 部署步骤

```bash
# 克隆项目
git clone https://github.com/biubush/EssayCorrector.git
cd EssayCorrector

# Windows系统使用
.\start-docker.bat

# Linux/macOS系统使用
chmod +x start-docker.sh
./start-docker.sh
```

如果一切正常，控制台将显示服务启动信息，然后访问 http://localhost:8329 即可使用服务。

#### Docker部署的高级选项

您可以通过编辑`docker-compose.yml`文件来自定义Docker部署：

```yaml
# 修改端口映射
ports:
  - "8080:8329"  # 改为使用8080端口访问

# 设置自定义API密钥和模型
environment:
  - AI_API_KEY=your_api_key_here  # 设置您的DeepSeek API密钥
  - AI_MODEL=deepseek-chat  # 选择使用的AI模型
  - PROMPTS_FILE=/app/custom_prompts.txt  # 自定义提示词文件路径

volumes:
  # 持久化存储数据库
  - ./tasks.db:/app/tasks.db
```

如果您需要修改配置，请直接编辑`docker-compose.yml`文件，然后重新启动容器：

```bash
# Windows
.\start-docker.bat

# Linux/macOS
./start-docker.sh
```

> **详细说明**：
> - 完整的Docker部署说明请参阅[Docker部署指南](docs/docker-guide.md)
> - 环境变量配置的详细信息请参阅[Docker环境变量配置指南](docs/docker-config-guide.md)

### 方法2：通用引导脚本安装

无论您使用的是Windows、Linux还是macOS，只需运行Python引导脚本即可完成安装：

#### 前提条件
- Python 3.6+ 环境
- pip包管理器
- Windows需要Visual C++ Build Tools
- Linux需要相关系统依赖（见下文）

#### 安装步骤

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **运行通用引导脚本**：
   ```
   python install.py
   ```
   
   该脚本将自动检测您的操作系统类型，并执行以下操作：
   - 检测操作系统类型并调用适当的安装脚本
   - 传递命令行参数给平台对应的安装脚本
   - 提供安装过程中的诊断信息和错误处理
   
   安装过程将包括：
   - 创建并激活Python虚拟环境（除非使用--no-venv参数）
   - 安装pip 24.0版本
   - 安装项目依赖
   - 配置系统环境
   - 创建启动脚本

   如需安装可选依赖（增强文本提取功能），可以传递参数：
   ```
   python install.py --with-textract
   ```

3. **启动应用**：
   安装完成后，使用生成的启动脚本启动应用：
   - Windows: 双击`start.bat`
   - Linux/macOS: 执行`./start.sh`

4. **访问应用**：
   打开浏览器，访问 http://localhost:8329

#### 安装脚本的命令行参数

通用安装脚本支持以下命令行参数：

```
--no-venv               不创建虚拟环境，使用系统Python
--venv-dir PATH         指定虚拟环境目录路径（默认: .venv）
--recreate-venv         如果虚拟环境已存在，重新创建
--with-textract         安装textract包（可选但建议，增强文本提取）
--no-system-deps        跳过系统依赖安装（适用于Linux）
```

例如：
```
python install.py --venv-dir custom_env --with-textract
```

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

1. **安装系统依赖**：
   ```
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y python3-dev python3-pip antiword catdoc libreoffice
   
   # CentOS/RHEL
   sudo yum install -y python3-devel python3-pip antiword catdoc libreoffice
   
   # macOS
   brew install antiword
   ```

2. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

3. **运行配置脚本**：
   ```
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```
   
   脚本将自动检测您的系统，安装必要的依赖，并创建启动脚本。
   
   如果需要安装可选依赖，可以使用：
   ```
   ./scripts/setup.sh --with-textract
   ```

4. **启动应用**：
   配置完成后，执行：
   ```
   ./start.sh
   ```

5. **访问应用**：
   打开浏览器，访问 http://localhost:8329

### 手动安装

如果您希望手动安装，请按照以下步骤操作：

#### Windows平台

1. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

2. **创建并激活虚拟环境**（可选）：
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **安装特定版本的pip**：
   ```
   python -m pip install pip==24.0
   ```

4. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```
   
   对于可选的textract库，需要使用特定版本的pip：
   ```
   pip install textract
   ```

5. **运行应用**：
   ```
   python app.py
   ```

#### Linux/macOS平台

1. **安装系统依赖**：
   ```
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y python3-dev python3-pip antiword catdoc libreoffice
   ```

2. **下载项目**：
   ```
   git clone https://github.com/biubush/EssayCorrector.git
   cd EssayCorrector
   ```

3. **创建并激活虚拟环境**（可选）：
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **安装特定版本的pip**：
   ```
   python -m pip install pip==24.0
   ```

5. **安装依赖**：
   ```
   pip install -r requirements.txt
   ```

6. **运行应用**：
   ```
   python app.py
   ```

## 配置说明

系统的主要配置位于`config.py`文件中，您可以根据需要修改以下配置：

### 基础配置

- **服务器配置**：
  ```python
  DEBUG = True  # 是否启用调试模式
  HOST = "0.0.0.0"  # 服务器监听的IP地址，0.0.0.0表示监听所有地址
  PORT = 8329  # 服务器监听的端口号
  ```

- **临时文件夹配置**：
  ```python
  TEMP_FOLDER = os.path.join(tempfile.gettempdir(), "essay_corrector_temp")  # 临时文件存储路径
  ```

- **数据库配置**：
  ```python
  DATABASE_URI = 'sqlite:///tasks.db'  # SQLite数据库连接URI
  ```

### AI配置

- **API密钥和模型**：
  ```python
  AI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxx"  # DeepSeek API密钥
  AI_MODEL = "deepseek-chat"  # 当前使用的AI模型
  ```

- **提示词配置**：
  ```python
  PROMPTS_FILE = 'prompts.txt'  # 提示词文件路径
  ```

### 文件处理配置

- **支持的文件类型**：
  ```python
  ALLOWED_EXTENSIONS = [
      '.doc', '.docx', '.docm', '.dotm',  # Word文档格式
      '.pdf',  # PDF文档格式
      '.txt', '.text',  # 文本文档格式
      '.csv',  # CSV文档格式
      '.xls', '.xlsx', '.xlsm',  # Excel文档格式
      '.md', '.markdown',  # Markdown文档格式
      '.ppt', '.pptx', '.pptm'  # PowerPoint文档格式
  ]
  ```

- **文本处理配置**：
  ```python
  MAX_CHARS_PER_PARAGRAPH = 3000  # 段落合并的最大字符数
  ```

- **定时任务配置**：
  ```python
  CLEANUP_INTERVAL_HOURS = 24  # 临时文件清理的时间间隔（小时）
  ```

### 自定义校对规则

您可以通过修改项目根目录下的`prompts.txt`文件来自定义AI校对规则。系统支持多种格式的提示词文件：

#### 基础规则列表格式
```
1. 校对学术论文中的语法错误，包括标点符号、拼写错误和语法结构问题
2. 修正不恰当的学术表达，使其更加专业和准确
3. 纠正不一致的时态和语态
```

#### 结构化Markdown格式
```markdown
# 基础原则

- **P1-严谨性原则**：仅修正明确错误，不改变原意表述
- **P2-保守性原则**：存疑内容保持原样，不进行推测性修改

## 必须处理

- ZH_语法错误：主谓宾残缺/动宾搭配不当/连词误用
- ZH_标点错误：句子结束无标点/引号括号不匹配/错误使用顿号

## 禁止处理

- STEM表达式：包含希腊字母/数学符号的完整表达式
- 专业术语：各学科专有名词（含大小写特殊格式）
```

#### 包含输出格式指定的复杂格式
```
# 输出格式示例
用这种格式表示修改：[{"theorigin":"原句","corrected":"修正句"}]
```

修改后，系统会在下一次处理文档时自动加载新的规则。您也可以通过修改`config.py`中的`PROMPTS_FILE`配置项来指定不同的提示词文件路径。

### Docker环境变量配置

在Docker环境中，您可以通过环境变量覆盖配置，无需修改源代码：

| 环境变量 | 说明 | 默认值 |
|---------|------|-------|
| `HOST` | 监听地址 | 0.0.0.0 |
| `PORT` | 监听端口 | 8329 |
| `TEMP_FOLDER` | 临时文件夹路径 | /tmp/essay_corrector_temp |
| `AI_API_KEY` | DeepSeek API密钥 | sk-xxxxxxxxxxxxxxxxxxxxxxxxx |
| `AI_MODEL` | 使用的AI模型 | deepseek-chat |
| `PROMPTS_FILE` | 提示词文件路径 | prompts.txt |
| `ALLOWED_EXTENSIONS` | 支持的文件扩展名（逗号分隔） | .doc,.docx,.pdf,... |
| `CLEANUP_INTERVAL_HOURS` | 临时文件清理间隔（小时） | 24 |
| `MAX_CHARS_PER_PARAGRAPH` | 段落合并的最大字符数 | 3000 |
| `PRINT_CONFIG` | 是否在启动时打印配置 | False |
| `DATABASE_URI` | 数据库连接URI | sqlite:///tasks.db |

## 使用指南

### 上传文档

1. 打开浏览器，访问 http://localhost:8329
2. 将文档拖放到上传区域，或点击"选择文件"按钮选择文档
3. 系统接受以下格式的文档：
   - Word文档：.doc, .docx, .docm, .dotm
   - PDF文档：.pdf
   - 文本文档：.txt, .text
   - CSV文档：.csv
   - Excel文档：.xls, .xlsx, .xlsm
   - Markdown文档：.md, .markdown
   - PowerPoint文档：.ppt, .pptx, .pptm

### 查看进度

1. 上传文档后，系统会显示实时进度条
2. 进度信息包括：
   - 已处理百分比
   - 当前段落/总段落数
   - 已用时间
   - 预计剩余时间

### 查看结果

1. 处理完成后，系统会自动显示结果
2. 结果页面包含以下内容：
   - 文档名称和处理时间
   - 修改建议总数
   - 原文与修改后文本的对比列表
   - 每条修改的具体内容和理由（如有）

3. 您可以通过以下方式浏览结果：
   - 使用筛选功能按修改类型查看
   - 点击每条修改查看详情
   - 使用分页导航浏览大量修改

### 查看历史任务

1. 在首页可以看到历史任务列表，包括：
   - 正在运行的任务
   - 已完成的任务
   - 失败的任务
2. 点击任务可以查看详情或结果

## 故障排除

### 常见问题

#### 上传文件失败
- 检查文件格式是否在支持列表中
- 确保文件大小不超过系统限制
- 检查文件是否被其他程序锁定

#### 处理进度停滞
- 复杂文档可能需要更长时间处理
- 检查网络连接是否正常
- 检查DeepSeek API服务是否可用

#### AI服务连接错误
- 确保提供了有效的DeepSeek API密钥
- 检查网络连接是否能访问DeepSeek API
- 确认API请求限制是否超出

#### 文本提取不完整
- PDF文档可能使用了特殊格式或加密保护
- 复杂的Word文档可能包含不支持的元素
- 考虑安装textract增强文本提取功能

### 日志查看

如果遇到问题，可以通过以下方式查看系统日志：

- Docker部署：
  ```bash
  docker logs essay-corrector
  ```

- 本地部署：
  查看控制台输出的日志信息

### 重启服务

如果服务出现异常，可以尝试重启：

- Docker部署：
  ```bash
  docker-compose restart
  ```

- 本地部署：
  停止当前运行的进程，重新执行启动脚本

## 技术栈

- **后端**：
  - Python 3.6+
  - Flask: Web框架
  - Socket.IO: 实时通信
  - SQLAlchemy: 数据库ORM
  - APScheduler: 定时任务

- **前端**：
  - HTML5, CSS3, JavaScript
  - Bootstrap 5: UI框架
  - Socket.IO客户端: 实时通信
  - Chart.js: 数据可视化

- **AI**：
  - DeepSeek API: 自然语言处理
  - 支持多种AI模型: deepseek-chat, deepseek-reasoner等

- **数据处理**：
  - PyPDF2: PDF处理
  - python-docx, docx2txt: Word文档处理
  - openpyxl: Excel处理
  - markdown: Markdown处理
  - python-pptx: PowerPoint处理

- **容器化**：
  - Docker
  - Docker Compose

## 项目结构

```
EssayCorrector/
├── app.py              # 主应用入口，Web服务器
├── config.py           # 配置文件，系统参数设置
├── models.py           # 数据模型，任务存储结构
├── prompts.txt         # AI提示词文件，自定义校对规则
├── requirements.txt    # 依赖列表
├── install.py          # 安装引导脚本
├── Dockerfile          # Docker镜像构建文件
├── docker-compose.yml  # Docker Compose配置
├── docker-entrypoint.sh # Docker容器入口脚本
├── start-docker.bat    # Windows Docker启动脚本
├── start-docker.sh     # Linux/macOS Docker启动脚本
├── .dockerignore       # Docker构建忽略文件
├── core/               # 核心功能模块
│   ├── __init__.py     # 模块初始化
│   ├── AI_solver.py    # AI求解器，与DeepSeek API交互
│   ├── corrector.py    # 纠错器，协调文档处理和AI分析
│   └── data_processor.py # 文档处理器，支持多种格式
├── scripts/            # 安装和配置脚本
│   ├── install.py      # 主安装脚本
│   ├── setup.bat       # Windows安装脚本
│   └── setup.sh        # Linux/macOS安装脚本
├── static/             # 静态资源文件
│   ├── css/            # 样式表
│   ├── js/             # JavaScript脚本
│   └── img/            # 图片资源
├── templates/          # 前端模板
│   └── index.html      # 主页面模板
└── docs/               # 文档目录
    ├── api-docs.md     # API文档
    ├── user-guide.md   # 用户指南
    └── docker-config-guide.md # Docker配置指南
```

## 扩展与开发

### 添加新的文档格式支持

如果需要添加新的文档格式支持，可以按照以下步骤操作：

1. 在`core/data_processor.py`中创建新的处理器类，继承`DocumentProcessor`基类
2. 实现`load_document()`和`process()`方法
3. 在`DocumentProcessorFactory.create_processor()`方法中添加新格式的映射
4. 在`config.py`的`ALLOWED_EXTENSIONS`中添加新的文件扩展名

### 更换AI模型

系统默认使用DeepSeek API，如果需要使用其他AI模型：

1. 在`core/AI_solver.py`中创建新的求解器类
2. 修改`config.py`中的`AI_MODEL`配置
3. 根据需要调整prompts.txt中的提示词

### 自定义用户界面

如果需要自定义用户界面，可以修改以下文件：

1. `templates/index.html`: 主页面模板
2. `static/css/`: 样式表目录
3. `static/js/`: JavaScript脚本目录

## 安全注意事项

1. **API密钥保护**：不要将您的API密钥直接硬编码在配置文件中，建议使用环境变量
2. **网络访问限制**：默认配置监听所有地址(0.0.0.0)，在生产环境中应限制访问地址
3. **文件上传安全**：系统会自动清理临时文件，但仍应定期检查临时目录
4. **数据保护**：敏感文档处理后应及时删除，避免数据泄露风险
5. **Docker安全**：在生产环境中应配置适当的Docker安全策略

## 注意事项

1. **首次运行**：
   - 首次运行时会自动创建数据库和临时文件夹
   - 初始使用时系统会使用默认的API密钥，建议替换为您自己的密钥
   
2. **系统要求**：
   - 默认使用8329端口，请确保该端口未被占用
   - Windows平台需要Microsoft Office组件以获得最佳Word文档处理体验
   - Linux平台需要antiword和catdoc等工具以支持旧版Word文档
   
3. **性能考虑**：
   - 对于大型文档（例如100页以上的PDF），处理时间可能较长
   - 文档内的图片、表格等非文本内容会被忽略
   - 可以通过调整`MAX_CHARS_PER_PARAGRAPH`参数优化性能和准确性的平衡
   
4. **AI限制**：
   - AI模型需要有效的API密钥才能正常使用
   - API调用可能有速率限制，处理大量文档时需要注意
   - AI分析结果仅供参考，建议用户对修改建议进行人工审核

5. **安装依赖**：
   - 安装脚本需要Python 3.6+环境
   - Docker部署需要安装Docker和Docker Compose
   - 某些特殊依赖（如textract）可能需要额外步骤安装

## 贡献与反馈

欢迎对项目进行贡献或提出反馈意见：

1. 提交Issue报告bug或提出功能建议
2. 提交Pull Request贡献代码
3. 分享您的使用体验和改进建议

## 许可证

本项目遵循MIT许可证。

## 联系方式

有任何问题或建议，请通过以下方式联系：

- GitHub: [biubush](https://github.com/biubush)
- 项目Issues: https://github.com/biubush/EssayCorrector/issues

感谢您对本项目的关注和支持！ 