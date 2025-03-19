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
    
    # Call the installation script directly with absolute path, preserving command line arguments
    return subprocess.call([sys.executable, install_script] + sys.argv[1:], cwd=current_dir)

if __name__ == "__main__":
    sys.exit(main()) 