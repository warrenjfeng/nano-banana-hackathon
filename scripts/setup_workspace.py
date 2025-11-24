#!/usr/bin/env python3
"""
Complete Workspace Setup Script
Sets up the entire ExecuTorch development environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required for ExecuTorch")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
        else:
            print("❌ Node.js not found. Please install Node.js")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} detected")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def setup_python_environment():
    """Set up Python environment"""
    print("🐍 Setting up Python environment...")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install additional development tools
    dev_tools = [
        "watchdog",  # For file watching
        "jupyter",   # For notebooks
        "ipykernel"  # For Jupyter kernel
    ]
    
    for tool in dev_tools:
        if not run_command(f"pip install {tool}", f"Installing {tool}"):
            print(f"⚠️  Failed to install {tool}, continuing...")
    
    return True

def setup_node_environment():
    """Set up Node.js environment"""
    print("📦 Setting up Node.js environment...")
    
    # Install npm dependencies
    if not run_command("npm install", "Installing npm dependencies"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    dirs = [
        "android_app",
        "models",
        "scripts",
        "notebooks",
        "data",
        "outputs",
        "logs",
        "temp",
        "build_cache",
        ".vscode"
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Created: {dir_name}")

def create_gitignore():
    """Create .gitignore file"""
    print("📝 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Android
android_app/.gradle/
android_app/build/
android_app/app/build/
android_app/local.properties
android_app/.idea/
android_app/*.iml

# ExecuTorch models
*.pte
models/*.pte

# Logs
logs/
*.log

# Temporary files
temp/
build_cache/
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore created")

def create_cursor_workspace():
    """Create Cursor workspace configuration"""
    print("⚙️  Creating Cursor workspace configuration...")
    
    workspace_config = {
        "folders": [
            {
                "path": ".",
                "name": "ExecuTorch Virtual Try-On"
            }
        ],
        "settings": {
            "python.defaultInterpreterPath": sys.executable,
            "python.terminal.activateEnvironment": True,
            "files.watcherExclude": {
                "**/node_modules/**": True,
                "**/build/**": True,
                "**/dist/**": True,
                "**/.gradle/**": True,
                "**/logs/**": True,
                "**/temp/**": True
            },
            "files.associations": {
                "*.pte": "binary",
                "*.pt": "python"
            },
            "editor.formatOnSave": True,
            "python.formatting.provider": "black",
            "python.linting.enabled": True,
            "python.linting.flake8Enabled": True,
            "java.configuration.updateBuildConfiguration": "automatic",
            "gradle.nestedProjects": True
        },
        "extensions": {
            "recommendations": [
                "ms-python.python",
                "ms-python.black-formatter",
                "ms-python.flake8",
                "redhat.java",
                "vscjava.vscode-gradle",
                "ms-vscode.vscode-json",
                "ms-vscode.vscode-typescript-next",
                "bradlc.vscode-tailwindcss"
            ]
        },
        "tasks": {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Setup ExecuTorch Environment",
                    "type": "shell",
                    "command": "python",
                    "args": ["setup_executorch.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Create Android Project",
                    "type": "shell",
                    "command": "python",
                    "args": ["scripts/create_android_project.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Convert Model to ExecuTorch",
                    "type": "shell",
                    "command": "python",
                    "args": ["scripts/model_converter.py", "--action", "create_test"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Start Development Server",
                    "type": "shell",
                    "command": "python",
                    "args": ["scripts/dev_server.py"],
                    "group": "build",
                    "isBackground": True,
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                },
                {
                    "label": "Deploy to Device",
                    "type": "shell",
                    "command": "python",
                    "args": ["scripts/device_deploy.py", "--action", "deploy"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared"
                    }
                }
            ]
        },
        "launch": {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "justMyCode": True
                },
                {
                    "name": "Python: Model Converter",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/scripts/model_converter.py",
                    "args": ["--action", "create_test"],
                    "console": "integratedTerminal",
                    "justMyCode": True
                },
                {
                    "name": "Python: Development Server",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/scripts/dev_server.py",
                    "console": "integratedTerminal",
                    "justMyCode": True
                }
            ]
        }
    }
    
    # Create .vscode directory
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # Save workspace configuration
    with open(vscode_dir / "settings.json", "w") as f:
        json.dump(workspace_config["settings"], f, indent=2)
    
    with open(vscode_dir / "extensions.json", "w") as f:
        json.dump(workspace_config["extensions"], f, indent=2)
    
    with open(vscode_dir / "tasks.json", "w") as f:
        json.dump(workspace_config["tasks"], f, indent=2)
    
    with open(vscode_dir / "launch.json", "w") as f:
        json.dump(workspace_config["launch"], f, indent=2)
    
    # Create workspace file
    with open("executorch-virtual-tryon.code-workspace", "w") as f:
        json.dump(workspace_config, f, indent=2)
    
    print("✅ Cursor workspace configuration created")

def create_development_scripts():
    """Create development helper scripts"""
    print("📜 Creating development scripts...")
    
    # Create quick start script
    quick_start_content = """#!/bin/bash
