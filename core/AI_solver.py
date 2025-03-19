"""
AI求解器模块 - 论文纠错系统

本模块实现了与DeepSeek API的交互，提供AI语言模型服务。
主要功能包括：
- 初始化API连接
- 构建API请求数据
- 发送请求并处理响应
- 错误处理

@author: Biubush
@date: 2025
"""
import requests

class AISolver:
    """
    用于与 DeepSeek API 进行交互的类。

    Attributes:
        api_key (str): 用于认证的 API Key。
        model (str): 使用的模型名称。
        url (str): API端点URL。
        headers (dict): HTTP请求头信息。
    """

    def __init__(self, api_key, model="deepseek-reasoner"):
        """
        初始化 AISolver 类的实例。

        Args:
            api_key (str): 用于认证的 API Key。
            model (str): 使用的模型名称，默认为 "deepseek-reasoner"。
            
        Raises:
            TypeError: 当输入参数类型不正确时抛出
        """
        if not isinstance(api_key, str):
            raise TypeError("api_key must be a string")
        if not isinstance(model, str):
            raise TypeError("model must be a string")
        self.api_key = api_key
        self.model = model
        self.url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_request_data(self, messages, stream=False):
        """
        创建请求数据。

        Args:
            messages (list): 消息列表，每个消息是一个字典，包含角色和内容。
            stream (bool): 是否使用流式传输，默认为 False。

        Returns:
            dict: 请求数据字典。
        """
        return {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

    def get_response(self, messages, stream=False):
        """
        发送请求并获取响应。

        Args:
            messages (list): 消息列表。
            stream (bool): 是否使用流式传输。

        Returns:
            str: 返回的消息内容。
        
        Raises:
            requests.RequestException: 当网络请求失败时抛出
            ValueError: 当API返回非200状态码或响应格式不正确时抛出
            Exception: 其他未预期的异常
        """
        try:
            data = self.create_request_data(messages, stream)
            response = requests.post(self.url, headers=self.headers, json=data)

            if response.status_code == 200:
                result = response.json()
                if 'choices' not in result or not result['choices'] or 'message' not in result['choices'][0]:
                    raise ValueError(f"API响应格式不正确: {result}")
                return result['choices'][0]['message']['content']
            else:
                error_msg = f"请求失败，错误码：{response.status_code}"
                if response.text:
                    try:
                        error_detail = response.json()
                        error_msg += f", 错误详情: {error_detail}"
                    except:
                        error_msg += f", 响应内容: {response.text[:200]}"
                raise ValueError(error_msg)
        except requests.RequestException as e:
            # 网络请求异常
            error_msg = f"网络请求异常: {str(e)}"
            print(error_msg)
            raise
        except ValueError as e:
            # API响应异常
            print(f"API响应异常: {str(e)}")
            raise
        except Exception as e:
            # 其他未预期的异常
            error_msg = f"AI调用过程中出现未预期的异常: {str(e)}"
            print(error_msg)
            raise

if __name__ == "__main__":
    # 示例代码：演示AI求解器的使用方法
    api_key = "sk-xxxxxxxxxxxxxxxxxxxxxx"  # 替换为你的API密钥
    solver = AISolver(api_key)
    messages = [
        {"role": "system", "content": "你是一个专业的助手"},
        {"role": "user", "content": "你是谁？"}
    ]
    response_content = solver.get_response(messages)
    print(response_content)