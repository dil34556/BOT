import React, { useState } from 'react';
import './App.css';

const Chat = () => {
  const [userMessage, setUserMessage] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [showPopup, setShowPopup] = useState(true);

  const sendMessage = async () => {
    if (!userMessage.trim()) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/chat/get-response/?message=${userMessage}`);
      const data = await response.json();
      setBotResponse(data.message);

      
      const updatedHistory = [...conversationHistory, { user: userMessage, bot: data.message }];
      setConversationHistory(updatedHistory);
    } catch (error) {
      console.error('Error fetching bot response:', error);
      setBotResponse('Oops! Something went wrong on our end.');
    } finally {
      setIsLoading(false);
    }
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  return (
    <div style={{ position: 'relative', display: 'flex', height: '100vh', backgroundColor: '#f4f4f4' }}>
      {}
      {showPopup && (
        <div style={{ position: 'absolute', top: '20px', right: '20px', backgroundColor: '#fff', padding: '10px', borderRadius: '8px', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
          <p>Use math,solve,eqution promt for math tutor <button onClick={closePopup}>Close</button></p>
        </div>
      )}

      {}
      <div style={{ flex: 1, padding: '20px', borderRadius: '8px', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
        <h2>DB CHATBOT</h2>
        <div style={{ width: '500px', marginLeft: 'auto', marginRight: 'auto' }}>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="Type your message..."
              style={{ width: '50%', height: '50%', padding: '8px', borderRadius: '15px', border: '1px solid #ccc' }}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading}
              style={{ padding: '8px', cursor: isLoading ? 'not-allowed' : 'pointer', borderRadius: '15px', backgroundColor: '#4CAF50', color: 'white', border: 'none' }}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
          <div>
            <p style={{ marginBottom: '5px' }}>User: {userMessage}</p>
            {botResponse && <p style={{ color: 'green' }}>Bot: {botResponse}</p>}
            {!botResponse && isLoading && <p style={{ fontStyle: 'italic' }}>Bot is typing...</p>}
            {!botResponse && !isLoading && <p style={{ fontStyle: 'italic' }}>Waiting for bot response...</p>}
          </div>
        </div>
      </div>
      {}
      <div style={{ flex: '0 0 200px', backgroundColor: '#ddd', padding: '20px' }}>
        <h3>Previous Chat</h3>
        {conversationHistory.map((entry, index) => (
          <div key={index}>
            <p>User: {entry.user}</p>
            <p style={{ color: 'green' }}>Bot: {entry.bot}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chat;