# Quick start script for ExecuTorch development

echo "🚀 Starting ExecuTorch Development Environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
npm install

# Create Android project if it doesn't exist
if [ ! -d "android_app" ]; then
    echo "📱 Creating Android project..."
    python scripts/create_android_project.py
fi

# Start development server
echo "🌐 Starting development server..."
python scripts/dev_server.py
"""
    
    with open("quick_start.sh", "w") as f:
        f.write(quick_start_content)
    
    # Make it executable
    os.chmod("quick_start.sh", 0o755)
    
    # Create Windows batch file
    quick_start_bat = """@echo off
REM Quick start script for ExecuTorch development

echo 🚀 Starting ExecuTorch Development Environment...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\\Scripts\\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt
npm install

REM Create Android project if it doesn't exist
if not exist "android_app" (
    echo 📱 Creating Android project...
    python scripts/create_android_project.py
)

REM Start development server
echo 🌐 Starting development server...
python scripts/dev_server.py
"""
    
    with open("quick_start.bat", "w") as f:
        f.write(quick_start_bat)
    
    print("✅ Development scripts created")

def create_readme():
    """Create comprehensive README"""
    print("📖 Creating README...")
    
    readme_content = """# ExecuTorch Virtual Try-On Development Environment

A complete development environment for building ExecuTorch-powered virtual try-on applications with synchronized development workflow using Cursor.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Android Studio (for Android development)
- Samsung S25 Ultra (or any Android device with USB debugging enabled)

### Setup
1. **Clone and setup the environment:**
   ```bash
   # Run the complete setup
   python scripts/setup_workspace.py
   
   # Or use the quick start script
   ./quick_start.sh  # Linux/Mac
   quick_start.bat   # Windows
   ```

2. **Connect your Samsung S25 Ultra:**
   - Enable Developer Options
   - Enable USB Debugging
   - Connect via USB

3. **Start development:**
   ```bash
   python scripts/dev_server.py
   ```

## 📁 Project Structure

```
├── android_app/              # Android project
├── models/                   # ExecuTorch model files (.pte)
├── scripts/                  # Development scripts
│   ├── create_android_project.py
│   ├── model_converter.py
│   ├── dev_server.py
│   └── device_deploy.py
├── notebooks/                # Jupyter notebooks for experimentation
├── data/                     # Training and test data
├── outputs/                  # Generated outputs
└── .vscode/                  # Cursor/VS Code configuration
```

## 🛠️ Development Workflow

### 1. Model Development
```bash
# Convert PyTorch model to ExecuTorch format
python scripts/model_converter.py --action create_test

# Convert existing model
python scripts/model_converter.py --action convert --model_path your_model.pt --output_path models/your_model.pte
```

