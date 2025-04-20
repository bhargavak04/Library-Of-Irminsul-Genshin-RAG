import React, { useState } from 'react';
import { Send } from 'lucide-react';

export default function Chatbot() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<{ type: 'user' | 'bot'; content: string }[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setChat(prev => [...prev, { type: 'user', content: message }]);
    setMessage('');
    // Bot response simulation
    setTimeout(() => {
      setChat(prev => [...prev, { 
        type: 'bot', 
        content: "I'm still learning about Teyvat's vast history. Please check back soon!" 
      }]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-chatbot bg-black/95 text-white p-8">
      <div className="max-w-4xl mx-auto pt-24">
        <h1 className="title text-4xl text-[#DEB887] mb-8 text-center">Ask Akasha</h1>
        
        <div className="bg-black/60 rounded-lg border border-[#DEB887]/30 h-[60vh] mb-6 p-6 overflow-y-auto">
          {chat.map((msg, idx) => (
            <div key={idx} className={`mb-4 ${msg.type === 'bot' ? 'text-left' : 'text-right'}`}>
              <div className={`inline-block max-w-[80%] p-4 rounded-lg ${
                msg.type === 'bot' 
                  ? 'bg-[#DEB887]/20 text-white' 
                  : 'bg-[#DEB887]/40 text-white'
              }`}>
                {msg.content}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about Genshin Impact lore..."
            className="flex-1 bg-black/60 border border-[#DEB887]/30 rounded-lg px-4 py-3 text-white placeholder:text-white/50 focus:outline-none focus:border-[#DEB887]"
          />
          <button type="submit" className="btn-primary px-6">
            <Send className="w-6 h-6" />
          </button>
        </form>
      </div>
    </div>
  );
}