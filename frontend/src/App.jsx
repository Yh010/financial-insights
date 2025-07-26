import { useState } from 'react';
import Navbar from './components/Navbar';
import ChatPage from './components/ChatPage';
import UploadPage from './components/UploadPage';

function App() {
    const [activeTab, setActiveTab] = useState('Dashboard');

    let content;
    if (activeTab === 'Dashboard') content = <div className="flex justify-center items-center min-h-[60vh] text-2xl text-gray-400">Dashboard coming soon...</div>;
    else if (activeTab === 'Chat') content = <ChatPage />;
    else if (activeTab === 'Upload') content = <UploadPage />;
    else content = <div className="flex justify-center items-center min-h-[60vh] text-2xl text-gray-400">Coming soon...</div>;

    return (
        <div className="min-h-screen bg-gradient-to-br from-background via-muted/30 to-background">
            <Navbar activeTab={activeTab} onTabChange={setActiveTab} />
            <main className="max-w-5xl mx-auto w-full px-4 py-8">
                {content}
            </main>
        </div>
    );
}

export default App; 