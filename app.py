"""
Flask应用主文件 - 论文纠错系统

本文件是论文纠错系统的Web应用主入口，基于Flask和Socket.IO构建。
系统功能包括：
1. 上传文档（支持多种格式如Word, PDF, TXT等）进行语法校对
2. 通过WebSocket实时向前端发送处理进度
3. 使用多线程处理文档纠错任务
4. 持久化存储任务状态到数据库
5. 定期清理临时文件

@author: Biubush
@date: 2025
"""
from flask import Flask, render_template, request, jsonify
import os
import shutil
from core.corrector import Corrector
from core import DocumentProcessorFactory
from core import AISolver
import uuid
import threading
import traceback
from models import Task, session
from datetime import datetime
from flask_socketio import SocketIO
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from config import (
    DEBUG, HOST, PORT, TEMP_FOLDER, 
    AI_API_KEY, AI_MODEL, ALLOWED_EXTENSIONS, 
    CLEANUP_INTERVAL_HOURS
)

app = Flask(__name__)
# 使用配置文件中的临时目录
app.config['TEMP_FOLDER'] = TEMP_FOLDER
# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# 确保临时文件夹存在
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# 进度回调函数，用于通过SocketIO向前端发送进度信息
def progress_callback(task_id, progress, elapsed_time, estimated_time, current, total):
    """
    通过 SocketIO 发送进度信息到前端并将进度更新到数据库
    
    Args:
        task_id (str): 任务ID
        progress (float): 进度百分比 (0-100)
        elapsed_time (int): 已耗时（秒）
        estimated_time (int): 预计剩余时间（秒）
        current (int): 当前处理的段落索引
        total (int): 总段落数
    
    Returns:
        None
    """
    # 格式化时间为分钟:秒
    def format_time(seconds):
        """
        将秒数转换为'分:秒'格式
        
        Args:
            seconds (int): 秒数
            
        Returns:
            str: 格式化后的时间字符串，如'5分30秒'
        """
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}分{seconds}秒"
    
    try:
        # 1. 更新数据库中的任务进度信息
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            task.progress = int(progress) if progress is not None else 0
            task.current = current if current is not None else 0
            task.total = total if total is not None else 1
            task.elapsed_time = elapsed_time if elapsed_time is not None else 0
            task.estimated_time = estimated_time if estimated_time is not None else 0
            task.last_updated = datetime.utcnow()
            session.commit()
            print(f"[任务 {task_id}] 进度已更新到数据库: {progress}%, {current}/{total}")
        else:
            print(f"[任务 {task_id}] 警告: 任务不存在，无法更新进度")
    except Exception as e:
        print(f"[任务 {task_id}] 更新进度到数据库时出错: {str(e)}")
    
    # 2. 向前端发送进度更新
    progress_data = {
        'task_id': task_id,
        'progress': progress,
        'elapsed_time': format_time(elapsed_time),
        'estimated_time': format_time(estimated_time),
        'current': current,
        'total': total
    }
    
    print(f"发送进度更新: {progress_data}")
    socketio.emit('task_progress', progress_data)

# Socket.IO连接事件处理
@socketio.on('connect')
def handle_connect():
    """
    当客户端连接到Socket.IO服务器时，发送当前所有进行中任务的状态和进度
    
    该函数会在新客户端连接时自动触发，并向其发送所有运行中任务的信息
    
    Returns:
        None
    """
    print(f"新客户端连接: {request.sid}")
    
    # 获取所有运行中的任务
    running_tasks = session.query(Task).filter_by(status='running').all()
    
    if running_tasks:
        print(f"向新客户端 {request.sid} 发送 {len(running_tasks)} 个正在运行的任务状态")
        
        # 向新连接的客户端发送每个运行中任务的最新进度
        for task in running_tasks:
            # 1. 发送任务基本信息
            task_info = {
                'task_id': task.id,
                'filename': task.filename,
                'created_at': task.created_at.isoformat(),
                'status': 'running'
            }
            socketio.emit('task_info', task_info, to=request.sid)
            
            # 2. 发送任务进度信息
            # 格式化时间为分钟:秒
            def format_time(seconds):
                """
                将秒数转换为'分:秒'格式
                
                Args:
                    seconds (int): 秒数
                    
                Returns:
                    str: 格式化后的时间字符串，如'5分30秒'
                """
                if seconds is None:
                    return "0分0秒"
                minutes = seconds // 60
                seconds = seconds % 60
                return f"{minutes}分{seconds}秒"
            
            progress_data = {
                'task_id': task.id,
                'progress': task.progress if task.progress is not None else 0,
                'elapsed_time': format_time(task.elapsed_time),
                'estimated_time': format_time(task.estimated_time),
                'current': task.current if task.current is not None else 0,
                'total': task.total if task.total is not None else 1
            }
            socketio.emit('task_progress', progress_data, to=request.sid)

