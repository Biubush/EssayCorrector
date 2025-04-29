"""
数据库模型定义模块 - 论文纠错系统

本模块定义了系统所需的数据库模型，使用SQLAlchemy ORM框架。
主要定义了Task模型，用于存储纠错任务的状态和结果。

@author: Biubush
@date: 2025
"""
from sqlalchemy import create_engine, Column, String, JSON, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URI

Base = declarative_base()

class Task(Base):
    """
    任务模型类，用于存储纠错任务的状态和结果
    
    Attributes:
        id (str): 主键，任务的唯一标识符
        filename (str): 上传的文件名
        status (str): 任务状态，可能的值: 'running', 'completed', 'failed'
        result (JSON): 纠错结果，JSON格式
        error_message (str): 任务失败时的错误信息
        created_at (DateTime): 任务创建时间
        completed_at (DateTime): 任务完成时间
        progress (int): 任务进度百分比，取值0-100
        current (int): 当前处理的段落索引
        total (int): 总段落数
        elapsed_time (int): 已耗时（秒）
        estimated_time (int): 预计剩余时间（秒）
        last_updated (DateTime): 最后更新时间
    """
    __tablename__ = 'tasks'
    
    id = Column(String, primary_key=True)
    filename = Column(String)
    status = Column(String)
    result = Column(JSON)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # 进度相关字段
    progress = Column(Integer, default=0)  # 进度百分比 0-100
    current = Column(Integer, default=0)   # 当前处理的段落索引
    total = Column(Integer, default=1)     # 总段落数
    elapsed_time = Column(Integer, default=0)  # 已耗时（秒）
    estimated_time = Column(Integer, default=0)  # 预计剩余时间（秒）
    last_updated = Column(DateTime, default=datetime.utcnow)  # 最后更新时间

# 创建数据库引擎
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session() 