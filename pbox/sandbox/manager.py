# sandbox/manager.py
import uuid
from datetime import datetime, timedelta
import threading

from .sand_box import CodeSandBox

class CodeSandBoxManager:
    def __init__(self):
        self.sandboxes = {}  # 存储kernel_id和其对应的sandbox实例
        self.api_key_to_kernel_ids = {}  # 新增：存储API_KEY与kernel_id的映射

    def create_sandbox(self, api_key):
        try:
            kernel_id = str(uuid.uuid4())
            sandbox = CodeSandBox()
            self.sandboxes[kernel_id] = sandbox

            # 新增：将kernel_id添加到对应API_KEY的列表中
            if api_key not in self.api_key_to_kernel_ids:
                self.api_key_to_kernel_ids[api_key] = []
            self.api_key_to_kernel_ids[api_key].append(kernel_id)

            # 设置24小时后自动关闭Kernel
            timer = threading.Timer(6*3600, self.close_sandbox, [api_key, kernel_id])
            timer.daemon = True
            timer.start()

            return kernel_id
        except Exception as e:
            print(str(e))
            return None
    
    
    def kernels(self, api_key):
        try:
            kernel_ids = self.api_key_to_kernel_ids.get(api_key, [])
            if not kernel_ids:  # 如果列表为空
                return f"No kernels found for {api_key}. Please create a kernel first."
            return kernel_ids
        except Exception as e:
            print(str(e))
            return None
    

    def close_sandbox(self, api_key, kernel_id):
        try:
            if kernel_id in self.sandboxes:
                sandbox = self.sandboxes.pop(kernel_id, None)
                if sandbox:
                    sandbox.close()
                    self.api_key_to_kernel_ids[api_key].remove(kernel_id)
                    if not self.api_key_to_kernel_ids[api_key]:
                        _ = self.api_key_to_kernel_ids.pop(api_key, None)
                return True
            else:
                return f"No kernels found for {api_key}. Please create a kernel first."
        except Exception as e:
            print(str(e))
            return False
                

    def execute_code(self, api_key, kernel_id, code):
        try:
            if kernel_id in self.sandboxes:
                sandbox = self.sandboxes[kernel_id]
                return sandbox.execute_code(code)
            else:
                return f"No kernels found for {api_key}. Please create a kernel first."
        except Exception as e:
            print(str(e))
            return False