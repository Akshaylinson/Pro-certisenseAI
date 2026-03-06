import React, { useState } from 'react';

const AIChat = ({ userRole }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          message: input,
          user_role: userRole,
          user_id: 'current_user'
        })
      });

      const data = await response.json();
      const aiMessage = { 
        type: 'ai', 
        content: data.response || data.text_visualization || 'Response received'
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'ai', content: 'Error: Unable to get response' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ai-chat">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <strong>{msg.type === 'user' ? 'You' : '🤖 AI'}:</strong> {msg.content}
          </div>
        ))}
        
        {isLoading && (
          <div className="message ai loading">
            <strong>🤖 AI:</strong>
            <div className="thinking-animation">
              <span className="dot">●</span>
              <span className="dot">●</span>
              <span className="dot">●</span>
              <span className="text">Thinking...</span>
            </div>
          </div>
        )}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask AI about certificates, blockchain, or system..."
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>

      <style jsx>{`
        .ai-chat {
          max-width: 600px;
          margin: 20px auto;
          border: 1px solid #ddd;
          border-radius: 8px;
          overflow: hidden;
        }

        .chat-messages {
          height: 400px;
          overflow-y: auto;
          padding: 15px;
          background: #f9f9f9;
        }

        .message {
          margin-bottom: 15px;
          padding: 10px;
          border-radius: 6px;
        }

        .message.user {
          background: #e3f2fd;
          margin-left: 20%;
        }

        .message.ai {
          background: #f1f8e9;
          margin-right: 20%;
        }

        .thinking-animation {
          display: flex;
          align-items: center;
          gap: 5px;
        }

        .dot {
          animation: pulse 1.5s infinite;
          color: #4caf50;
          font-size: 20px;
        }

        .dot:nth-child(1) { animation-delay: 0s; }
        .dot:nth-child(2) { animation-delay: 0.3s; }
        .dot:nth-child(3) { animation-delay: 0.6s; }

        .text {
          margin-left: 10px;
          color: #666;
          font-style: italic;
        }

        @keyframes pulse {
          0%, 60%, 100% { opacity: 0.3; }
          30% { opacity: 1; }
        }

        .chat-input {
          display: flex;
          padding: 15px;
          background: white;
          border-top: 1px solid #ddd;
        }

        .chat-input input {
          flex: 1;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          margin-right: 10px;
        }

        .chat-input button {
          padding: 10px 15px;
          background: #2196f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .chat-input button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
};

export default AIChat;