import React, { useState, useEffect } from 'react';
import type { ImageFile, StyleRequest, GenerationResult } from '../types';
import { getHairstyleById } from '../constants/hairstyles';

interface HistoryEntry {
  id: string;
  timestamp: number;
  personImageUrl: string; // Store as data URL instead of base64
  styleRequest: StyleRequest;
  result: GenerationResult;
}

interface HistoryPanelProps {
  onLoadEntry: (entry: HistoryEntry) => void;
  currentPersonImage?: ImageFile | null;
  currentStyleRequest?: StyleRequest | null;
  currentResult?: GenerationResult | null;
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({ 
  onLoadEntry, 
  currentPersonImage, 
  currentStyleRequest, 
  currentResult 
}) => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('virtual-try-on-history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (error) {
        console.error('Error loading history:', error);
        // Clear corrupted history
        localStorage.removeItem('virtual-try-on-history');
        setHistory([]);
      }
    }
  }, []);

  // Save current result to history when it changes
  useEffect(() => {
    if (currentResult && currentPersonImage && currentStyleRequest) {
      const newEntry: HistoryEntry = {
        id: Date.now().toString(),
        timestamp: Date.now(),
        personImageUrl: `data:${currentPersonImage.mimeType};base64,${currentPersonImage.base64}`,
        styleRequest: currentStyleRequest,
        result: currentResult
      };

      setHistory(prev => {
        const updated = [newEntry, ...prev].slice(0, 5); // Keep only last 5 entries to save space
        try {
          localStorage.setItem('virtual-try-on-history', JSON.stringify(updated));
        } catch (error) {
          console.error('Error saving history:', error);
          // If storage fails, keep only the most recent entry
          const minimalHistory = [newEntry];
          try {
            localStorage.setItem('virtual-try-on-history', JSON.stringify(minimalHistory));
          } catch (minimalError) {
            console.error('Error saving minimal history:', minimalError);
            // Clear history if even minimal storage fails
            localStorage.removeItem('virtual-try-on-history');
          }
          return minimalHistory;
        }
        return updated;
      });
    }
  }, [currentResult, currentPersonImage, currentStyleRequest]);

  const getStyleDisplayName = (styleRequest: StyleRequest): string => {
    if (styleRequest.type === 'image') return 'Custom Image';
    if (styleRequest.presetId) {
      const preset = getHairstyleById(styleRequest.presetId);
      return preset?.name || 'Unknown Preset';
    }
    return styleRequest.text || 'Custom Text';
  };

  const formatDate = (timestamp: number): string => {
    return new Date(timestamp).toLocaleString();
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('virtual-try-on-history');
  };

  if (history.length === 0 && !isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 bg-gray-700 hover:bg-gray-600 text-white p-3 rounded-full shadow-lg transition-colors"
        title="View History"
      >
        📚
      </button>
    );
  }

  return (
    <div className={`fixed bottom-4 right-4 transition-all duration-300 ${
      isOpen ? 'w-80 h-96' : 'w-12 h-12'
    }`}>
      {isOpen ? (
        <div className="bg-gray-800 border border-gray-600 rounded-lg shadow-xl h-full flex flex-col">
          <div className="flex items-center justify-between p-3 border-b border-gray-600">
            <h3 className="text-lg font-semibold text-gray-100">History</h3>
            <div className="flex gap-2">
              {history.length > 0 && (
                <button
                  onClick={clearHistory}
                  className="text-red-400 hover:text-red-300 text-sm"
                  title="Clear History"
                >
                  🗑️
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-300"
              >
                ✕
              </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-3">
            {history.length === 0 ? (
              <p className="text-gray-400 text-sm text-center py-8">
                No history yet. Generate some styles to see them here!
              </p>
            ) : (
              <div className="space-y-3">
                {history.map((entry) => (
                  <div
                    key={entry.id}
                    className="bg-gray-700 rounded-lg p-3 cursor-pointer hover:bg-gray-600 transition-colors"
                    onClick={() => onLoadEntry(entry)}
                  >
                    <div className="flex gap-3">
                      <img
                        src={entry.personImageUrl}
                        alt="Person"
                        className="w-12 h-12 object-cover rounded"
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-100 truncate">
                          {getStyleDisplayName(entry.styleRequest)}
                        </p>
                        <p className="text-xs text-gray-400">
                          {formatDate(entry.timestamp)}
                        </p>
                      </div>
                      <img
                        src={entry.result.imageUrl}
                        alt="Result"
                        className="w-12 h-12 object-cover rounded"
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="w-12 h-12 bg-gray-700 hover:bg-gray-600 text-white rounded-full shadow-lg transition-colors flex items-center justify-center"
          title="View History"
        >
          📚
        </button>
      )}
    </div>
  );
};
