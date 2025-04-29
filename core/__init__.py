"""
核心模块包初始化文件 - 论文纠错系统

本文件定义了核心模块包的导出内容，包括：
- 文档处理器类（支持多种文档格式）
- 文档处理器工厂类
- AI求解器类
- 纠错器类

@author: Biubush
@date: 2025
"""
from core.data_processor import (
    DocumentProcessor,
    WordDocumentProcessor,
    PDFDocumentProcessor,
    TXTDocumentProcessor,
    CSVDocumentProcessor,
    ExcelDocumentProcessor,
    MarkdownDocumentProcessor,
    PowerPointDocumentProcessor,
    DocumentProcessorFactory
)
from core.AI_solver import AISolver
from core.corrector import Corrector