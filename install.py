#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Essay Corrector System - Installation Bootstrap Entry

This script is the entry point for the installation bootstrap script,
which calls the main installation script in the scripts directory.

@author: Biubush
"""

import os
import sys
import subprocess
import platform
import tempfile

def main():
    """
    Start the installation bootstrap script
    """
    # Get absolute paths for script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build installation script path with absolute path
    install_script = os.path.join(current_dir, "scripts", "install.py")
    
    # Print diagnostics 
    print(f"[INFO] Current directory: {current_dir}")
    print(f"[INFO] Installation script path: {install_script}")
    
    # Check if installation script exists
    if not os.path.isfile(install_script):
        print(f"[ERROR] Installation script not found: {install_script}")
        print("[INFO] Please ensure you have downloaded the complete project code")
        return 1
    
    # 处理可能的GBK编码问题 (针对中文Windows系统)
    if platform.system() == "Windows" and any('--with-textract' in arg for arg in sys.argv):
        print("[INFO] 检测到--with-textract参数，正在预处理requirements.txt避免GBK编码问题")
        try:
            # 读取原始requirements文件并创建临时文件
            req_path = os.path.join(current_dir, "requirements.txt")
            temp_req_path = os.path.join(tempfile.gettempdir(), "essay_corrector_req.txt")
            
            # 尝试使用UTF-8读取，然后用GBK写入
            with open(req_path, 'r', encoding='utf-8') as src_file:
                content = src_file.read()
                
            with open(temp_req_path, 'w', encoding='gbk') as dest_file:
                dest_file.write(content)
                
            print(f"[INFO] 已创建GBK编码的临时requirements文件: {temp_req_path}")
            print("[INFO] 如果安装依赖时仍遇到编码问题，请尝试手动安装：")
            print("       pip install textract")
        except Exception as e:
            print(f"[WARNING] 预处理requirements.txt时出错: {e}")
            print("[INFO] 如果安装失败，请尝试手动安装textract")
    
    # Call the installation script directly with absolute path, preserving command line arguments
    return subprocess.call([sys.executable, install_script] + sys.argv[1:], cwd=current_dir)

if __name__ == "__main__":
    sys.exit(main()) 