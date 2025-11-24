#!/usr/bin/env python3
"""
Development Server for ExecuTorch
Provides hot reloading and synchronized development workflow
"""

import os
import sys
import time
import json
import subprocess
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

class ExecuTorchDevHandler(FileSystemEventHandler):
    """File system event handler for development server"""
    
    def __init__(self, callback):
        self.callback = callback
        self.last_modified = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        current_time = time.time()
        
        # Debounce file changes
        if file_path in self.last_modified:
            if current_time - self.last_modified[file_path] < 1.0:
                return
        
        self.last_modified[file_path] = current_time
        
        # Only process relevant files
        if any(file_path.endswith(ext) for ext in ['.py', '.kt', '.java', '.xml', '.gradle']):
            print(f"🔄 File changed: {file_path}")
            self.callback(file_path)

class DevelopmentServer:
    """Main development server class"""
    
    def __init__(self, port=8080, android_port=8081):
        self.port = port
        self.android_port = android_port
        self.observers = []
        self.processes = {}
        self.setup_directories()
    
    def setup_directories(self):
        """Set up necessary directories"""
        dirs = ['logs', 'temp', 'build_cache']
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)
    
    def start_web_server(self):
        """Start the web development server"""
        print(f"🌐 Starting web server on port {self.port}...")
        
        try:
            # Start Vite dev server
            cmd = ["npm", "run", "dev", "--", "--port", str(self.port)]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes['web'] = process
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Open browser
            webbrowser.open(f"http://localhost:{self.port}")
            print(f"✅ Web server started at http://localhost:{self.port}")
            
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
    
    def start_android_build_watcher(self):
        """Start watching Android project for changes"""
        print("📱 Starting Android build watcher...")
        
        android_dir = Path("android_app")
        if not android_dir.exists():
            print("⚠️  Android project not found. Run create_android_project.py first.")
            return
        
        def on_android_change(file_path):
            print(f"📱 Android file changed: {file_path}")
            self.trigger_android_build()
        
        observer = Observer()
        observer.schedule(ExecuTorchDevHandler(on_android_change), str(android_dir), recursive=True)
        observer.start()
        self.observers.append(observer)
        
        print("✅ Android build watcher started")
    
    def trigger_android_build(self):
        """Trigger Android build when files change"""
        print("🔨 Triggering Android build...")
        
        try:
            # Run gradle build
            android_dir = Path("android_app")
            cmd = ["./gradlew", "assembleDebug"]
            
            process = subprocess.Popen(
                cmd, 
                cwd=android_dir,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Store process for potential cleanup
            self.processes['android_build'] = process
            
            print("✅ Android build triggered")
            
        except Exception as e:
            print(f"❌ Failed to trigger Android build: {e}")
    
    def start_model_watcher(self):
        """Start watching model files for changes"""
        print("🤖 Starting model watcher...")
        
        models_dir = Path("models")
        scripts_dir = Path("scripts")
        
        def on_model_change(file_path):
            print(f"🤖 Model file changed: {file_path}")
            if file_path.endswith('.py'):
                self.trigger_model_conversion()
        
        # Watch models directory
        if models_dir.exists():
            observer = Observer()
            observer.schedule(ExecuTorchDevHandler(on_model_change), str(models_dir), recursive=True)
            observer.start()
            self.observers.append(observer)
        
        # Watch scripts directory
        if scripts_dir.exists():
            observer = Observer()
            observer.schedule(ExecuTorchDevHandler(on_model_change), str(scripts_dir), recursive=True)
            observer.start()
            self.observers.append(observer)
        
        print("✅ Model watcher started")
    
    def trigger_model_conversion(self):
        """Trigger model conversion when files change"""
        print("🔄 Triggering model conversion...")
        
        try:
            cmd = [sys.executable, "scripts/model_converter.py", "--action", "create_test"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes['model_conversion'] = process
            
            print("✅ Model conversion triggered")
            
        except Exception as e:
            print(f"❌ Failed to trigger model conversion: {e}")
    
    def start_device_monitor(self):
        """Start monitoring connected devices"""
        print("📱 Starting device monitor...")
        
        def monitor_devices():
            while True:
                try:
                    # Check for connected Android devices
                    result = subprocess.run(
                        ["adb", "devices"], 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')[1:]  # Skip header
                        devices = [line.split('\t')[0] for line in lines if line.strip()]
                        
                        if devices:
                            print(f"📱 Connected devices: {', '.join(devices)}")
                        else:
                            print("📱 No devices connected")
                    
                except Exception as e:
                    print(f"⚠️  Device monitoring error: {e}")
                
                time.sleep(10)  # Check every 10 seconds
        
        device_thread = threading.Thread(target=monitor_devices, daemon=True)
        device_thread.start()
        print("✅ Device monitor started")
    
    def create_cursor_config(self):
        """Create Cursor configuration for synchronized development"""
        print("⚙️  Creating Cursor configuration...")
        
        cursor_config = {
            "version": "1.0.0",
            "name": "ExecuTorch Development",
            "folders": [
                {
                    "path": ".",
                    "name": "Virtual Try-On Project"
                }
            ],
            "settings": {
                "python.defaultInterpreterPath": sys.executable,
                "python.terminal.activateEnvironment": True,
                "files.watcherExclude": {
                    "**/node_modules/**": True,
                    "**/build/**": True,
                    "**/dist/**": True,
                    "**/.gradle/**": True
                },
                "files.associations": {
                    "*.pte": "binary",
                    "*.pt": "python"
                },
                "editor.formatOnSave": True,
                "python.formatting.provider": "black",
                "python.linting.enabled": True,
                "python.linting.flake8Enabled": True
            },
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.black-formatter",
                    "ms-python.flake8",
                    "redhat.java",
                    "vscjava.vscode-gradle",
                    "ms-vscode.vscode-json"
                ]
            },
            "tasks": {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Setup ExecuTorch",
                        "type": "shell",
                        "command": "python",
                        "args": ["setup_executorch.py"],
                        "group": "build"
                    },
                    {
                        "label": "Create Android Project",
                        "type": "shell",
                        "command": "python",
                        "args": ["scripts/create_android_project.py"],
                        "group": "build"
                    },
                    {
                        "label": "Convert Model",
                        "type": "shell",
                        "command": "python",
                        "args": ["scripts/model_converter.py", "--action", "create_test"],
                        "group": "build"
                    },
                    {
                        "label": "Start Dev Server",
                        "type": "shell",
                        "command": "python",
                        "args": ["scripts/dev_server.py"],
                        "group": "build"
                    }
                ]
            }
        }
        
        # Create .vscode directory and config
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)
        
        with open(vscode_dir / "settings.json", "w") as f:
            json.dump(cursor_config["settings"], f, indent=2)
        
        with open(vscode_dir / "extensions.json", "w") as f:
            json.dump(cursor_config["extensions"], f, indent=2)
        
        with open(vscode_dir / "tasks.json", "w") as f:
            json.dump(cursor_config["tasks"], f, indent=2)
        
        print("✅ Cursor configuration created")
    
    def start(self):
        """Start the development server"""
        print("🚀 Starting ExecuTorch Development Server...")
        print("=" * 50)
        
        # Create Cursor configuration
        self.create_cursor_config()
        
        # Start web server
        self.start_web_server()
        
        # Start watchers
        self.start_android_build_watcher()
        self.start_model_watcher()
        self.start_device_monitor()
        
        print("\n" + "=" * 50)
        print("🎉 Development server started successfully!")
        print("\nAvailable services:")
        print(f"🌐 Web app: http://localhost:{self.port}")
        print("📱 Android project: android_app/")
        print("🤖 Models: models/")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down development server...")
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the development server"""
        # Stop observers
        for observer in self.observers:
            observer.stop()
            observer.join()
        
        # Terminate processes
        for name, process in self.processes.items():
            if process.poll() is None:  # Process is still running
                print(f"🛑 Stopping {name} process...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ Development server stopped")

def main():
    parser = argparse.ArgumentParser(description='ExecuTorch Development Server')
    parser.add_argument('--port', type=int, default=8080, help='Web server port')
    parser.add_argument('--android-port', type=int, default=8081, help='Android server port')
    
    args = parser.parse_args()
    
    server = DevelopmentServer(args.port, args.android_port)
    server.start()

if __name__ == "__main__":
    main()



