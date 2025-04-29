#!/bin/bash
# Environment Setup Script Launcher - Essay Corrector System
# 
# This script is used to launch the environment setup script on Linux/macOS systems.
# 
# @author: Biubush

echo "Starting environment setup script..."

# Get script directory and project root with absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not detected. Please install Python 3.7 or higher."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "You can use 'brew install python3' or download from https://www.python.org/downloads/"
    else
        echo "You can install Python using your package manager, for example:"
        echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
        echo "  - CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "  - Arch Linux: sudo pacman -S python python-pip"
    fi
    exit 1
fi

# Execute setup.py script with absolute path
python3 "$SCRIPT_DIR/setup.py" "$@"

# If there's an error, exit
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred during installation. Please check the error messages above."
    exit 1
fi

echo ""
echo "Environment setup completed." 