#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Installation Bootstrap Script - Essay Corrector System

This script automatically detects the current system platform and calls the appropriate installation script.

@author: Biubush
"""

import os
import sys
import platform
import subprocess
import time

# Get absolute paths for script directory and project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Change to project root directory
os.chdir(PROJECT_ROOT)

def print_info(message):
    """Print information message"""
    print(f"[INFO] {message}")

def print_error(message):
    """Print error message"""
    print(f"[ERROR] {message}")

def wait_for_keypress():
    """Wait for user to press a key to continue"""
    if platform.system() == "Windows":
        os.system("pause")
    else:
        input("Press Enter to continue...")

def is_executable(file_path):
    """Check if file exists and is executable"""
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print(">>> Essay Corrector System - Installation Bootstrap")
    print(">>> Author: Biubush")
    print("=" * 60 + "\n")
    
    # Detect system type
    system_type = platform.system()
    print_info(f"Detected {system_type} operating system")
    print_info(f"Project root: {PROJECT_ROOT}")
    print_info(f"Script directory: {SCRIPT_DIR}")
    
    # Get command line arguments (excluding script name)
    args = sys.argv[1:]
    
    if system_type == "Windows":
        # Windows platform
        setup_script = os.path.join(SCRIPT_DIR, "setup.bat")
        if not os.path.isfile(setup_script):
            print_error(f"Windows setup script not found: {setup_script}")
            print_info("Please ensure you're running this script from the correct directory")
            wait_for_keypress()
            return 1
        
        print_info(f"Running Windows setup script: {setup_script}")
        try:
            # Call batch script directly with absolute path
            subprocess.run([setup_script] + args, check=True, cwd=PROJECT_ROOT)
        except subprocess.CalledProcessError as e:
            print_error(f"Setup script execution failed: {e}")
            wait_for_keypress()
            return 1
        
    elif system_type in ["Linux", "Darwin"]:  # Linux or macOS
        # Linux/macOS platform
        setup_script = os.path.join(SCRIPT_DIR, "setup.sh")
        
        # Check if script exists
        if not os.path.isfile(setup_script):
            print_error(f"Unix setup script not found: {setup_script}")
            print_info("Please ensure you're running this script from the correct directory")
            wait_for_keypress()
            return 1
        
        # Check if script is executable
        if not is_executable(setup_script):
            print_info("Adding execution permission to setup.sh")
            try:
                os.chmod(setup_script, 0o755)  # Add execution permission
            except Exception as e:
                print_error(f"Cannot add execution permission: {e}")
                print_info(f"Please execute manually: chmod +x {setup_script}")
                wait_for_keypress()
                return 1
        
        print_info(f"Running Unix setup script: {setup_script}")
        try:
            # Execute shell script with absolute path
            subprocess.run([setup_script] + args, check=True, cwd=PROJECT_ROOT)
        except subprocess.CalledProcessError as e:
            print_error(f"Setup script execution failed: {e}")
            wait_for_keypress()
            return 1
    
    else:
        # Unknown system type
        print_error(f"Unsupported operating system: {system_type}")
        print_info("This installer only supports Windows, Linux, and macOS")
        wait_for_keypress()
        return 1
    
    print("\nInstallation bootstrap completed")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        # On Windows, give users some time to view the output
        if platform.system() == "Windows":
            time.sleep(2)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInstallation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error occurred during installation: {e}")
        wait_for_keypress()
        sys.exit(1) 