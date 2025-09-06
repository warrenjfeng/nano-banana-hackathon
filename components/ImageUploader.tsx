
import React, { useState, useRef, useCallback } from 'react';
import type { ImageFile } from '../types';

interface ImageUploaderProps {
  id: string;
  title: string;
  description: string;
  onImageUpload: (file: ImageFile | null) => void;
}

const fileToData = (file: File): Promise<ImageFile> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = (reader.result as string).split(',')[1];
      resolve({ base64: base64String, mimeType: file.type });
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
};


export const ImageUploader: React.FC<ImageUploaderProps> = ({ id, title, description, onImageUpload }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isCameraActive, setIsCameraActive] = useState<boolean>(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [isVideoReady, setIsVideoReady] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const handleFileChange = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
      setPreviewUrl(URL.createObjectURL(file));
      setFileName(file.name);
      const imageData = await fileToData(file);
      onImageUpload(imageData);
    }
  }, [onImageUpload, previewUrl]);
  
  const handleRemoveImage = useCallback(() => {
    setPreviewUrl(null);
    setFileName(null);
    onImageUpload(null);
    if(fileInputRef.current) {
        fileInputRef.current.value = "";
    }
  }, [onImageUpload]);

  const handleUploaderClick = () => {
    fileInputRef.current?.click();
  };

  const startCamera = useCallback(async () => {
    if (isCameraActive) {
      console.log('Camera already active, skipping...');
      return;
    }
    
    try {
      setCameraError(null);
      setIsVideoReady(false);
      console.log('Starting camera...');
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'user',
          width: { ideal: 640 },
          height: { ideal: 480 }
        } 
      });
      
      console.log('Got camera stream:', stream);
      streamRef.current = stream;
      setIsCameraActive(true);
      
    } catch (error) {
      console.error('Error accessing camera:', error);
      setCameraError('Unable to access camera. Please check permissions and try again.');
      setIsVideoReady(false);
    }
  }, [isCameraActive]);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraActive(false);
    setIsVideoReady(false);
    setCameraError(null);
  }, []);

  const capturePhoto = useCallback(() => {
    console.log('Capture photo clicked!');
    console.log('Video ref:', videoRef.current);
    console.log('Canvas ref:', canvasRef.current);
    console.log('Is video ready:', isVideoReady);
    
    if (!videoRef.current || !canvasRef.current) {
      console.error('Missing video or canvas ref');
      setCameraError('Camera components not available. Please try again.');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    console.log('Video dimensions:', video.videoWidth, 'x', video.videoHeight);
    console.log('Video ready state:', video.readyState);
    console.log('Video current time:', video.currentTime);

    // Check if video has valid dimensions (more lenient check)
    if (video.videoWidth === 0 || video.videoHeight === 0) {
      console.error('Video dimensions not available, trying anyway...');
      // Don't return, try to capture anyway
    }

    const context = canvas.getContext('2d');
    if (!context) {
      console.error('Could not get canvas context');
      setCameraError('Unable to capture photo. Please try again.');
      return;
    }

    // Set canvas dimensions to match video (use fallback if video dimensions are 0)
    const width = video.videoWidth || 640;
    const height = video.videoHeight || 480;
    canvas.width = width;
    canvas.height = height;

    console.log('Drawing to canvas with dimensions:', width, 'x', height);

    // Draw the current video frame to canvas
    try {
      context.drawImage(video, 0, 0, width, height);
      console.log('Successfully drew video to canvas');
    } catch (error) {
      console.error('Error drawing video to canvas:', error);
      setCameraError('Error capturing video frame. Please try again.');
      return;
    }

    // Convert canvas to blob and then to base64
    canvas.toBlob(async (blob) => {
      console.log('Canvas toBlob callback, blob:', blob);
      if (blob) {
        try {
          console.log('Creating file from blob...');
          const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
          console.log('File created:', file);
          
          const imageData = await fileToData(file);
          console.log('Image data created:', imageData);
          
          // Update preview
          if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
          }
          const newPreviewUrl = URL.createObjectURL(file);
          setPreviewUrl(newPreviewUrl);
          setFileName('Camera Capture');
          onImageUpload(imageData);
          
          console.log('Successfully captured and processed photo');
          
          // Stop camera after capture
          stopCamera();
        } catch (error) {
          console.error('Error processing captured image:', error);
          setCameraError('Error processing captured image. Please try again.');
        }
      } else {
        console.error('Failed to create blob from canvas');
        setCameraError('Failed to capture photo. Please try again.');
      }
    }, 'image/jpeg', 0.8);
  }, [onImageUpload, previewUrl, stopCamera, isVideoReady]);

  // Handle video element when camera becomes active
  React.useEffect(() => {
    if (isCameraActive && streamRef.current && videoRef.current) {
      const video = videoRef.current;
      const stream = streamRef.current;
      
      console.log('Setting up video element with stream');
      video.srcObject = stream;
      
      // Ensure video plays
      video.play().then(() => {
        console.log('Video started playing');
      }).catch((error) => {
        console.error('Error playing video:', error);
      });
      
      const handleVideoReady = () => {
        console.log('Video ready! Dimensions:', video.videoWidth, 'x', video.videoHeight);
        setIsVideoReady(true);
      };
      
      // Try multiple events to ensure we catch when video is ready
      video.onloadedmetadata = handleVideoReady;
      video.oncanplay = handleVideoReady;
      video.onloadeddata = handleVideoReady;
      video.onplaying = handleVideoReady;
      
      // Fallback: check after a delay
      setTimeout(() => {
        if (video.videoWidth > 0 && video.videoHeight > 0) {
          console.log('Video ready via timeout fallback');
          setIsVideoReady(true);
        } else {
          console.log('Video not ready, but enabling capture anyway');
          setIsVideoReady(true);
        }
      }, 2000);
    }
  }, [isCameraActive]);

  // Handle paste events for image data
  React.useEffect(() => {
    const handlePaste = async (event: ClipboardEvent) => {
      const items = event.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.startsWith('image/')) {
          event.preventDefault();
          const file = item.getAsFile();
          if (file) {
            try {
              const imageData = await fileToData(file);
              if (previewUrl) {
                URL.revokeObjectURL(previewUrl);
              }
              setPreviewUrl(URL.createObjectURL(file));
              setFileName('Pasted Image');
              onImageUpload(imageData);
            } catch (error) {
              console.error('Error processing pasted image:', error);
            }
          }
          break;
        }
      }
    };

    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, [onImageUpload, previewUrl]);

  // Cleanup camera stream on unmount
  React.useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="bg-gray-800 border-2 border-dashed border-gray-600 rounded-lg p-6 text-center transition-all hover:border-purple-500 hover:bg-gray-700/50">
      <h3 className="text-xl font-semibold text-gray-100">{title}</h3>
      <p className="mt-1 text-sm text-gray-400">{description}</p>
      <p className="mt-1 text-xs text-gray-500">💡 Tip: You can also paste images (Ctrl+V)</p>
      <div 
        className="mt-4 aspect-square rounded-lg bg-gray-900/50 flex items-center justify-center cursor-pointer"
        onClick={!isCameraActive ? handleUploaderClick : undefined}
      >
        <input
          type="file"
          id={id}
          ref={fileInputRef}
          className="hidden"
          accept="image/png, image/jpeg, image/webp"
          onChange={handleFileChange}
        />
        <canvas ref={canvasRef} className="hidden" />
        
        {isCameraActive ? (
          <div className="w-full h-full relative">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover rounded-lg"
              style={{ backgroundColor: '#000' }}
            />
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex flex-col items-center gap-2">
              <div className="text-white text-xs bg-black/50 px-2 py-1 rounded">
                Video Ready: {isVideoReady ? 'Yes' : 'No'} | Stream: {streamRef.current ? 'Yes' : 'No'}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={capturePhoto}
                  className="bg-white text-black px-4 py-2 rounded-full font-semibold hover:bg-gray-200 transition-colors"
                >
                  📸 Capture
                </button>
                <button
                  onClick={stopCamera}
                  className="bg-red-600 text-white px-4 py-2 rounded-full font-semibold hover:bg-red-700 transition-colors"
                >
                  ✕ Cancel
                </button>
              </div>
            </div>
          </div>
        ) : previewUrl ? (
          <img src={previewUrl} alt="Preview" className="w-full h-full object-cover rounded-lg" />
        ) : (
          <div className="text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p className="mt-2 text-sm">Click to upload</p>
          </div>
        )}
      </div>
      {fileName && (
         <div className="mt-2 text-xs text-gray-400 flex items-center justify-center">
            <span className="truncate max-w-[200px]">{fileName}</span>
            <button onClick={handleRemoveImage} className="ml-2 text-red-400 hover:text-red-300">&times;</button>
        </div>
      )}
      
      {/* Camera Error Display */}
      {cameraError && (
        <div className="mt-2 text-xs text-red-400 text-center">
          {cameraError}
        </div>
      )}
      
      {/* Take Photo Button */}
      {!isCameraActive && (
        <div className="mt-4">
          <button
            onClick={startCamera}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Take Photo
          </button>
        </div>
      )}
    </div>
  );
};
