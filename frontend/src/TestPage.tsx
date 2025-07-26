import React, { useState } from 'react';
import { AudioTester } from './components/AudioTester';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export const TestPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'audio'>('chat');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              Project Raseed 🧾 - Test Interface
            </h1>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveTab('chat')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'chat'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                💬 Chat Interface
              </button>
              <button
                onClick={() => setActiveTab('audio')}
                className={`px-4 py-2 rounded-lg font-medium ${
                  activeTab === 'audio'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                🎤 Audio Tester
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {activeTab === 'chat' ? (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">💬 Chat Interface</h2>
            <p className="text-gray-600 mb-4">
              Use the chat interface to test both image and audio uploads. You can:
            </p>
            <ul className="list-disc list-inside text-gray-600 mb-6 space-y-1">
              <li>Upload receipt images</li>
              <li>Record or upload audio files</li>
              <li>Combine text, images, and audio in one message</li>
              <li>Get responses from your AI agent</li>
            </ul>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-blue-800">
                <strong>Note:</strong> The chat interface is integrated into the main App.tsx file. 
                To use it, navigate to the main application.
              </p>
            </div>
          </div>
        ) : (
          <AudioTester backendUrl={BACKEND_URL} />
        )}
      </main>

      <footer className="bg-white border-t mt-8">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Project Raseed - Financial Insights with Audio Processing
          </p>
        </div>
      </footer>
    </div>
  );
}; 