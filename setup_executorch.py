#!/usr/bin/env python3
"""
ExecuTorch Development Setup Script
Sets up the development environment for ExecuTorch on Samsung S25 Ultra
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required for ExecuTorch")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def setup_android_sdk():
    """Set up Android SDK environment"""
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        print("⚠️  ANDROID_HOME not set. Please set it to your Android SDK path")
        print("   Example: export ANDROID_HOME=/Users/username/Library/Android/sdk")
        return False
    
    print(f"✅ Android SDK found at: {android_home}")
    return True

def create_directories():
    """Create necessary directories for the project"""
    dirs = [
        "android_app",
        "models",
        "scripts",
        "notebooks",
        "data",
        "outputs"
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Created directory: {dir_name}")

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def setup_git_hooks():
    """Set up git hooks for development"""
    hooks_dir = Path(".git/hooks")
    if hooks_dir.exists():
        pre_commit_hook = hooks_dir / "pre-commit"
        pre_commit_content = """#!/bin/sh
# Pre-commit hook for ExecuTorch development
echo "Running pre-commit checks..."
python -m black --check .
python -m flake8 .
"""
        pre_commit_hook.write_text(pre_commit_content)
        pre_commit_hook.chmod(0o755)
        print("✅ Git pre-commit hook installed")

def main():
    """Main setup function"""
    print("🚀 Setting up ExecuTorch development environment...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check Android SDK
    setup_android_sdk()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup git hooks
    setup_git_hooks()
    
    print("\n" + "=" * 50)
    print("🎉 ExecuTorch development environment setup complete!")
    print("\nNext steps:")
    print("1. Set up Android Studio and SDK")
    print("2. Connect your Samsung S25 Ultra")
    print("3. Run: python scripts/create_android_project.py")
    print("4. Start development with: python scripts/dev_server.py")

if __name__ == "__main__":
    main()



