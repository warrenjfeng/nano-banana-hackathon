#!/usr/bin/env python3
"""
Android Project Creation Script for ExecuTorch
Creates a complete Android project structure for ExecuTorch integration
"""

import os
import json
import shutil
from pathlib import Path

def create_android_project_structure():
    """Create the Android project structure"""
    android_dir = Path("android_app")
    
    # Main directories
    directories = [
        "app/src/main/java/com/executorch/virtualtryon",
        "app/src/main/res/layout",
        "app/src/main/res/values",
        "app/src/main/res/drawable",
        "app/src/main/assets",
        "app/src/main/jniLibs/arm64-v8a",
        "app/src/main/jniLibs/armeabi-v7a",
        "app/src/main/jniLibs/x86_64",
        "app/src/test/java",
        "app/src/androidTest/java",
        "gradle/wrapper"
    ]
    
    for dir_path in directories:
        (android_dir / dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {dir_path}")

def create_build_gradle():
    """Create the main build.gradle file"""
    build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.executorch.virtualtryon'
    compileSdk 34

    defaultConfig {
        applicationId "com.executorch.virtualtryon"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        
        ndk {
            abiFilters 'arm64-v8a', 'armeabi-v7a', 'x86_64'
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = '1.8'
    }
    
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.7.0'
    
    // ExecuTorch dependencies
    implementation 'org.pytorch:executorch:1.0.0'
    implementation 'org.pytorch:pytorch_android:1.13.1'
    implementation 'org.pytorch:pytorch_android_torchvision:1.13.1'
    
    // Image processing
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    
    // Camera and permissions
    implementation 'androidx.camera:camera-core:1.3.1'
    implementation 'androidx.camera:camera-camera2:1.3.1'
    implementation 'androidx.camera:camera-lifecycle:1.3.1'
    implementation 'androidx.camera:camera-view:1.3.1'
    
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    
    with open("android_app/build.gradle", "w") as f:
        f.write(build_gradle_content)
    print("✅ Created build.gradle")

def create_app_build_gradle():
    """Create the app-level build.gradle file"""
    app_build_gradle_content = """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.executorch.virtualtryon'
    compileSdk 34

    defaultConfig {
        applicationId "com.executorch.virtualtryon"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        
        ndk {
            abiFilters 'arm64-v8a', 'armeabi-v7a', 'x86_64'
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    
    kotlinOptions {
        jvmTarget = '1.8'
    }
    
    buildFeatures {
        viewBinding true
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.7.0'
    
    // ExecuTorch dependencies
    implementation 'org.pytorch:executorch:1.0.0'
    implementation 'org.pytorch:pytorch_android:1.13.1'
    implementation 'org.pytorch:pytorch_android_torchvision:1.13.1'
    
    // Image processing
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    
    // Camera and permissions
    implementation 'androidx.camera:camera-core:1.3.1'
    implementation 'androidx.camera:camera-camera2:1.3.1'
    implementation 'androidx.camera:camera-lifecycle:1.3.1'
    implementation 'androidx.camera:camera-view:1.3.1'
    
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
"""
    
    with open("android_app/app/build.gradle", "w") as f:
        f.write(app_build_gradle_content)
    print("✅ Created app/build.gradle")

def create_android_manifest():
    """Create AndroidManifest.xml"""
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.VirtualTryOn"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.VirtualTryOn">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
    </application>

</manifest>
"""
    
    with open("android_app/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(manifest_content)
    print("✅ Created AndroidManifest.xml")

def create_main_activity():
    """Create the main activity Kotlin file"""
    main_activity_content = """package com.executorch.virtualtryon

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import com.executorch.virtualtryon.databinding.ActivityMainBinding
import com.executorch.virtualtryon.viewmodel.MainViewModel
import org.pytorch.executorch.ExecutorTorch
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private lateinit var viewModel: MainViewModel
    
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            Toast.makeText(this, "Permission granted", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show()
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        viewModel = ViewModelProvider(this)[MainViewModel::class.java]
        
        setupUI()
        checkPermissions()
        setupObservers()
    }
    
    private fun setupUI() {
        binding.btnCapturePhoto.setOnClickListener {
            // TODO: Implement camera capture
        }
        
        binding.btnSelectFromGallery.setOnClickListener {
            // TODO: Implement gallery selection
        }
        
        binding.btnProcessImage.setOnClickListener {
            // TODO: Implement image processing with ExecuTorch
        }
    }
    
    private fun checkPermissions() {
        when {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED -> {
                // Permission already granted
            }
            else -> {
                requestPermissionLauncher.launch(Manifest.permission.CAMERA)
            }
        }
    }
    
    private fun setupObservers() {
        viewModel.processedImage.observe(this) { bitmap ->
            binding.ivResult.setImageBitmap(bitmap)
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) 
                android.view.View.VISIBLE else android.view.View.GONE
        }
        
        viewModel.errorMessage.observe(this) { error ->
            if (error.isNotEmpty()) {
                Toast.makeText(this, error, Toast.LENGTH_LONG).show()
            }
        }
    }
}
"""
    
    with open("android_app/app/src/main/java/com/executorch/virtualtryon/MainActivity.kt", "w") as f:
        f.write(main_activity_content)
    print("✅ Created MainActivity.kt")

def create_view_model():
    """Create the ViewModel for the app"""
    view_model_content = """package com.executorch.virtualtryon.viewmodel

import android.graphics.Bitmap
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.pytorch.executorch.ExecutorTorch
import java.io.File

