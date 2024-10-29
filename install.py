# post_install.py
import os
from pathlib import Path

def create_pbox_configs():
    # 获取用户主目录
    home_dir = Path.home()

    # 创建 `.pbox` 文件夹路径
    pbox_dir = home_dir / ".pbox"
    pbox_dir.mkdir(exist_ok=True)  # 如果目录已存在，则不报错

    # 创建 API_KEYS 文件
    api_keys_file = pbox_dir / "API_KEYS"
    api_keys_file.touch(exist_ok=True)  # 如果文件已存在，则不报错

if __name__ == "__main__":
    create_pbox_configs()
