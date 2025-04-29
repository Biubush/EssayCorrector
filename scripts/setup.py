#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Environment Setup Script - Essay Corrector System

This script automatically detects the operating system type and installs the appropriate dependencies.
Supports Windows and Linux/macOS platforms.

@author: Biubush
"""

import os
import sys
import platform
import subprocess
import shutil
import tempfile
import venv
import argparse
from pathlib import Path

# Get absolute paths for script directory and project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Ensure working directory is project root
os.chdir(PROJECT_ROOT)

# Print diagnostic information
print(f"[INFO] Script directory: {SCRIPT_DIR}")
print(f"[INFO] Project root: {PROJECT_ROOT}")
print(f"[INFO] Current working directory: {os.getcwd()}")

def print_step(message):
    """Print formatted step information"""
    print("\n" + "=" * 60)
    print(f">>> {message}")
    print("=" * 60)


def print_info(message):
    """Print information message"""
    print(f"[INFO] {message}")


def print_success(message):
    """Print success message"""
    print(f"[SUCCESS] {message}")


def print_warning(message):
    """Print warning message"""
    print(f"[WARNING] {message}")


def print_error(message):
    """Print error message"""
    print(f"[ERROR] {message}")


def run_command(command, shell=True, check=True, capture_output=False):
    """
    Run command and return result
    
    Args:
        command: Command to run
        shell: Whether to use shell
        check: Whether to check return code
        capture_output: Whether to capture output
    
    Returns:
        subprocess.CompletedProcess: Command execution result
        
    Raises:
        subprocess.CalledProcessError: When command execution fails and check=True
    """
    try:
        return subprocess.run(
            command,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True,
            encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        if not check:
            return e
        print_error(f"Command execution failed: {e}")
        print_info(f"Failed command: {command}")
        raise


def is_command_available(command):
    """
    Check if command is available in the system
    
    Args:
        command: Command to check
        
    Returns:
        bool: True if command is available, False otherwise
    """
    try:
        if platform.system() == "Windows":
            result = subprocess.run(f"where {command}", shell=True, check=False, capture_output=True)
        else:
            result = subprocess.run(f"which {command}", shell=True, check=False, capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def detect_system():
    """
    Detect system type and distribution
    
    Returns:
        tuple: (system_type, distribution_name)
            system_type: 'Windows', 'Linux', 'Darwin'
            distribution_name: Linux distribution name (e.g., 'Ubuntu', 'CentOS')
    """
    system_type = platform.system()
    distro = ""
    
    if system_type == "Linux":
        # Try to detect Linux distribution
        try:
            import distro as distro_module
            distro = distro_module.id()
            print_info(f"Detected Linux distribution: {distro}")
        except ImportError:
            # If distro module is not available, try using os-release file
            try:
                with open("/etc/os-release", "r") as f:
                    content = f.read()
                    if "ID=" in content:
                        distro = content.split("ID=")[1].split("\n")[0].strip('"').strip("'")
                print_info(f"Detected Linux distribution: {distro}")
            except:
                print_warning("Could not detect Linux distribution. System dependencies may not be installed correctly.")
    
    return system_type, distro


def setup_virtual_env(args):
    """
    Set up virtual environment
    
    Args:
        args: Command line arguments
        
    Returns:
        str: Path to Python executable in virtual environment
    """
    venv_dir = args.venv_dir
    recreate_venv = args.recreate_venv
    no_venv = args.no_venv
    
    if no_venv:
        print_info("Skipping virtual environment creation (--no-venv)")
        return sys.executable
    
    # Use absolute path for virtual environment
    venv_path = os.path.join(PROJECT_ROOT, venv_dir)
    print_info(f"Virtual environment path: {venv_path}")
    
    # Check if virtual environment already exists
    if os.path.exists(venv_path):
        if recreate_venv:
            print_info(f"Recreating virtual environment at {venv_path}")
            shutil.rmtree(venv_path)
        else:
            print_info(f"Using existing virtual environment at {venv_path}")
            # Return path to Python executable in virtual environment
            if platform.system() == "Windows":
                python_path = os.path.join(venv_path, "Scripts", "python.exe")
            else:
                python_path = os.path.join(venv_path, "bin", "python")
            
            if os.path.exists(python_path):
                print_success(f"Found Python at {python_path}")
                return python_path
            else:
                print_warning(f"Could not find Python executable in virtual environment. Recreating.")
                shutil.rmtree(venv_path)
    
    print_step("Creating virtual environment")
    try:
        venv.create(venv_path, with_pip=True)
        print_success(f"Virtual environment created at {venv_path}")
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        print_info("Using system Python instead")
        return sys.executable
    
    # Get path to Python executable in virtual environment
    if platform.system() == "Windows":
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_path, "bin", "python")
    
    return python_path


def install_python_dependencies(python_path, requirements_file="requirements.txt", args=None):
    """
    Install Python dependencies from requirements file
    
    Args:
        python_path: Path to Python executable
        requirements_file: Path to requirements file
        args: Command line arguments
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    print_step("Installing Python dependencies")
    
    # Use absolute path for requirements file
    full_requirements_path = os.path.join(PROJECT_ROOT, requirements_file)
    print_info(f"Requirements file path: {full_requirements_path}")
    
    if not os.path.exists(full_requirements_path):
        print_error(f"Requirements file not found: {full_requirements_path}")
        return False
    
    # Install specific pip version (24.0) instead of upgrading to latest
    print_info("Installing pip version 24.0")
    try:
        run_command(f'"{python_path}" -m pip install pip==24.0')
    except Exception as e:
        print_warning(f"Failed to install pip version 24.0: {e}")
    
    # Install requirements
    print_info(f"Installing requirements from {requirements_file}")
    try:
        with_textract = args.with_textract if args and hasattr(args, 'with_textract') else False
        
        # 创建临时requirements文件，使用GBK编码
        temp_req_path = os.path.join(tempfile.gettempdir(), "essay_corrector_requirements.txt")
        print_info(f"Creating temporary requirements file with GBK encoding: {temp_req_path}")
        
        try:
            # 读取原始requirements文件（UTF-8编码）
            with open(full_requirements_path, 'r', encoding='utf-8') as src_file:
                content = src_file.read()
                
            # 写入临时文件（GBK编码）
            with open(temp_req_path, 'w', encoding='gbk') as dest_file:
                dest_file.write(content)
                
            # 使用临时文件安装依赖
            if with_textract:
                print_info("Including optional 'textract' package (--with-textract)")
                run_command(f'"{python_path}" -m pip install -r "{temp_req_path}" textract')
            else:
                run_command(f'"{python_path}" -m pip install -r "{temp_req_path}"')
                
            # 安装完成后删除临时文件
            try:
                os.remove(temp_req_path)
                print_info(f"Temporary requirements file removed")
            except Exception as e:
                print_warning(f"Could not remove temporary requirements file: {e}")
                
        except UnicodeDecodeError as ude:
            print_warning(f"Encountered encoding issue: {ude}")
            print_info("Attempting direct installation with encoding parameter")
            
            # 直接安装，尝试使用pip的--no-cache-dir选项
            if with_textract:
                run_command(f'"{python_path}" -m pip install --no-cache-dir -r "{full_requirements_path}" textract')
            else:
                run_command(f'"{python_path}" -m pip install --no-cache-dir -r "{full_requirements_path}"')
        
        print_success("Python dependencies installed successfully")
        return True
    except Exception as e:
        print_error(f"Failed to install Python dependencies: {e}")
        return False


