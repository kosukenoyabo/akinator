import React, { useState, useEffect } from 'react';
import { initializeGame, chatWithGPT } from './api';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const initialize = async () => {
      try {
        const message = await initializeGame();
        setMessages([{ role: 'assistant', content: message }]);
      } catch (error) {
        console.error('Error initializing the game:', error);
      }
    };

    initialize();
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages([...messages, { role: 'user', content: input }]);
    setLoading(true);

    try {
      const response = await chatWithGPT(input);
      setMessages((prev) => [...prev, { role: 'assistant', content: response }]);
    } catch (error) {
      console.error('Error chatting with GPT:', error);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <div>
      <h1>Akinator Game</h1>
      <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ margin: '10px 0' }}>
            <strong>{msg.role === 'user' ? 'You' : 'Akinator'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={loading}
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
}

export default App;
