"""
配置文件模块 - 论文纠错系统

本模块包含了系统的所有配置参数，包括：
- 应用服务器配置（调试模式、主机、端口）
- 临时文件夹配置
- 数据库连接配置
- AI模型配置
- 文件上传配置
- 定时任务配置
- 文本处理配置

@author: Biubush
@date: 2025
"""
import os
import tempfile

# 应用配置
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')  # 是否启用调试模式
HOST = os.environ.get('HOST', "0.0.0.0")  # 服务器监听的IP地址，0.0.0.0表示监听所有地址
PORT = int(os.environ.get('PORT', 8329))  # 服务器监听的端口号

# 临时文件夹配置
TEMP_FOLDER = os.environ.get('TEMP_FOLDER', os.path.join(tempfile.gettempdir(), "essay_corrector_temp"))  # 临时文件存储路径

# 数据库配置
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///tasks.db')  # SQLite数据库连接URI

# AI配置
AI_API_KEY = os.environ.get('AI_API_KEY', "sk-xxxxxxxxxxxxxxxxxxxxxxxxx")  # AI API密钥
# AI_MODEL = "deepseek-reasoner"  # 备选AI模型
AI_MODEL = os.environ.get('AI_MODEL', "deepseek-chat")  # 当前使用的AI模型

# AI提示词配置
PROMPTS_FILE = os.environ.get('PROMPTS_FILE', 'prompts.txt')  # 提示词文件路径
# 默认提示词，当提示词文件不存在时使用
DEFAULT_PROMPTS = """
1. 校对学术论文中的语法错误，包括标点符号、拼写错误和语法结构问题
2. 修正不恰当的学术表达，使其更加专业和准确
3. 纠正不一致的时态和语态
4. 调整不连贯或不流畅的句子
5. 修改不准确或模糊的表述
6. 纠正冗余或重复的内容
"""

# 文件上传配置
DEFAULT_EXTENSIONS = [
    # Word文档格式
    '.doc', '.docx', '.docm', '.dotm',
    # PDF文档格式
    '.pdf',
    # 文本文档格式
    '.txt', '.text',
    # CSV文档格式
    '.csv',
    # Excel文档格式
    '.xls', '.xlsx', '.xlsm',
    # Markdown文档格式
    '.md', '.markdown',
    # PowerPoint文档格式
    '.ppt', '.pptx', '.pptm'
]

# 如果在环境变量中定义了ALLOWED_EXTENSIONS，则使用环境变量中的配置
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS', ','.join(DEFAULT_EXTENSIONS)).split(',')
if isinstance(ALLOWED_EXTENSIONS, str):
    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS.split(',')

# 定时任务配置
CLEANUP_INTERVAL_HOURS = int(os.environ.get('CLEANUP_INTERVAL_HOURS', 24))  # 临时文件清理的时间间隔（小时）

# 文本处理配置
MAX_CHARS_PER_PARAGRAPH = int(os.environ.get('MAX_CHARS_PER_PARAGRAPH', 3000))  # 段落合并的最大字符数 

# 调试信息
if os.environ.get('PRINT_CONFIG', 'False').lower() in ('true', '1', 't'):
    print("当前配置:")
    print(f"DEBUG: {DEBUG}")
    print(f"HOST: {HOST}")
    print(f"PORT: {PORT}")
    print(f"TEMP_FOLDER: {TEMP_FOLDER}")
    print(f"DATABASE_URI: {DATABASE_URI}")
    print(f"AI_API_KEY: {'*' * 10}")
    print(f"AI_MODEL: {AI_MODEL}")
    print(f"PROMPTS_FILE: {PROMPTS_FILE}")
    print(f"ALLOWED_EXTENSIONS: {ALLOWED_EXTENSIONS}")
    print(f"CLEANUP_INTERVAL_HOURS: {CLEANUP_INTERVAL_HOURS}")
    print(f"MAX_CHARS_PER_PARAGRAPH: {MAX_CHARS_PER_PARAGRAPH}") 