def process_task(task_id, file_path):
    """
    在后台线程中处理文档纠错任务
    
    该函数创建文档处理器和AI求解器，执行纠错操作，并更新任务状态
    
    Args:
        task_id (str): 任务ID
        file_path (str): 需要处理的文件路径
        
    Returns:
        None
    """
    try:
        # 使用工厂创建适合的文档处理器
        try:
            print(f"[任务 {task_id}] 开始处理文件: {file_path}")
            data_processor = DocumentProcessorFactory.create_processor(file_path)
            if data_processor is None:
                raise ValueError(f"不支持的文件类型: {os.path.splitext(file_path)[1]}")
            print(f"[任务 {task_id}] 成功创建文档处理器: {type(data_processor).__name__}")
        except Exception as e:
            print(f"[任务 {task_id}] 创建文档处理器失败: {str(e)}")
            raise ValueError(f"创建文档处理器失败: {str(e)}")
            
        # 创建AI求解器
        try:
            print(f"[任务 {task_id}] 正在初始化AI求解器")
            ai_solver = AISolver(AI_API_KEY, AI_MODEL)
            print(f"[任务 {task_id}] 成功创建AI求解器: {AI_MODEL}")
        except Exception as e:
            print(f"[任务 {task_id}] 创建AI求解器失败: {str(e)}")
            raise ValueError(f"创建AI求解器失败: {str(e)}")
        
        # 创建纠错器并执行纠错
        try:
            print(f"[任务 {task_id}] 开始创建纠错器")
            corrector = Corrector(data_processor, ai_solver)
            # 设置进度回调
            corrector.set_progress_callback(progress_callback)
            # 执行纠错，传入任务ID以便进度回调
            print(f"[任务 {task_id}] 开始执行文档纠错")
            output_json = corrector.correct(task_id=task_id)
            print(f"[任务 {task_id}] 文档纠错完成，检测到 {len(output_json)} 个纠错项")
        except Exception as e:
            print(f"[任务 {task_id}] 执行纠错过程失败: {str(e)}")
            print(f"[任务 {task_id}] 错误详情: {traceback.format_exc()}")
            raise ValueError(f"执行纠错过程失败: {str(e)}")
        
        # 更新任务状态
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            print(f"[任务 {task_id}] 任务完成，正在更新数据库状态")
            task.status = 'completed'
            task.result = output_json
            task.completed_at = datetime.utcnow()
            session.commit()
            print(f"[任务 {task_id}] 数据库状态更新完成")
            
            # 通知前端任务已完成
            print(f"[任务 {task_id}] 发送任务完成通知到前端")
            socketio.emit('task_complete', {
                'task_id': task_id,
                'status': 'completed',
                'filename': task.filename,
                'created_at': task.created_at.isoformat(),
                'completed_at': task.completed_at.isoformat()
            })
    except Exception as e:
        print(f"[任务 {task_id}] 处理任务时出错: {e}")
        # 更新任务状态为失败
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            print(f"[任务 {task_id}] 标记任务为失败")
            task.status = 'failed'
            task.error_message = str(e)
            task.result = {"error": str(e), "error_type": type(e).__name__}
            task.completed_at = datetime.utcnow()
            session.commit()
            
            # 通知前端任务失败
            print(f"[任务 {task_id}] 发送任务失败通知到前端")
            socketio.emit('task_error', {
                'task_id': task_id,
                'error': str(e),
                'error_type': type(e).__name__,
                'filename': task.filename,
                'created_at': task.created_at.isoformat(),
                'completed_at': task.completed_at.isoformat()
            })
    finally:
        # 无论成功还是失败，都清理临时文件
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[任务 {task_id}] 已删除临时文件: {file_path}")
        except Exception as e:
            print(f"[任务 {task_id}] 删除临时文件失败: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    首页路由处理函数
    
    GET请求：返回上传页面
    POST请求：处理文件上传，创建纠错任务
    
    Returns:
        flask.Response: GET请求返回渲染后的HTML页面
                        POST请求成功返回JSON格式的任务ID和状态
                        POST请求失败返回错误信息
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "没有上传文件"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 检查文件扩展名
        _, file_extension = os.path.splitext(file.filename)
        file_extension = file_extension.lower()
        
        if file_extension not in ALLOWED_EXTENSIONS:
            supported_formats = ", ".join(ALLOWED_EXTENSIONS)
            return jsonify({"error": f"不支持的文件类型 '{file_extension}'。支持的格式有: {supported_formats}"}), 400
            
        if file:
            # 生成任务ID
            task_id = str(uuid.uuid4())
            # 使用任务ID和原始文件后缀保存文件到临时目录
            file_path = os.path.join(app.config['TEMP_FOLDER'], f"{task_id}{file_extension}")
            file.save(file_path)
            
            # 创建任务记录，包含初始进度信息
            new_task = Task(
                id=task_id, 
                filename=file.filename, 
                status='running', 
                result=None,
                progress=0,
                current=0,
                total=1,
                elapsed_time=0,
                estimated_time=0,
                last_updated=datetime.utcnow()
            )
            session.add(new_task)
            session.commit()
            
            # 发送初始进度信息（0%）
            progress_callback(
                task_id=task_id,
                progress=0,
                elapsed_time=0,
                estimated_time=0,
                current=0,
                total=1  # 临时设置为1，后续会更新真实总数
            )
            
            # 启动后台线程处理任务
            threading.Thread(target=process_task, args=(task_id, file_path)).start()
            
            return jsonify({"task_id": task_id, "status": "running"})
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    获取所有任务状态的API端点
    
    返回三类任务：正在运行、已完成和失败的任务
    
    Returns:
        flask.Response: JSON格式的任务列表，按状态分类
    """
    running_tasks = session.query(Task).filter_by(status='running').all()
    completed_tasks = session.query(Task).filter_by(status='completed').all()
    failed_tasks = session.query(Task).filter_by(status='failed').all()
    
    # 格式化时间为分钟:秒
    def format_time(seconds):
        """
        将秒数转换为'分:秒'格式
        
        Args:
            seconds (int): 秒数
            
        Returns:
            str: 格式化后的时间字符串，如'5分30秒'
        """
        if seconds is None:
            return "0分0秒"
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}分{seconds}秒"
    
    # 构建运行中任务的字典，包含进度信息
    running_tasks_dict = {}
    for task in running_tasks:
        running_tasks_dict[task.id] = {
            "filename": task.filename, 
            "created_at": task.created_at,
            "progress": task.progress if task.progress is not None else 0,
            "current": task.current if task.current is not None else 0,
            "total": task.total if task.total is not None else 1,
            "elapsed_time": format_time(task.elapsed_time),
            "estimated_time": format_time(task.estimated_time),
            "last_updated": task.last_updated
        }
    
    return jsonify({
        "running": running_tasks_dict,
        "completed": {task.id: {"filename": task.filename, "created_at": task.created_at, "completed_at": task.completed_at} for task in completed_tasks},
        "failed": {task.id: {"filename": task.filename, "created_at": task.created_at, "completed_at": task.completed_at} for task in failed_tasks}
    })

@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    获取特定任务详情的API端点
    
    Args:
        task_id (str): URL参数中的任务ID
    
    Returns:
        flask.Response: JSON格式的任务详情或错误信息
    """
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        response = {"status": task.status}
        if task.status == 'failed':
            # 优先使用error_message字段
            if task.error_message:
                response["error"] = task.error_message
            # 兼容旧格式，从result中获取错误信息
            elif task.result and isinstance(task.result, dict):
                response["error"] = task.result.get("error", "未知错误")
                response["error_type"] = task.result.get("error_type", "未知错误类型")
            else:
                response["error"] = "未知错误"
                response["error_type"] = "未知错误类型"
        else:
            response["result"] = task.result
        return jsonify(response)
    return jsonify({"error": "Task not found"}), 404

def cleanup_temp_files():
    """
    定期清理临时文件夹中的文件
    
    该函数会被定时任务调度器调用，清理临时目录中的所有文件和文件夹
    
    Returns:
        None
    """
    try:
        # 清理临时目录中的所有文件
        for filename in os.listdir(app.config['TEMP_FOLDER']):
            file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'清理临时文件失败: {e}')
    except Exception as e:
        print(f'清理临时文件夹失败: {e}')

# 启动定时清理任务
scheduler = BackgroundScheduler()
scheduler.add_job(func=cleanup_temp_files, trigger="interval", hours=CLEANUP_INTERVAL_HOURS)
scheduler.start()

# 确保应用退出时关闭调度器
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    socketio.run(app, debug=DEBUG, host=HOST, port=PORT, allow_unsafe_werkzeug=True)