def install_system_dependencies(system_type, distro=""):
    """
    Install system dependencies based on platform
    
    Args:
        system_type: System type ('Windows', 'Linux', 'Darwin')
        distro: Linux distribution name
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    print_step("Installing system dependencies")
    
    if system_type == "Windows":
        print_info("No additional system dependencies required for Windows")
        return True
    
    elif system_type == "Linux":
        if not distro:
            print_warning("Could not detect Linux distribution. Skipping system dependencies installation.")
            print_info("You may need to install the following packages manually:")
            print("  - antiword: For Word document processing")
            print("  - poppler-utils: For PDF processing")
            print("  - libxml2-dev libxslt1-dev: For XML processing")
            return True
        
        try:
            if distro.lower() in ["ubuntu", "debian", "linuxmint", "pop"]:
                # Ubuntu/Debian-based
                print_info("Installing dependencies for Ubuntu/Debian")
                commands = [
                    "apt-get update",
                    "apt-get install -y antiword poppler-utils libxml2-dev libxslt1-dev"
                ]
                for cmd in commands:
                    print_info(f"Running: sudo {cmd}")
                    run_command(f"sudo {cmd}")
                
            elif distro.lower() in ["centos", "rhel", "fedora"]:
                # RHEL-based
                print_info("Installing dependencies for CentOS/RHEL/Fedora")
                commands = [
                    "yum install -y antiword poppler-utils libxml2-devel libxslt-devel"
                ]
                for cmd in commands:
                    print_info(f"Running: sudo {cmd}")
                    run_command(f"sudo {cmd}")
                
            elif distro.lower() in ["arch", "manjaro"]:
                # Arch-based
                print_info("Installing dependencies for Arch Linux")
                commands = [
                    "pacman -Sy --noconfirm antiword poppler libxml2 libxslt"
                ]
                for cmd in commands:
                    print_info(f"Running: sudo {cmd}")
                    run_command(f"sudo {cmd}")
                
            else:
                print_warning(f"Unsupported Linux distribution: {distro}")
                print_info("You may need to install the following packages manually:")
                print("  - antiword: For Word document processing")
                print("  - poppler-utils: For PDF processing")
                print("  - libxml2-dev libxslt1-dev: For XML processing")
                return True
            
            print_success("System dependencies installed successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to install system dependencies: {e}")
            print_warning("You may need to install the following packages manually:")
            print("  - antiword: For Word document processing")
            print("  - poppler-utils: For PDF processing")
            print("  - libxml2-dev libxslt1-dev: For XML processing")
            return False
    
    elif system_type == "Darwin":  # macOS
        try:
            if not is_command_available("brew"):
                print_warning("Homebrew not found. Please install Homebrew first:")
                print("  /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                print_info("Then install the following packages manually:")
                print("  brew install antiword poppler libxml2 libxslt")
                return True
            
            print_info("Installing dependencies using Homebrew")
            commands = [
                "brew install antiword poppler libxml2 libxslt"
            ]
            for cmd in commands:
                print_info(f"Running: {cmd}")
                run_command(cmd)
            
            print_success("System dependencies installed successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to install system dependencies: {e}")
            print_warning("You may need to install the following packages manually:")
            print("  brew install antiword poppler libxml2 libxslt")
            return False
    
    else:
        print_warning(f"Unsupported system type for system dependencies: {system_type}")
        return False


def create_startup_script(system_type, python_path):
    """
    Create startup script for running the application
    
    Args:
        system_type: System type ('Windows', 'Linux', 'Darwin')
        python_path: Path to Python executable
        
    Returns:
        bool: True if script creation was successful, False otherwise
    """
    print_step("Creating startup script")
    
    try:
        # Create startup script in project root with absolute paths
        start_script_path = os.path.join(PROJECT_ROOT, "start.bat" if system_type == "Windows" else "start.sh")
        app_script_path = os.path.join(PROJECT_ROOT, "app.py")
        
        print_info(f"Creating startup script at: {start_script_path}")
        print_info(f"Application script path: {app_script_path}")
        
        if system_type == "Windows":
            # Create batch file for Windows
            with open(start_script_path, "w", encoding="utf-8") as f:
                f.write('@echo off\n')
                f.write('chcp 65001 >nul\n')  # Set UTF-8 code page
                f.write('echo Starting Essay Corrector System...\n')
                f.write(f'cd /d "{PROJECT_ROOT}"\n')  # Use /d for changing drive and directory, quoted path
                f.write(f'"{python_path}" "{app_script_path}"\n')  # Quote paths to handle spaces and special characters
                f.write('if %ERRORLEVEL% NEQ 0 (\n')
                f.write('    echo.\n')
                f.write('    echo Application crashed. Please check the error messages above.\n')
                f.write('    pause\n')
                f.write(')\n')
            print_success("Created startup script: start.bat")
        else:
            # Create shell script for Linux/macOS
            with open(start_script_path, "w", encoding="utf-8") as f:
                f.write(f'#!/bin/bash\n')
                f.write(f'echo "Starting Essay Corrector System..."\n')
                f.write(f'cd "{PROJECT_ROOT}"\n')  # Ensure correct working directory
                f.write(f'"{python_path}" "{app_script_path}"\n')
            
            # Make the script executable
            os.chmod(start_script_path, 0o755)
            print_success("Created startup script: start.sh")
        
        return True
    except Exception as e:
        print_error(f"Failed to create startup script: {e}")
        return False


def print_usage_instructions(system_type, venv_dir=None):
    """
    Print usage instructions
    
    Args:
        system_type: System type ('Windows', 'Linux', 'Darwin')
        venv_dir: Virtual environment directory
    """
    print_step("Usage Instructions")
    
    print("To start the Essay Corrector System:")
    
    if system_type == "Windows":
        print("  1. Double-click the 'start.bat' file in the project directory")
        print("  - OR -")
        print("  1. Open Command Prompt")
        print(f"  2. Navigate to {PROJECT_ROOT}")
        print("  3. Run: start.bat")
    else:
        print("  1. Open Terminal")
        print(f"  2. Navigate to {PROJECT_ROOT}")
        print("  3. Run: ./start.sh")
    
    print("\nOnce started, open your web browser and visit:")
    print("  http://localhost:8329")
    
    if venv_dir:
        print("\nTo activate the virtual environment manually:")
        if system_type == "Windows":
            print(f"  {venv_dir}\\Scripts\\activate.bat")
        else:
            print(f"  source {venv_dir}/bin/activate")
    
    print("\nFor more information, please refer to the README.md file.")


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Essay Corrector System Setup")
    parser.add_argument("--no-venv", action="store_true", help="Don't create a virtual environment, use system Python")
    parser.add_argument("--venv-dir", default=".venv", help="Virtual environment directory (default: .venv)")
    parser.add_argument("--recreate-venv", action="store_true", help="Recreate virtual environment if it exists")
    parser.add_argument("--with-textract", action="store_true", help="Install textract package (optional but recommended)")
    parser.add_argument("--no-system-deps", action="store_true", help="Skip system dependencies installation")
    
    return parser.parse_args()


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print(">>> Essay Corrector System - Environment Setup")
    print(">>> Author: Biubush")
    print("=" * 60 + "\n")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Detect system
    system_type, distro = detect_system()
    
    # Install system dependencies
    if not args.no_system_deps:
        install_system_dependencies(system_type, distro)
    else:
        print_info("Skipping system dependencies installation (--no-system-deps)")
    
    # Setup virtual environment
    python_path = setup_virtual_env(args)
    print_info(f"Using Python: {python_path}")
    
    # Install Python dependencies
    success = install_python_dependencies(python_path, args=args)
    if not success:
        print_error("Failed to install Python dependencies. Setup incomplete.")
        return 1
    
    # Create startup script
    create_startup_script(system_type, python_path)
    
    # Print usage instructions
    print_usage_instructions(system_type, args.venv_dir if not args.no_venv else None)
    
    print("\n" + "=" * 60)
    print(">>> Setup completed successfully!")
    print(">>> You can now start the Essay Corrector System using the startup script.")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error occurred during setup: {e}")
        sys.exit(1)