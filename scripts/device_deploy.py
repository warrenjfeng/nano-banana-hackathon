#!/usr/bin/env python3
"""
Device Deployment Script for Samsung S25 Ultra
Handles deployment and testing on connected Android devices
"""

import os
import sys
import subprocess
import time
import json
import argparse
from pathlib import Path
import socket

class DeviceDeployer:
    """Handles deployment to Android devices"""
    
    def __init__(self):
        self.device_id = None
        self.package_name = "com.executorch.virtualtryon"
        self.apk_path = None
    
    def check_adb_connection(self):
        """Check if ADB is available and devices are connected"""
        print("🔍 Checking ADB connection...")
        
        try:
            # Check if adb is available
            result = subprocess.run(["adb", "version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ ADB not found. Please install Android SDK and add to PATH")
                return False
            
            print("✅ ADB found")
            
            # Check connected devices
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Failed to list devices")
                return False
            
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = []
            
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            
            if not devices:
                print("❌ No devices connected")
                print("📱 Please connect your Samsung S25 Ultra and enable USB debugging")
                return False
            
            if len(devices) == 1:
                self.device_id = devices[0]
                print(f"✅ Found device: {self.device_id}")
            else:
                print(f"📱 Found {len(devices)} devices:")
                for i, device in enumerate(devices):
                    print(f"   {i+1}. {device}")
                
                # Use first device for now
                self.device_id = devices[0]
                print(f"✅ Using device: {self.device_id}")
            
            return True
            
        except FileNotFoundError:
            print("❌ ADB not found. Please install Android SDK")
            return False
        except Exception as e:
            print(f"❌ Error checking ADB: {e}")
            return False
    
    def get_device_info(self):
        """Get information about the connected device"""
        if not self.device_id:
            return None
        
        print(f"📱 Getting device info for {self.device_id}...")
        
        try:
            info = {}
            
            # Get device model
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                info['model'] = result.stdout.strip()
            
            # Get Android version
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "getprop", "ro.build.version.release"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                info['android_version'] = result.stdout.strip()
            
            # Get API level
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "getprop", "ro.build.version.sdk"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                info['api_level'] = result.stdout.strip()
            
            # Get architecture
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "getprop", "ro.product.cpu.abi"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                info['architecture'] = result.stdout.strip()
            
            print("📋 Device Information:")
            for key, value in info.items():
                print(f"   {key}: {value}")
            
            return info
            
        except Exception as e:
            print(f"❌ Error getting device info: {e}")
            return None
    
    def build_apk(self):
        """Build the Android APK"""
        print("🔨 Building Android APK...")
        
        android_dir = Path("android_app")
        if not android_dir.exists():
            print("❌ Android project not found. Run create_android_project.py first.")
            return False
        
        try:
            # Change to android directory and build
            cmd = ["./gradlew", "assembleDebug"]
            result = subprocess.run(
                cmd,
                cwd=android_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Find the generated APK
                apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
                if apk_path.exists():
                    self.apk_path = str(apk_path)
                    print(f"✅ APK built successfully: {self.apk_path}")
                    return True
                else:
                    print("❌ APK file not found after build")
                    return False
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Build timed out")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def install_apk(self):
        """Install the APK on the device"""
        if not self.apk_path:
            print("❌ No APK to install. Build first.")
            return False
        
        print(f"📱 Installing APK on {self.device_id}...")
        
        try:
            # Uninstall existing app if it exists
            subprocess.run(
                ["adb", "-s", self.device_id, "uninstall", self.package_name],
                capture_output=True
            )
            
            # Install new APK
            result = subprocess.run(
                ["adb", "-s", self.device_id, "install", self.apk_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ APK installed successfully")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def push_model_files(self):
        """Push model files to the device"""
        print("📤 Pushing model files to device...")
        
        models_dir = Path("models")
        if not models_dir.exists():
            print("⚠️  No models directory found")
            return False
        
        try:
            # Create models directory on device
            subprocess.run(
                ["adb", "-s", self.device_id, "shell", "mkdir", "-p", "/sdcard/Android/data/com.executorch.virtualtryon/files/models"],
                capture_output=True
            )
            
            # Push model files
            for model_file in models_dir.glob("*.pte"):
                print(f"📤 Pushing {model_file.name}...")
                result = subprocess.run(
                    ["adb", "-s", self.device_id, "push", str(model_file), 
                     f"/sdcard/Android/data/com.executorch.virtualtryon/files/models/"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ {model_file.name} pushed successfully")
                else:
                    print(f"❌ Failed to push {model_file.name}: {result.stderr}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error pushing model files: {e}")
            return False
    
    def launch_app(self):
        """Launch the app on the device"""
        print(f"🚀 Launching app on {self.device_id}...")
        
        try:
            # Launch the main activity
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "am", "start", 
                 "-n", f"{self.package_name}/.MainActivity"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ App launched successfully")
                return True
            else:
                print(f"❌ Failed to launch app: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error launching app: {e}")
            return False
    
    def get_logs(self):
        """Get device logs for debugging"""
        print("📋 Getting device logs...")
        
        try:
            # Clear logcat first
            subprocess.run(["adb", "-s", self.device_id, "logcat", "-c"], capture_output=True)
            
            # Get logs with our package filter
            result = subprocess.run(
                ["adb", "-s", self.device_id, "logcat", "-s", "VirtualTryOn:*", "AndroidRuntime:E"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                print("📋 Recent logs:")
                print(result.stdout)
            else:
                print("📋 No recent logs found")
            
            return True
            
        except subprocess.TimeoutExpired:
            print("📋 Log collection timed out")
            return True
        except Exception as e:
            print(f"❌ Error getting logs: {e}")
            return False
    
    def run_tests(self):
        """Run tests on the device"""
        print("🧪 Running tests on device...")
        
        try:
            # Run unit tests
            android_dir = Path("android_app")
            result = subprocess.run(
                ["./gradlew", "connectedAndroidTest"],
                cwd=android_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅ Tests passed")
                return True
            else:
                print(f"❌ Tests failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out")
            return False
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
    
    def full_deploy(self):
        """Perform full deployment process"""
        print("🚀 Starting full deployment process...")
        print("=" * 50)
        
        # Check ADB connection
        if not self.check_adb_connection():
            return False
        
        # Get device info
        device_info = self.get_device_info()
        if not device_info:
            print("⚠️  Could not get device info, continuing anyway...")
        
        # Build APK
        if not self.build_apk():
            return False
        
        # Install APK
        if not self.install_apk():
            return False
        
        # Push model files
        self.push_model_files()
        
        # Launch app
        if not self.launch_app():
            return False
        
        print("\n" + "=" * 50)
        print("🎉 Deployment completed successfully!")
        print("\nNext steps:")
        print("1. Check the app on your device")
        print("2. Run: python scripts/device_deploy.py --logs to see logs")
        print("3. Run: python scripts/device_deploy.py --test to run tests")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Deploy ExecuTorch app to Android device')
    parser.add_argument('--action', choices=['deploy', 'build', 'install', 'launch', 'logs', 'test'], 
                       default='deploy', help='Action to perform')
    parser.add_argument('--device-id', type=str, help='Specific device ID to use')
    
    args = parser.parse_args()
    
    deployer = DeviceDeployer()
    
    if args.device_id:
        deployer.device_id = args.device_id
    
    if args.action == 'deploy':
        deployer.full_deploy()
    elif args.action == 'build':
        deployer.build_apk()
    elif args.action == 'install':
        if deployer.check_adb_connection():
            deployer.build_apk()
            deployer.install_apk()
    elif args.action == 'launch':
        if deployer.check_adb_connection():
            deployer.launch_app()
    elif args.action == 'logs':
        if deployer.check_adb_connection():
            deployer.get_logs()
    elif args.action == 'test':
        if deployer.check_adb_connection():
            deployer.run_tests()

if __name__ == "__main__":
    main()



