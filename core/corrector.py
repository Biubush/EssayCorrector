"""
文档纠错器模块 - 论文纠错系统

本模块实现了文档纠错的核心逻辑，使用AI模型对文档内容进行语法纠错。
主要功能包括：
- 设置纠错规则
- 处理文档段落
- 请求AI模型进行纠错
- 解析和格式化纠错结果
- 处理进度回调

@author: Biubush
@date: 2025
"""
import json
import re
import time
import os
import concurrent.futures
from core.data_processor import DocumentProcessor
from core.AI_solver import AISolver
from config import PROMPTS_FILE, DEFAULT_PROMPTS

class Corrector:
    """
    Corrector 类用于处理文档并通过 AI 模型进行校正。

    Attributes:
        dataProcessor (DocumentProcessor): 已经实例化的 DocumentProcessor 对象。
        AISolver (AISolver): 已经实例化的 AISolver 对象。
        prompts (str): 用于校正的提示信息。
        progress_callback (callable, optional): 进度回调函数。
    """

    def __init__(self, dataProcessor, AIsolver):
        """
        初始化 Corrector 类的实例。

        Args:
            dataProcessor (DocumentProcessor): 已经实例化的 DocumentProcessor 对象。
            AISolver (AISolver): 已经实例化的 AISolver 对象。
            
        Raises:
            TypeError: 当输入参数类型不正确时抛出
        """
        if not isinstance(dataProcessor, DocumentProcessor):
            raise TypeError("dataProcessor must be an instance of DocumentProcessor")
        if not isinstance(AIsolver, AISolver):
            raise TypeError("AISolver must be an instance of AISolver")
        self.dataProcessor = dataProcessor
        self.AISolver = AIsolver
        
        # 读取提示词文件
        self.user_prompts = self._load_prompts()
        
        # 注意：这里不使用f-string，避免大括号转义问题
        self.prompts = "你即将收到一段文本，请按照以下规则对文本进行严谨的文本校对：\n\n"
        self.prompts += self.user_prompts
        self.prompts += "\n\n在处理完成后，请按照以下格式输出："
        self.prompts += "\n- 如果需要纠正，输出: [{\"theorigin\":\"原句有错\",\"corrected\":\"原句修正后\"}]"
        self.prompts += "\n- 如果无需纠正，输出: []"
        self.prompts += "\n\n在遵守以上规则的前提下，禁止以下行为："
        self.prompts += "\n- 添加解释说明"
        self.prompts += "\n- 回复中使用markdown语法"
        self.prompts += "\n- 在JSON前后添加任何其他文字或说明"
        
        self.progress_callback = None
        
    def _load_prompts(self):
        """
        从文件加载提示词，如果文件不存在则使用默认提示词
        
        Returns:
            str: 提示词内容
        """
        try:
            if os.path.exists(PROMPTS_FILE):
                print(f"正在从文件加载提示词：{PROMPTS_FILE}")
                with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
                    prompts = f.read().strip()
                print(f"成功加载提示词，长度：{len(prompts)}字符")
                return prompts
            else:
                print(f"提示词文件 {PROMPTS_FILE} 不存在，使用默认提示词")
                return DEFAULT_PROMPTS
        except Exception as e:
            print(f"加载提示词文件时出错：{str(e)}，使用默认提示词")
            return DEFAULT_PROMPTS
        
    def set_progress_callback(self, callback):
        """
        设置进度回调函数。

        Args:
            callback (callable): 用于报告进度的回调函数，接收任务ID、进度百分比和预计剩余时间等参数
        """
        self.progress_callback = callback

    def correct(self, task_id=None, max_workers=None):
        """
        执行文档处理和校正操作，使用并行处理提高效率。

        Args:
            task_id (str, optional): 任务ID，用于进度通知。
            max_workers (int, optional): 最大工作线程数，默认为None(由系统决定)。

        Returns:
            list: 包含 AI 校正后的json列表，格式为[{"theorigin":"原句","corrected":"修正句"},...]。
        
        Raises:
            ValueError: 当文档处理失败或响应解析失败时抛出
            RuntimeError: 当AI服务请求失败时抛出
            Exception: 当纠错过程中出现其他异常时抛出
        """
        try:
            # 使用 DocumentProcessor 处理文档
            paragraphs = self.dataProcessor.process()
            
            # 如果处理失败，抛出异常
            if paragraphs is None:
                raise ValueError("文档处理失败，无法进行校正")
            
            corrected_paragraphs = [None] * len(paragraphs)  # 预分配结果列表
            total_paragraphs = len(paragraphs)
            start_time = time.time()
            
            # 用于跟踪已完成的段落数量
            completed_count = 0
            
            # 定义处理单个段落的函数
            def process_paragraph(idx_paragraph):
                idx, paragraph = idx_paragraph
                try:
                    # 为每个段落创建消息
                    messages = [
                        {"role": "system", "content": self.prompts},
                        {"role": "user", "content": paragraph}
                    ]
                    # 使用 AISolver 获取校正后的内容
                    corrected_content = self.AISolver.get_response(messages=messages)
                    
                    # 尝试从响应中提取有效的JSON，改进原有的正则表达式方式
                    try:
                        # 首先打印AI返回的原始内容以便调试
                        print(f"AI原始返回内容: {corrected_content[:150]}...")
                        
                        # 尝试找到响应中最完整的JSON数组
                        json_matches = re.findall(r'\[[\s\S]*?\]', corrected_content)
                        if not json_matches:
                            # 如果没有找到JSON数组，尝试寻找可能的JSON对象
                            json_matches = re.findall(r'\{[\s\S]*?\}', corrected_content)
                        
                        if not json_matches:
                            # 如果仍然没有找到，尝试使用原始的正则但报告详细错误
                            raise ValueError(f"无法从AI响应中提取JSON格式数据: {corrected_content[:150]}...")
                        
                        # 尝试解析每个匹配的JSON片段，直到找到有效的
                        valid_json = None
                        for match in json_matches:
                            try:
                                # 验证这是否是有效的JSON
                                test_json = json.loads(match)
                                # 确认这是一个数组，且包含所需的字段
                                if isinstance(test_json, list) and len(test_json) > 0:
                                    if all(isinstance(item, dict) and 'theorigin' in item and 'corrected' in item for item in test_json):
                                        valid_json = match
                                        break
                            except json.JSONDecodeError:
                                continue
                        
                        if valid_json:
                            corrected_content = valid_json
                        else:
                            # 如果没有找到有效JSON，尝试将整个响应作为JSON解析
                            try:
                                # 清理可能的非JSON前缀/后缀
                                cleaned_content = corrected_content.strip()
                                # 查找第一个[和最后一个]，只保留这中间的内容
                                start_idx = cleaned_content.find('[')
                                end_idx = cleaned_content.rfind(']')
                                
                                if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                                    corrected_content = cleaned_content[start_idx:end_idx+1]
                                    # 测试解析
                                    json.loads(corrected_content)
                                else:
                                    raise ValueError("未找到完整的JSON数组")
                            except Exception as e:
                                print(f"清理JSON时出错: {str(e)}")
                                raise ValueError(f"无法解析AI返回内容为有效JSON: {corrected_content[:150]}...")
                    except Exception as e:
                        print(f"处理AI响应时出错: {str(e)}")
                        raise ValueError(f"处理AI响应失败: {str(e)}")

                    if corrected_content.startswith("请求失败"):
                        raise RuntimeError(f"AI服务请求失败: {corrected_content}")
                    
                    return idx, corrected_content
                except Exception as e:
                    print(f"处理段落 {idx+1} 时出错: {str(e)}")
                    return idx, f"处理错误: {str(e)}"
            
            # 使用线程池并行处理段落
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任务
                future_to_idx = {
                    executor.submit(process_paragraph, (idx, paragraph)): idx 
                    for idx, paragraph in enumerate(paragraphs)
                }
                
                # 处理完成的任务并更新进度
                for future in concurrent.futures.as_completed(future_to_idx):
                    completed_count += 1
                    
                    # 获取处理结果
                    try:
                        idx, result = future.result()
                        corrected_paragraphs[idx] = result
                    except Exception as e:
                        idx = future_to_idx[future]
                        print(f"段落 {idx+1} 处理失败: {str(e)}")
                        corrected_paragraphs[idx] = f"处理失败: {str(e)}"
                    
                    # 计算进度和预计剩余时间
                    progress_percent = round((completed_count / total_paragraphs) * 100, 2)
                    elapsed_time = time.time() - start_time
                    
                    if completed_count > 0:  # 避免除零错误
                        time_per_paragraph = elapsed_time / completed_count
                        remaining_paragraphs = total_paragraphs - completed_count
                        estimated_time_remaining = remaining_paragraphs * time_per_paragraph
                    else:
                        estimated_time_remaining = 0
                    
                    # 如果有进度回调函数，调用它
                    if self.progress_callback and task_id:
                        print(f"发送进度更新 - 任务ID: {task_id}, 进度: {progress_percent}%, 当前: {completed_count}/{total_paragraphs}")
                        self.progress_callback(
                            task_id=task_id,
                            progress=progress_percent,
                            elapsed_time=round(elapsed_time),
                            estimated_time=round(estimated_time_remaining),
                            current=completed_count,
                            total=total_paragraphs
                        )
            
            # 最后一次更新进度为100%
            if self.progress_callback and task_id:
                elapsed_time = time.time() - start_time
                self.progress_callback(
                    task_id=task_id,
                    progress=100,
                    elapsed_time=round(elapsed_time),
                    estimated_time=0,
                    current=total_paragraphs,
                    total=total_paragraphs
                )
            
            # 将校正后的段落转换为 JSON 格式并合并
            all_corrections = []
            for i, paragraph in enumerate(corrected_paragraphs):
                try:
                    # 跳过错误的段落
                    if paragraph is None or isinstance(paragraph, str) and paragraph.startswith("处理"):
                        print(f"跳过处理失败的段落 {i+1}: {paragraph}")
                        continue
                    
                    # 打印当前正在处理的段落内容前100个字符
                    print(f"处理第{i+1}段JSON内容: {paragraph[:100]}...")
                    
                    # 再次尝试清理JSON字符串
                    cleaned_paragraph = paragraph.strip()
                    
                    # 确保是以[开头，]结尾的JSON数组
                    if not (cleaned_paragraph.startswith('[') and cleaned_paragraph.endswith(']')):
                        print(f"格式不正确的JSON: {cleaned_paragraph[:50]}...")
                        # 尝试修复简单的格式问题
                        if not cleaned_paragraph.startswith('['):
                            cleaned_paragraph = '[' + cleaned_paragraph
                        if not cleaned_paragraph.endswith(']'):
                            cleaned_paragraph = cleaned_paragraph + ']'
                    
                    # 尝试解析JSON
                    corrections = json.loads(cleaned_paragraph)
                    
                    # 验证解析后的结果是否符合预期格式
                    if not isinstance(corrections, list):
                        print(f"警告: 解析结果不是数组，而是{type(corrections)}")
                        # 如果不是数组，尝试包装成数组
                        if isinstance(corrections, dict):
                            corrections = [corrections]
                        else:
                            raise ValueError(f"无法将解析结果转换为数组: {corrections}")
                    
                    # 验证每个项是否包含必要的字段
                    valid_items = []
                    for item in corrections:
                        if isinstance(item, dict) and 'theorigin' in item and 'corrected' in item:
                            valid_items.append(item)
                        else:
                            print(f"警告: 跳过不符合格式的项: {item}")
                    
                    if not valid_items:
                        print(f"警告: 第{i+1}段没有有效的纠错项")
                    else:
                        all_corrections.extend(valid_items)
                except json.JSONDecodeError as e:
                    # 不中断整个流程，仅打印警告并跳过这段
                    print(f"警告: 第{i+1}段解析JSON失败: {e}, 内容: {paragraph[:100]}...")
                    print(f"跳过此段并继续处理")
                except Exception as e:
                    # 其他异常也只打印警告
                    print(f"警告: 处理第{i+1}段时出现未知错误: {str(e)}")
            
            # 如果所有段落都处理失败，则抛出异常
            if not all_corrections and corrected_paragraphs:
                raise ValueError("所有段落的JSON解析都失败了，无法获得有效的纠错结果")
            
            print(f"成功提取了{len(all_corrections)}个纠错项")
            return all_corrections
        except Exception as e:
            # 记录异常并向上传播
            print(f"纠错过程中出现异常: {e}")
            raise