### 2. Android Development
```bash
# Create Android project
python scripts/create_android_project.py

# Build and deploy to device
python scripts/device_deploy.py --action deploy
```

### 3. Synchronized Development
```bash
# Start development server with hot reloading
python scripts/dev_server.py
```

## 📱 Device Deployment

### Deploy to Samsung S25 Ultra
```bash
# Full deployment (build + install + launch)
python scripts/device_deploy.py --action deploy

# Individual steps
python scripts/device_deploy.py --action build
python scripts/device_deploy.py --action install
python scripts/device_deploy.py --action launch
```

### Debugging
```bash
# View device logs
python scripts/device_deploy.py --action logs

# Run tests
python scripts/device_deploy.py --action test
```

## 🔧 Cursor Integration

The workspace is pre-configured for Cursor with:
- Python development environment
- Android development tools
- ExecuTorch model support
- Hot reloading and file watching
- Integrated debugging

### Available Tasks (Ctrl+Shift+P → Tasks: Run Task)
- Setup ExecuTorch Environment
- Create Android Project
- Convert Model to ExecuTorch
- Start Development Server
- Deploy to Device

## 🤖 Model Integration

### Supported Formats
- **Input**: PyTorch models (.pt, .pth)
- **Output**: ExecuTorch models (.pte)
- **Backends**: XNNPACK, Vulkan, CPU

### Model Conversion
```python
from scripts.model_converter import export_to_executorch

# Convert your model
export_to_executorch(
    model=your_pytorch_model,
    output_path="models/your_model.pte",
    backend="xnnpack"
)
```

## 📊 Performance Optimization

### For Samsung S25 Ultra
- Use `arm64-v8a` architecture
- Optimize for XNNPACK backend
- Enable GPU acceleration with Vulkan backend
- Use quantized models for better performance

## 🐛 Troubleshooting

### Common Issues

1. **ADB not found**
   - Install Android SDK
   - Add to PATH: `export PATH=$PATH:$ANDROID_HOME/platform-tools`

2. **Device not detected**
   - Enable USB Debugging
   - Check USB connection
   - Run: `adb devices`

3. **Build failures**
   - Check Android SDK version
   - Ensure Gradle is properly configured
   - Check device compatibility

4. **Model loading errors**
   - Verify .pte file format
   - Check model metadata
   - Ensure correct backend

## 📚 Resources

- [ExecuTorch Documentation](https://docs.pytorch.org/executorch/1.0/index.html)
- [Android Development Guide](https://docs.pytorch.org/executorch/1.0/using-executorch-android.html)
- [Model Export Guide](https://docs.pytorch.org/executorch/1.0/using-executorch-export.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on Samsung S25 Ultra
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README created")

def main():
    """Main setup function"""
    print("🚀 Setting up ExecuTorch Development Workspace...")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met. Please install required software.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .gitignore
    create_gitignore()
    
    # Setup Python environment
    if not setup_python_environment():
        print("❌ Failed to setup Python environment")
        sys.exit(1)
    
    # Setup Node.js environment
    if not setup_node_environment():
        print("❌ Failed to setup Node.js environment")
        sys.exit(1)
    
    # Create Cursor workspace
    create_cursor_workspace()
    
    # Create development scripts
    create_development_scripts()
    
    # Create README
    create_readme()
    
    print("\n" + "=" * 60)
    print("🎉 ExecuTorch Development Workspace Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Connect your Samsung S25 Ultra with USB debugging enabled")
    print("2. Run: python scripts/create_android_project.py")
    print("3. Run: python scripts/model_converter.py --action create_test")
    print("4. Run: python scripts/dev_server.py")
    print("5. Open the project in Cursor for synchronized development")
    print("\n🚀 Quick Start:")
    print("   ./quick_start.sh  # Linux/Mac")
    print("   quick_start.bat   # Windows")
    print("\n📚 Documentation: README.md")

if __name__ == "__main__":
    main()



