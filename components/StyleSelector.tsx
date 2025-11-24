import React, { useState, useRef, useCallback } from 'react';
import type { StyleRequest, ImageFile } from '../types';
import { HAIRSTYLE_PRESETS, CLOTHING_PRESETS, ACCESSORY_PRESETS } from '../constants/hairstyles';

interface StyleSelectorProps {
  onStyleSelect: (styleRequest: StyleRequest) => void;
  selectedStyle?: StyleRequest;
}

export const StyleSelector: React.FC<StyleSelectorProps> = ({ onStyleSelect, selectedStyle }) => {
  const [customText, setCustomText] = useState('');
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [isVideoReady, setIsVideoReady] = useState(false);
  const [currentCategory, setCurrentCategory] = useState<'hairstyles' | 'clothing' | 'accessories'>('hairstyles');
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const handlePresetSelect = (presetId: string) => {
    let preset;
    if (currentCategory === 'hairstyles') {
      preset = HAIRSTYLE_PRESETS.find(p => p.id === presetId);
    } else if (currentCategory === 'clothing') {
      preset = CLOTHING_PRESETS.find(p => p.id === presetId);
    } else {
      preset = ACCESSORY_PRESETS.find(p => p.id === presetId);
    }

    const styleRequest: StyleRequest = {
      type: 'text',
      presetId,
      text: preset?.name || ''
    };
    onStyleSelect(styleRequest);
    setShowCustomInput(false);
  };

  const handleCustomSubmit = () => {
    if (customText.trim()) {
      const styleRequest: StyleRequest = {
        type: 'text',
        text: customText.trim()
      };
      onStyleSelect(styleRequest);
      setShowCustomInput(false);
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1];
        const styleRequest: StyleRequest = {
          type: 'image',
          image: { base64: base64String, mimeType: file.type }
        };
        onStyleSelect(styleRequest);
      };
      reader.readAsDataURL(file);
    }
  };

  const startCamera = useCallback(async () => {
    if (isCameraActive) {
      console.log('Camera already active, skipping...');
      return;
    }
    
    try {
      setCameraError(null);
      setIsVideoReady(false);
      console.log('Starting camera for style capture...');
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'environment', // Use back camera for taking photos of items
          width: { ideal: 640 },
          height: { ideal: 480 }
        } 
      });
      
      console.log('Got camera stream for style capture:', stream);
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

  const captureStylePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) {
      console.error('Missing video or canvas ref for style capture');
      setCameraError('Camera components not available. Please try again.');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) {
      console.error('Could not get canvas context for style capture');
      setCameraError('Unable to capture photo. Please try again.');
      return;
    }

    // Set canvas dimensions to match video
    const width = video.videoWidth || 640;
    const height = video.videoHeight || 480;
    canvas.width = width;
    canvas.height = height;

    // Draw the current video frame to canvas
    try {
      context.drawImage(video, 0, 0, width, height);
      console.log('Successfully drew style video to canvas');
    } catch (error) {
      console.error('Error drawing style video to canvas:', error);
      setCameraError('Error capturing video frame. Please try again.');
      return;
    }

    // Convert canvas to blob and then to base64
    canvas.toBlob(async (blob) => {
      if (blob) {
        try {
          const file = new File([blob], 'style-capture.jpg', { type: 'image/jpeg' });
          const reader = new FileReader();
          reader.onload = () => {
            const base64String = (reader.result as string).split(',')[1];
            const styleRequest: StyleRequest = {
              type: 'image',
              image: { base64: base64String, mimeType: 'image/jpeg' }
            };
            onStyleSelect(styleRequest);
            stopCamera();
          };
          reader.readAsDataURL(file);
        } catch (error) {
          console.error('Error processing captured style image:', error);
          setCameraError('Error processing captured image. Please try again.');
        }
      } else {
        console.error('Failed to create blob from style canvas');
        setCameraError('Failed to capture photo. Please try again.');
      }
    }, 'image/jpeg', 0.8);
  }, [onStyleSelect, stopCamera]);

  // Handle video element when camera becomes active
  React.useEffect(() => {
    if (isCameraActive && streamRef.current && videoRef.current) {
      const video = videoRef.current;
      const stream = streamRef.current;
      
      console.log('Setting up style video element with stream');
      video.srcObject = stream;
      
      // Ensure video plays
      video.play().then(() => {
        console.log('Style video started playing');
      }).catch((error) => {
        console.error('Error playing style video:', error);
      });
      
      const handleVideoReady = () => {
        console.log('Style video ready! Dimensions:', video.videoWidth, 'x', video.videoHeight);
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
          console.log('Style video ready via timeout fallback');
          setIsVideoReady(true);
        } else {
          console.log('Style video not ready, but enabling capture anyway');
          setIsVideoReady(true);
        }
      }, 2000);
    }
  }, [isCameraActive]);


  // Cleanup camera stream on unmount
  React.useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const getSelectedStyleName = () => {
    if (!selectedStyle) return null;
    if (selectedStyle.type === 'image') return 'Custom Image';
    if (selectedStyle.presetId) {
      // Check all categories for the preset
      let preset = HAIRSTYLE_PRESETS.find(p => p.id === selectedStyle.presetId);
      if (!preset) preset = CLOTHING_PRESETS.find(p => p.id === selectedStyle.presetId);
      if (!preset) preset = ACCESSORY_PRESETS.find(p => p.id === selectedStyle.presetId);
      return preset?.name;
    }
    return selectedStyle.text;
  };

  return (
    <div className="bg-gray-800 border-2 border-dashed border-gray-600 rounded-lg p-6 text-center transition-all hover:border-purple-500 hover:bg-gray-700/50">
      <h3 className="text-xl font-semibold text-gray-100">2. Choose Your Style</h3>
      <p className="mt-1 text-sm text-gray-400">Hairstyles, clothing, accessories, or any style element</p>
      <p className="mt-1 text-xs text-gray-500">💡 Tip: You can paste images (Ctrl+V) or take photos of items</p>
      
      {/* Selected Style Display */}
      {selectedStyle && (
        <div className="mt-4 p-3 bg-purple-600/20 border border-purple-500/30 rounded-lg">
          <p className="text-purple-300 text-sm">
            <span className="font-semibold">Selected:</span> {getSelectedStyleName()}
          </p>
        </div>
      )}

      {/* Category Selection */}
      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-300 mb-3">Categories</h4>
        <div className="grid grid-cols-3 gap-2 mb-4">
          <button
            onClick={() => setCurrentCategory('hairstyles')}
            className={`p-2 text-xs rounded-lg border transition-colors ${
              currentCategory === 'hairstyles'
                ? 'bg-purple-600/30 border-purple-500/50 text-purple-200'
                : 'bg-gray-600/20 border-gray-500/30 text-gray-300 hover:bg-gray-600/30'
            }`}
          >
            💇 Hairstyles
          </button>
          <button
            onClick={() => setCurrentCategory('clothing')}
            className={`p-2 text-xs rounded-lg border transition-colors ${
              currentCategory === 'clothing'
                ? 'bg-blue-600/30 border-blue-500/50 text-blue-200'
                : 'bg-blue-600/20 border-blue-500/30 text-blue-300 hover:bg-blue-600/30'
            }`}
          >
            👔 Clothing
          </button>
          <button
            onClick={() => setCurrentCategory('accessories')}
            className={`p-2 text-xs rounded-lg border transition-colors ${
              currentCategory === 'accessories'
                ? 'bg-green-600/30 border-green-500/50 text-green-200'
                : 'bg-green-600/20 border-green-500/30 text-green-300 hover:bg-green-600/30'
            }`}
          >
            👓 Accessories
          </button>
        </div>
      </div>

      {/* Preset Buttons */}
      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-300 mb-3">
          {currentCategory === 'hairstyles' && 'Popular Hairstyles'}
          {currentCategory === 'clothing' && 'Clothing Options'}
          {currentCategory === 'accessories' && 'Accessory Options'}
        </h4>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-64 overflow-y-auto">
          {currentCategory === 'hairstyles' && HAIRSTYLE_PRESETS.map((style) => (
            <button
              key={style.id}
              onClick={() => handlePresetSelect(style.id)}
              className={`p-2 text-xs rounded-lg border transition-colors ${
                selectedStyle?.presetId === style.id
                  ? 'bg-purple-600 border-purple-500 text-white'
                  : 'bg-gray-700 border-gray-600 text-gray-300 hover:bg-gray-600 hover:border-gray-500'
              }`}
              title={style.description}
            >
              <div className="font-medium">{style.name}</div>
              <div className="text-xs opacity-75">{style.category}</div>
            </button>
          ))}
          {currentCategory === 'clothing' && CLOTHING_PRESETS.map((style) => (
            <button
              key={style.id}
              onClick={() => handlePresetSelect(style.id)}
              className={`p-2 text-xs rounded-lg border transition-colors ${
                selectedStyle?.presetId === style.id
                  ? 'bg-blue-600 border-blue-500 text-white'
                  : 'bg-gray-700 border-gray-600 text-gray-300 hover:bg-gray-600 hover:border-gray-500'
              }`}
              title={style.description}
            >
              <div className="font-medium">{style.name}</div>
              <div className="text-xs opacity-75">{style.category}</div>
            </button>
          ))}
          {currentCategory === 'accessories' && ACCESSORY_PRESETS.map((style) => (
            <button
              key={style.id}
              onClick={() => handlePresetSelect(style.id)}
              className={`p-2 text-xs rounded-lg border transition-colors ${
                selectedStyle?.presetId === style.id
                  ? 'bg-green-600 border-green-500 text-white'
                  : 'bg-gray-700 border-gray-600 text-gray-300 hover:bg-gray-600 hover:border-gray-500'
              }`}
              title={style.description}
            >
              <div className="font-medium">{style.name}</div>
              <div className="text-xs opacity-75">{style.category}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Options */}
      <div className="mt-4 space-y-2">
        <button
          onClick={() => setShowCustomInput(!showCustomInput)}
          className="w-full bg-gray-700 hover:bg-gray-600 text-gray-300 py-2 px-4 rounded-lg transition-colors text-sm"
        >
          {showCustomInput ? 'Hide Custom Options' : 'Custom Style Options'}
        </button>

        {showCustomInput && (
          <div className="space-y-3">
            {/* Custom Text Input */}
            <div>
              <input
                type="text"
                value={customText}
                onChange={(e) => setCustomText(e.target.value)}
                placeholder="Describe your desired hairstyle, clothing, or accessory..."
                className="w-full p-2 bg-gray-700 border border-gray-600 rounded-lg text-gray-100 placeholder-gray-400 focus:border-purple-500 focus:outline-none"
                onKeyPress={(e) => e.key === 'Enter' && handleCustomSubmit()}
              />
              <button
                onClick={handleCustomSubmit}
                disabled={!customText.trim()}
                className="mt-2 w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-2 px-4 rounded-lg transition-colors text-sm"
              >
                Apply Custom Style
              </button>
            </div>

            {/* Camera Capture for Style Items */}
            {!isCameraActive ? (
              <button
                onClick={startCamera}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors text-sm flex items-center justify-center gap-2"
              >
                📷 Take Photo of Item
              </button>
            ) : (
              <div className="space-y-2">
                <div className="relative bg-gray-900 rounded-lg p-4">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-32 object-cover rounded-lg"
                    style={{ backgroundColor: '#000' }}
                  />
                  <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 flex gap-2">
                    <button
                      onClick={captureStylePhoto}
                      className="bg-white text-black px-3 py-1 rounded-full font-semibold hover:bg-gray-200 transition-colors text-xs"
                    >
                      📸 Capture
                    </button>
                    <button
                      onClick={stopCamera}
                      className="bg-red-600 text-white px-3 py-1 rounded-full font-semibold hover:bg-red-700 transition-colors text-xs"
                    >
                      ✕ Cancel
                    </button>
                  </div>
                </div>
                {cameraError && (
                  <div className="text-red-400 text-xs text-center">
                    {cameraError}
                  </div>
                )}
              </div>
            )}

            {/* Image Upload */}
            <div>
              <input
                type="file"
                id="style-image-upload"
                className="hidden"
                accept="image/png, image/jpeg, image/webp"
                onChange={handleImageUpload}
              />
              <label
                htmlFor="style-image-upload"
                className="block w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors text-sm cursor-pointer text-center"
              >
                📁 Upload Style Image
              </label>
            </div>
          </div>
        )}

        {/* Hidden canvas for camera capture */}
        <canvas ref={canvasRef} className="hidden" />
      </div>
    </div>
  );
};
