import React, { useState, useRef, useEffect, type ChangeEvent, type FormEvent } from 'react';
import { AgentMessage } from './components/AgentMessage';
import { Paperclip, SendHorizonal, XCircle } from 'lucide-react';

// Define the structure for a chat message
interface Message {
  id: number;
  role: 'user' | 'agent';
  text: string;
  imageUrl?: string;
}

// Define the expected structure of the API response
interface ApiResponse {
  status: string;
  response_text: string;
  session_id?: string;
}

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

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
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
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

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedText = inputValue.trim();
    if (!trimmedText && !selectedFile) return;

    setIsLoading(true);

    const userMessage: Message = {
      id: getNextId(),
      role: 'user',
      text: trimmedText,
      imageUrl: selectedFile ? URL.createObjectURL(selectedFile) : undefined,
    };

    // --- FIX IS HERE ---
    // The FormData field names must match the backend API
    const formData = new FormData();
    formData.append('query', trimmedText); // Changed 'text' to 'query'
    if (selectedFile) {
      formData.append('images', selectedFile); // Changed 'image' to 'images'
    }
    // --- END OF FIX ---

    console.log('📤 Sending query:', trimmedText);
    if (selectedFile) {
      console.log('📎 Sending file:', selectedFile.name);
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
    <div className="flex h-screen flex-col bg-gray-50 font-sans">
      <header className="border-b bg-white p-4 shadow-sm">
        <h1 className="text-xl font-bold text-gray-800 text-center">
          Project Raseed 🧾
        </h1>
      </header>

      <main
        ref={chatContainerRef}
        className="flex-1 space-y-6 overflow-y-auto p-4 md:p-6"
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
              <div className="flex max-w-sm flex-col items-end gap-2">
                <div className="rounded-lg rounded-br-none bg-blue-500 p-3 text-white whitespace-pre-wrap">
                  {msg.imageUrl && (
                    <img
                      src={msg.imageUrl}
                      alt="Uploaded receipt"
                      className="mb-2 rounded-lg max-h-48"
                    />
                  )}
                  <p className="whitespace-pre-wrap">{msg.text || '...'}</p>
                </div>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-700 text-white font-bold">
                R
              </div>
              <div className="rounded-lg rounded-tl-none bg-gray-200 p-3 text-gray-800">
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

      <footer className="border-t bg-white p-2 md:p-4">
        <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
          {selectedFile && (
            <div className="mb-2 flex items-center justify-between rounded-lg bg-gray-100 p-2 text-sm">
              <span className="truncate text-gray-600">
                {selectedFile.name}
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
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="p-2 text-gray-500 hover:text-blue-500 disabled:opacity-50"
              disabled={isLoading}
            >
              <Paperclip size={20} />
            </button>
            <button
              type="submit"
              className="rounded-md bg-blue-500 p-2 text-white shadow-sm transition-colors hover:bg-blue-600 disabled:bg-blue-300"
              disabled={isLoading || (!inputValue.trim() && !selectedFile)}
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