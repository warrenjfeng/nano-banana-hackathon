import React, { useState, useCallback } from 'react';
import { Header } from './components/Header';
import { ImageUploader } from './components/ImageUploader';
import { StyleSelector } from './components/StyleSelector';
import { ResultDisplay } from './components/ResultDisplay';
import { Button } from './components/Button';
import { HistoryPanel } from './components/HistoryPanel';
import { ErrorBoundary } from './components/ErrorBoundary';
import type { ImageFile, GenerationResult, StyleRequest } from './types';
import { generateVirtualTryOn } from './services/geminiService';

const App: React.FC = () => {
  const [personImage, setPersonImage] = useState<ImageFile | null>(null);
  const [styleRequest, setStyleRequest] = useState<StyleRequest | null>(null);
  const [result, setResult] = useState<GenerationResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = useCallback(async () => {
    if (!personImage || !styleRequest) {
      setError('Please upload your photo and select a style before generating.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const generatedResult = await generateVirtualTryOn(personImage, styleRequest);
      setResult(generatedResult);
    } catch (e) {
      console.error(e);
      setError('Failed to generate the image. Please check the console for more details.');
    } finally {
      setIsLoading(false);
    }
  }, [personImage, styleRequest]);

  const handleLoadHistoryEntry = useCallback((entry: any) => {
    // Convert the personImageUrl back to ImageFile format
    const personImage: ImageFile = {
      base64: entry.personImageUrl.split(',')[1],
      mimeType: entry.personImageUrl.split(',')[0].split(':')[1].split(';')[0]
    };
    
    setPersonImage(personImage);
    setStyleRequest(entry.styleRequest);
    setResult(entry.result);
    setError(null);
  }, []);

  // Smart paste order: person first, then style
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
              const reader = new FileReader();
              reader.onload = () => {
                const base64String = (reader.result as string).split(',')[1];
                const imageData = { base64: base64String, mimeType: file.type };
                
                // Smart paste order: person image first, then style
                if (!personImage) {
                  // No person image yet, paste to person
                  setPersonImage(imageData);
                } else if (!styleRequest) {
                  // Person image exists but no style, paste to style
                  const styleRequest: StyleRequest = {
                    type: 'image',
                    image: imageData
                  };
                  setStyleRequest(styleRequest);
                } else {
                  // Both exist, replace style
                  const styleRequest: StyleRequest = {
                    type: 'image',
                    image: imageData
                  };
                  setStyleRequest(styleRequest);
                }
              };
              reader.readAsDataURL(file);
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
  }, [personImage, styleRequest]);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center p-4 sm:p-6 lg:p-8">
        <div className="w-full max-w-5xl mx-auto">
          <Header />

          <main className="mt-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <ImageUploader
                id="person-uploader"
                title="1. Upload Your Photo"
                description="A clear, front-facing photo works best."
                onImageUpload={setPersonImage}
                currentImage={personImage}
              />
              <StyleSelector
                onStyleSelect={setStyleRequest}
                selectedStyle={styleRequest}
              />
            </div>

            <div className="mt-8 text-center">
              <Button
                onClick={handleGenerate}
                disabled={!personImage || !styleRequest || isLoading}
                isLoading={isLoading}
              >
                {isLoading ? 'Styling in Progress...' : 'Generate My Style'}
              </Button>
            </div>
            
            <div className="mt-12">
              <ResultDisplay loading={isLoading} error={error} result={result} />
            </div>
          </main>
        </div>
        
        <HistoryPanel
          onLoadEntry={handleLoadHistoryEntry}
          currentPersonImage={personImage}
          currentStyleRequest={styleRequest}
          currentResult={result}
        />
      </div>
    </ErrorBoundary>
  );
};

export default App;