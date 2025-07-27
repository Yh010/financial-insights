import React, { useState, useRef, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { AgentMessage } from './components/AgentMessage';
import { Paperclip, SendHorizonal, XCircle, Mic, MicOff } from 'lucide-react';

// Define the structure for a chat message
interface Message {
  id: number;
  role: 'user' | 'agent';
  text: string;
  imageUrl?: string;
  audioUrl?: string;
  audioFileName?: string;
}

// Define the expected structure of the API response
interface ApiResponse {
  status: string;
  response_text: string;
  session_id?: string;
}

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL; // Placeholder for demo

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'agent',
      text:
        'Welcome to Raseed! How can I help you today? Please upload a receipt or ask a question.',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedAudioFile, setSelectedAudioFile] = useState<File | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const audioInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const messageIdCounter = useRef(messages.length + 1);

  useEffect(() => {
    if (chatContainerRef.current) {
      const { scrollHeight, clientHeight } = chatContainerRef.current;
      chatContainerRef.current.scrollTop = scrollHeight - clientHeight;
    }
  }, [messages, isLoading]);

  const getNextId = () => {
    messageIdCounter.current += 1;
    return messageIdCounter.current;
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleAudioFileChange = (event: ChangeEvent<HTMLInputElement>) => {
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

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedText = inputValue.trim();
    if (!trimmedText && !selectedFile && !selectedAudioFile) return;

    setIsLoading(true);

    const userMessage: Message = {
      id: getNextId(),
      role: 'user',
      text: trimmedText,
      imageUrl: selectedFile ? URL.createObjectURL(selectedFile) : undefined,
      audioUrl: selectedAudioFile ? URL.createObjectURL(selectedAudioFile) : undefined,
      audioFileName: selectedAudioFile?.name,
    };

    // --- FIX IS HERE ---
    // The FormData field names must match the backend API
    const formData = new FormData();
    formData.append('query', trimmedText); // Changed 'text' to 'query'
    if (selectedFile) {
      formData.append('images', selectedFile); // Changed 'image' to 'images'
    }
    if (selectedAudioFile) {
      formData.append('audio_files', selectedAudioFile); // Add audio files
    }
    // --- END OF FIX ---

    console.log('📤 Sending query:', trimmedText);
    if (selectedFile) {
      console.log('📎 Sending image file:', selectedFile.name);
    }
    if (selectedAudioFile) {
      console.log('🎤 Sending audio file:', selectedAudioFile.name);
    }

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      console.log('✅ API response:', data);

      if (!data || typeof data.response_text !== 'string') {
        throw new Error('Invalid API response format');
      }

      const agentMessage: Message = {
        id: getNextId(),
        role: 'agent',
        text: data.response_text || 'Sorry, I couldn’t understand that.',
      };

      setMessages((prev) => [...prev, agentMessage]);
      setInputValue('');
      setSelectedFile(null);
      setSelectedAudioFile(null);
    } catch (error) {
      console.error('❌ Error during fetch:', error);

      setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));

      const errorMessage: Message = {
        id: getNextId(),
        role: 'agent',
        text: 'Sorry, something went wrong. Please try again.',
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen flex-col bg-gray-100 font-sans relative overflow-hidden">
      {/* Background geometric shapes */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Blue curved shape - bottom left */}
        <div className="absolute -bottom-32 -left-32 w-96 h-96 bg-gradient-to-tr from-blue-500 to-blue-600 rounded-full opacity-80"></div>
        
        {/* Red curved shape - top right */}
        <div className="absolute -top-24 -right-24 w-80 h-80 bg-gradient-to-bl from-red-500 to-red-600 rounded-full opacity-75"></div>
        
        {/* Green shape - middle left */}
        <div className="absolute top-1/3 left-1/4 w-48 h-48 bg-gradient-to-br from-green-500 to-green-600 rounded-full opacity-30"></div>
        
        {/* Yellow shape - bottom right */}
        <div className="absolute bottom-1/4 right-1/3 w-32 h-32 bg-gradient-to-tr from-yellow-400 to-yellow-500 rounded-full opacity-40"></div>
        
        {/* Additional subtle Google color accents */}
        <div className="absolute top-1/2 right-1/5 w-24 h-24 bg-gradient-to-bl from-blue-400 to-blue-500 rounded-full opacity-20"></div>
        <div className="absolute bottom-1/3 left-1/5 w-20 h-20 bg-gradient-to-tr from-green-400 to-green-500 rounded-full opacity-25"></div>
      </div>

      <header className="border-b bg-white/90 backdrop-blur-sm p-4 shadow-sm relative z-10">
        <div className="flex justify-center items-center">
          <h1 className="text-xl font-bold text-gray-800">
            Project <span className="text-blue-500">R</span><span className="text-red-500">a</span><span className="text-yellow-500">s</span><span className="text-blue-500">e</span><span className="text-green-500">e</span><span className="text-red-500">d</span> 🧾
          </h1>
        </div>
      </header>

      <main
        ref={chatContainerRef}
        className="flex-1 space-y-6 overflow-y-auto p-4 md:p-6 relative z-10"
      >
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.role === 'agent' ? (
              <AgentMessage content={msg.text || '...'} />
            ) : (
              <div className="flex max-w-sm flex-col items-end gap-2 min-w-0">
                <div className="rounded-lg rounded-br-none bg-blue-500 p-3 text-white break-words overflow-hidden">
                  {msg.imageUrl && (
                    <img
                      src={msg.imageUrl}
                      alt="Uploaded receipt"
                      className="mb-2 rounded-lg max-h-48 max-w-full object-contain"
                    />
                  )}
                  {msg.audioUrl && (
                    <div className="mb-2 flex items-center gap-2 rounded-lg bg-blue-600 p-2 min-w-0">
                      <Mic size={16} className="shrink-0" />
                      <span className="text-sm truncate">{msg.audioFileName || 'Audio file'}</span>
                      <audio controls className="max-w-full min-w-0">
                        <source src={msg.audioUrl} type="audio/webm" />
                        Your browser does not support the audio element.
                      </audio>
                    </div>
                  )}
                  <p className="whitespace-pre-wrap break-words">{msg.text || '...'}</p>
                </div>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start max-w-full">
            <div className="flex items-start gap-3 max-w-full">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-700 text-white font-bold">
                R
              </div>
              <div className="rounded-lg rounded-tl-none bg-gray-200 p-3 text-gray-800 min-w-0">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 animate-pulse rounded-full bg-gray-500"></div>
                  <div className="h-2 w-2 animate-pulse rounded-full bg-gray-500 [animation-delay:0.2s]"></div>
                  <div className="h-2 w-2 animate-pulse rounded-full bg-gray-500 [animation-delay:0.4s]"></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="border-t bg-white/90 backdrop-blur-sm p-2 md:p-4 relative z-10">
        <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
          {selectedFile && (
            <div className="mb-2 flex items-center justify-between rounded-lg bg-gray-100 p-2 text-sm">
              <span className="truncate text-gray-600">
                📎 {selectedFile.name}
              </span>
              <button
                type="button"
                onClick={() => setSelectedFile(null)}
                className="text-gray-500 hover:text-red-500"
              >
                <XCircle size={18} />
              </button>
            </div>
          )}
          {selectedAudioFile && (
            <div className="mb-2 flex items-center justify-between rounded-lg bg-green-100 p-2 text-sm">
              <span className="truncate text-gray-600">
                🎤 {selectedAudioFile.name}
              </span>
              <button
                type="button"
                onClick={() => setSelectedAudioFile(null)}
                className="text-gray-500 hover:text-red-500"
              >
                <XCircle size={18} />
              </button>
            </div>
          )}
          <div className="flex items-center rounded-lg border bg-white p-1">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message or upload a receipt..."
              className="flex-1 appearance-none bg-transparent px-3 py-2 text-gray-700 outline-none"
              disabled={isLoading}
            />
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  const file = e.target.files[0];
                  if (file.type.startsWith('image/')) {
                    setSelectedFile(file);
                  } else if (file.type.startsWith('audio/')) {
                    setSelectedAudioFile(file);
                  }
                }
              }}
              accept="image/*,audio/*"
              className="hidden"
            />
            <input
              type="file"
              ref={audioInputRef}
              onChange={handleAudioFileChange}
              accept="audio/*"
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="p-2 text-gray-500 hover:text-blue-500 disabled:opacity-50"
              disabled={isLoading}
              title="Upload image or audio file"
            >
              <Paperclip size={20} />
            </button>
            <button
              type="button"
              onClick={handleAudioToggle}
              className={`p-2 disabled:opacity-50 ${
                isRecording 
                  ? 'text-red-500 hover:text-red-600' 
                  : 'text-gray-500 hover:text-green-500'
              }`}
              disabled={isLoading}
              title={isRecording ? 'Stop recording' : 'Start recording'}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            <button
              type="submit"
              className="rounded-md bg-blue-500 p-2 text-white shadow-sm transition-colors hover:bg-blue-600 disabled:bg-blue-300"
              disabled={isLoading || (!inputValue.trim() && !selectedFile && !selectedAudioFile)}
            >
              <SendHorizonal size={20} />
            </button>
          </div>
        </form>
      </footer>
    </div>
  );
}

export default App;