class MainViewModel : ViewModel() {
    
    private val _processedImage = MutableLiveData<Bitmap?>()
    val processedImage: LiveData<Bitmap?> = _processedImage
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _errorMessage = MutableLiveData<String>()
    val errorMessage: LiveData<String> = _errorMessage
    
    private var executorTorch: ExecutorTorch? = null
    
    init {
        loadModel()
    }
    
    private fun loadModel() {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                
                withContext(Dispatchers.IO) {
                    // Load the ExecuTorch model
                    val modelFile = File("models/virtual_try_on.pte")
                    if (modelFile.exists()) {
                        executorTorch = ExecutorTorch.load(modelFile.absolutePath)
                    } else {
                        _errorMessage.postValue("Model file not found: ${modelFile.absolutePath}")
                    }
                }
            } catch (e: Exception) {
                _errorMessage.value = "Error loading model: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    fun processImage(inputBitmap: Bitmap) {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                _errorMessage.value = ""
                
                val result = withContext(Dispatchers.IO) {
                    // TODO: Implement image processing with ExecuTorch
                    // This is where you'll call your model inference
                    processImageWithModel(inputBitmap)
                }
                
                _processedImage.value = result
            } catch (e: Exception) {
                _errorMessage.value = "Error processing image: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    private fun processImageWithModel(inputBitmap: Bitmap): Bitmap? {
        // TODO: Implement actual model inference
        // This is a placeholder - you'll need to:
        // 1. Convert Bitmap to tensor
        // 2. Run inference with ExecuTorch
        // 3. Convert result tensor back to Bitmap
        
        return inputBitmap // Placeholder return
    }
}
"""
    
    # Create viewmodel directory
    Path("android_app/app/src/main/java/com/executorch/virtualtryon/viewmodel").mkdir(parents=True, exist_ok=True)
    
    with open("android_app/app/src/main/java/com/executorch/virtualtryon/viewmodel/MainViewModel.kt", "w") as f:
        f.write(view_model_content)
    print("✅ Created MainViewModel.kt")

def create_layout_files():
    """Create layout files"""
    # Main activity layout
    main_layout_content = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Virtual Style Try-On"
        android:textSize="24sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="24dp" />

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical">

            <!-- Input Image Section -->
            <TextView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Input Image"
                android:textSize="18sp"
                android:textStyle="bold"
                android:layout_marginBottom="8dp" />

            <ImageView
                android:id="@+id/iv_input"
                android:layout_width="match_parent"
                android:layout_height="200dp"
                android:background="@drawable/image_placeholder"
                android:scaleType="centerCrop"
                android:layout_marginBottom="16dp" />

            <!-- Action Buttons -->
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:layout_marginBottom="24dp">

                <Button
                    android:id="@+id/btn_capture_photo"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Capture"
                    android:layout_marginEnd="8dp" />

                <Button
                    android:id="@+id/btn_select_from_gallery"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:text="Gallery"
                    android:layout_marginStart="8dp" />

            </LinearLayout>

            <!-- Process Button -->
            <Button
                android:id="@+id/btn_process_image"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Process with ExecuTorch"
                android:layout_marginBottom="24dp" />

            <!-- Progress Bar -->
            <ProgressBar
                android:id="@+id/progress_bar"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:visibility="gone"
                android:layout_marginBottom="16dp" />

            <!-- Result Image Section -->
            <TextView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Result"
                android:textSize="18sp"
                android:textStyle="bold"
                android:layout_marginBottom="8dp" />

            <ImageView
                android:id="@+id/iv_result"
                android:layout_width="match_parent"
                android:layout_height="200dp"
                android:background="@drawable/image_placeholder"
                android:scaleType="centerCrop" />

        </LinearLayout>

    </ScrollView>

</LinearLayout>
"""
    
    with open("android_app/app/src/main/res/layout/activity_main.xml", "w") as f:
        f.write(main_layout_content)
    print("✅ Created activity_main.xml")

def create_strings_and_styles():
    """Create strings.xml and styles"""
    strings_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Virtual Try-On</string>
    <string name="capture_photo">Capture Photo</string>
    <string name="select_from_gallery">Select from Gallery</string>
    <string name="process_image">Process Image</string>
    <string name="loading">Processing...</string>
    <string name="error_loading_model">Error loading model</string>
    <string name="error_processing_image">Error processing image</string>
</resources>
"""
    
    with open("android_app/app/src/main/res/values/strings.xml", "w") as f:
        f.write(strings_content)
    print("✅ Created strings.xml")

def create_gradle_wrapper():
    """Create gradle wrapper files"""
    gradle_wrapper_properties = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
    
    with open("android_app/gradle/wrapper/gradle-wrapper.properties", "w") as f:
        f.write(gradle_wrapper_properties)
    print("✅ Created gradle-wrapper.properties")

def main():
    """Main function to create Android project"""
    print("🚀 Creating Android project for ExecuTorch...")
    print("=" * 50)
    
    create_android_project_structure()
    create_build_gradle()
    create_app_build_gradle()
    create_android_manifest()
    create_main_activity()
    create_view_model()
    create_layout_files()
    create_strings_and_styles()
    create_gradle_wrapper()
    
    print("\n" + "=" * 50)
    print("🎉 Android project created successfully!")
    print("\nNext steps:")
    print("1. Open android_app/ in Android Studio")
    print("2. Sync project with Gradle files")
    print("3. Connect your Samsung S25 Ultra")
    print("4. Build and run the app")

if __name__ == "__main__":
    main()



