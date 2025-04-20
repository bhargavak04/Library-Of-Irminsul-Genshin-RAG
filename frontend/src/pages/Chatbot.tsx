import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function Chatbot() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<{ type: 'user' | 'bot'; content: string }[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  
  // Function to scroll to bottom of chat
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };
  
  // Scroll to bottom whenever chat updates
  useEffect(() => {
    scrollToBottom();
  }, [chat]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message to chat
    setChat(prev => [...prev, { type: 'user', content: message }]);
    
    // Clear input field
    const userInput = message;
    setMessage('');
    
    // Show loading state
    setIsLoading(true);
    
    try {
      // Send message to API
      const response = await fetch('http://localhost:10000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userInput,
          session_id: sessionId
        }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      
      // Update session ID if we don't have one yet
      if (!sessionId) {
        setSessionId(data.session_id);
      }
      
      // Add bot response to chat
      setChat(prev => [...prev, { type: 'bot', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message to chat
      setChat(prev => [...prev, { 
        type: 'bot', 
        content: "Sorry, I couldn't connect to the knowledge network. Please try again later." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to start a new conversation
  const handleNewConversation = () => {
    setChat([]);
    setSessionId(null);
  };

  return (
    <div className="min-h-screen bg-chatbot bg-black/95 text-white p-8">
      <div className="max-w-4xl mx-auto pt-24">
        <h1 className="title text-4xl text-[#DEB887] mb-8 text-center">Ask Akasha</h1>
        
        <div 
          ref={chatContainerRef}
          className="bg-black/60 rounded-lg border border-[#DEB887]/30 h-[60vh] mb-6 p-6 overflow-y-auto"
        >
          {chat.map((msg, idx) => (
            <div key={idx} className={`mb-4 ${msg.type === 'bot' ? 'text-left' : 'text-right'}`}>
              <div className={`inline-block max-w-[80%] p-4 rounded-lg ${
                msg.type === 'bot' 
                  ? 'bg-[#DEB887]/20 text-white' 
                  : 'bg-[#DEB887]/40 text-white'
              }`}>
                {msg.type === 'bot' ? (
                  <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown
                      components={{
                        // Style headings
                        h1: ({node, ...props}) => <h1 className="text-xl font-bold text-[#DEB887] mb-2" {...props} />,
                        h2: ({node, ...props}) => <h2 className="text-lg font-bold text-[#DEB887] mb-2" {...props} />,
                        h3: ({node, ...props}) => <h3 className="text-base font-bold text-[#DEB887] mb-1" {...props} />,
                        // Style lists
                        ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2" {...props} />,
                        ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2" {...props} />,
                        // Style paragraphs
                        p: ({node, ...props}) => <p className="mb-2" {...props} />,
                        // Style emphasis
                        strong: ({node, ...props}) => <strong className="font-bold text-[#DEB887]" {...props} />
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="bg-[#DEB887]/20 text-white p-4 rounded-lg flex items-center">
                <div className="flex space-x-2">
                  <div className="h-2 w-2 bg-[#DEB887]/60 rounded-full animate-bounce"></div>
                  <div className="h-2 w-2 bg-[#DEB887]/60 rounded-full animate-bounce delay-75"></div>
                  <div className="h-2 w-2 bg-[#DEB887]/60 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about Genshin Impact lore..."
            className="flex-1 bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-3 text-white placeholder:text-white/50 focus:outline-none focus:border-[#DEB887]"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className={`btn-primary px-6 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={isLoading}
          >
            <Send className="w-6 h-6" />
          </button>
        </form>
      </div>
    </div>
  );
}