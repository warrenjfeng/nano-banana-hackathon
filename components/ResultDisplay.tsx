
import React from 'react';
import type { GenerationResult } from '../types';
import { Spinner } from './Spinner';

interface ResultDisplayProps {
  loading: boolean;
  error: string | null;
  result: GenerationResult | null;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ loading, error, result }) => {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center text-center p-8 bg-gray-800 rounded-lg border border-gray-700">
        <Spinner />
        <p className="mt-4 text-lg font-semibold text-gray-300">Generating your new look...</p>
        <p className="text-sm text-gray-400">This might take a moment. The AI is working its magic!</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-8 bg-red-900/20 border border-red-500 rounded-lg">
        <h3 className="text-xl font-bold text-red-400">An Error Occurred</h3>
        <p className="mt-2 text-red-300">{error}</p>
      </div>
    );
  }

  if (result) {
    return (
      <div className="p-4 sm:p-8 bg-gray-800 rounded-lg border border-gray-700 shadow-2xl">
        <h2 className="text-2xl sm:text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
          Your Style Result!
        </h2>
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-5 gap-8">
            <div className="lg:col-span-3">
                 <img src={result.imageUrl} alt="Generated style" className="w-full rounded-lg shadow-lg" />
            </div>
            <div className="lg:col-span-2 flex flex-col justify-center">
                <h4 className="font-semibold text-lg text-gray-200">AI Comments:</h4>
                <p className="mt-2 text-gray-300 bg-gray-700/50 p-4 rounded-md">{result.text}</p>
            </div>
        </div>
      </div>
    );
  }

  return (
    <div className="text-center p-8 bg-gray-800/50 rounded-lg border border-dashed border-gray-700">
        <h3 className="text-lg font-medium text-gray-400">Your generated image will appear here.</h3>
        <p className="text-sm text-gray-500">Upload both images and click "Generate My Style" to begin.</p>
    </div>
  );
};
