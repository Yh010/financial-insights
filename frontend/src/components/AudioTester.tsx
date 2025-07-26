import React, { useState, useRef } from 'react';
import { Mic, MicOff, Upload, Play, Download } from 'lucide-react';

interface AudioTesterProps {
  backendUrl: string;
}

interface TestResult {
  endpoint: string;
  success: boolean;
  data?: any;
  error?: string;
}

export const AudioTester: React.FC<AudioTesterProps> = ({ backendUrl }) => {
  const [selectedAudioFile, setSelectedAudioFile] = useState<File | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [receiptData, setReceiptData] = useState<any>(null);
  const [walletUrl, setWalletUrl] = useState('');

  const audioInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const handleAudioFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedAudioFile(event.target.files[0]);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      const chunks: Blob[] = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        const audioFile = new File([audioBlob], 'recorded_audio.webm', { type: 'audio/webm' });
        setSelectedAudioFile(audioFile);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleAudioToggle = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const testEndpoint = async (endpoint: string, formData: FormData): Promise<TestResult> => {
    try {
      const response = await fetch(`${backendUrl}${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        return {
          endpoint,
          success: false,
          error: `HTTP ${response.status}: ${errorText}`
        };
      }

      const data = await response.json();
      return {
        endpoint,
        success: true,
        data
      };
    } catch (error) {
      return {
        endpoint,
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  };

  const runAllTests = async () => {
    if (!selectedAudioFile) {
      alert('Please select or record an audio file first');
      return;
    }

    setIsLoading(true);
    setTestResults([]);
    setTranscript('');
    setReceiptData(null);
    setWalletUrl('');

    const results: TestResult[] = [];

    // Test 1: Audio Transcription
    const transcriptionFormData = new FormData();
    transcriptionFormData.append('audio_file', selectedAudioFile);
    transcriptionFormData.append('language_code', 'en-US');
    
    const transcriptionResult = await testEndpoint('/audio/transcribe', transcriptionFormData);
    results.push(transcriptionResult);
    
    if (transcriptionResult.success) {
      setTranscript(transcriptionResult.data.transcript);
    }

    // Test 2: Audio Receipt Processing
    const receiptFormData = new FormData();
    receiptFormData.append('audio_file', selectedAudioFile);
    receiptFormData.append('language_code', 'en-US');
    
    const receiptResult = await testEndpoint('/audio/process-receipt', receiptFormData);
    results.push(receiptResult);
    
    if (receiptResult.success) {
      setReceiptData(receiptResult.data.receipt_data);
    }

    // Test 3: Complete Audio to Wallet Pass
    const walletFormData = new FormData();
    walletFormData.append('audio_file', selectedAudioFile);
    walletFormData.append('language_code', 'en-US');
    
    const walletResult = await testEndpoint('/audio/create-pass-from-audio', walletFormData);
    results.push(walletResult);
    
    if (walletResult.success) {
      setWalletUrl(walletResult.data.wallet_save_url);
    }

    setTestResults(results);
    setIsLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">🎤 Audio Features Tester</h2>
      
      {/* Audio Input Section */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">Audio Input</h3>
        
        <div className="flex flex-wrap gap-4 items-center">
          {/* File Upload */}
          <div className="flex items-center gap-2">
            <input
              type="file"
              ref={audioInputRef}
              onChange={handleAudioFileChange}
              accept="audio/*"
              className="hidden"
            />
            <button
              onClick={() => audioInputRef.current?.click()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              <Upload size={16} />
              Upload Audio
            </button>
          </div>

          {/* Recording */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleAudioToggle}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                isRecording 
                  ? 'bg-red-500 text-white hover:bg-red-600' 
                  : 'bg-green-500 text-white hover:bg-green-600'
              }`}
            >
              {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </button>
          </div>

          {/* Selected File Display */}
          {selectedAudioFile && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Play size={16} />
              {selectedAudioFile.name} ({(selectedAudioFile.size / 1024).toFixed(1)} KB)
            </div>
          )}
        </div>

        {/* Audio Preview */}
        {selectedAudioFile && (
          <div className="mt-4">
            <audio controls className="w-full">
              <source src={URL.createObjectURL(selectedAudioFile)} type={selectedAudioFile.type} />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </div>

      {/* Test Controls */}
      <div className="mb-6 text-center">
        <button
          onClick={runAllTests}
          disabled={!selectedAudioFile || isLoading}
          className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Testing...' : 'Run All Audio Tests'}
        </button>
      </div>

      {/* Test Results */}
      {testResults.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Test Results</h3>
          
          <div className="space-y-4">
            {testResults.map((result, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border ${
                  result.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold">{result.endpoint}</h4>
                  <span className={`px-2 py-1 rounded text-sm ${
                    result.success ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'
                  }`}>
                    {result.success ? '✅ Success' : '❌ Failed'}
                  </span>
                </div>
                
                {result.success ? (
                  <pre className="text-sm bg-white p-2 rounded border overflow-x-auto">
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                ) : (
                  <p className="text-red-600">{result.error}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Extracted Data Display */}
      {(transcript || receiptData || walletUrl) && (
        <div className="space-y-4">
          {/* Transcript */}
          {transcript && (
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold mb-2">📝 Transcript</h4>
              <p className="text-gray-700">{transcript}</p>
            </div>
          )}

          {/* Receipt Data */}
          {receiptData && (
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h4 className="font-semibold mb-2">🧾 Receipt Data</h4>
              <pre className="text-sm bg-white p-2 rounded border overflow-x-auto">
                {JSON.stringify(receiptData, null, 2)}
              </pre>
            </div>
          )}

          {/* Wallet URL */}
          {walletUrl && (
            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-semibold mb-2">💳 Wallet Pass</h4>
              <div className="flex items-center gap-2">
                <a
                  href={walletUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Open Wallet Pass
                </a>
                <button
                  onClick={() => navigator.clipboard.writeText(walletUrl)}
                  className="px-2 py-1 bg-gray-200 rounded text-sm hover:bg-gray-300"
                >
                  Copy URL
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}; 