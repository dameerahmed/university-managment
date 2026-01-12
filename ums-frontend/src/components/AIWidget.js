import React, { useState } from 'react';
import { MessageSquare, X, Bot } from 'lucide-react';

const AIWidget = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end font-sans">

            {/* Chat Window */}
            <div
                className={`
          transition-all duration-300 ease-in-out origin-bottom-right
          ${isOpen ? 'scale-100 opacity-100 mb-4' : 'scale-0 opacity-0 mb-0 h-0 overflow-hidden'}
          bg-white rounded-2xl shadow-2xl border border-gray-200 w-[400px] h-[600px] flex flex-col overflow-hidden
        `}
            >
                {/* Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 flex justify-between items-center shrink-0">
                    <div className="flex items-center gap-3">
                        <div className="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
                            <Bot className="text-white" size={24} />
                        </div>
                        <div>
                            <h3 className="text-white font-bold text-lg leading-tight">AI Assistant</h3>
                            <p className="text-blue-100 text-xs">Powered by Gemini 2.5</p>
                        </div>
                    </div>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="text-white/80 hover:text-white hover:bg-white/10 p-1 rounded-lg transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Iframe Container */}
                <div className="flex-1 bg-gray-50 relative">
                    <iframe
                        src="http://localhost:8001"
                        title="AI Agent"
                        className="w-full h-full border-none"
                    />
                    {/* Loading Placeholder (visible while iframe loads) */}
                    <div className="absolute inset-0 -z-10 flex items-center justify-center text-gray-400">
                        Loading Agent...
                    </div>
                </div>
            </div>

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
          h-16 w-16 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95
          ${isOpen ? 'bg-gray-800 rotate-90' : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-blue-500/50'}
        `}
            >
                {isOpen ? (
                    <X className="text-white" size={32} />
                ) : (
                    <MessageSquare className="text-white" size={32} />
                )}
            </button>
        </div>
    );
};

export default AIWidget;
