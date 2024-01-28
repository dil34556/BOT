import React, { useState } from 'react';
import './App.css';

const ChatBot = () => {
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
    <div>
      <div className="chatbot-heading">
        <h1>ChatBot</h1>
      </div>

      {showPopup && (
        <div className="popup">
          <p>
            Use math, solve, equation prompt for the math tutor
            <button onClick={closePopup}>Close</button>
          </p>
        </div>
      )}

      <div className="main-chat">
        <div className="input-container">
          <input
            type="text"
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className={`send-button ${isLoading ? 'disabled' : ''}`}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        <div className="chat-messages">
          {userMessage && <p className="user-message">User: {userMessage}</p>}
          {botResponse && <p className="bot-message">Bot: {botResponse}</p>}
          {!botResponse && isLoading && <p className="typing-message">Bot is typing...</p>}
          {!botResponse && !isLoading && <p className="waiting-message">Waiting for bot response...</p>}
        </div>
      </div>

      <div className="right-panel">
        <h3>Previous Chat</h3>
        <div className="previous-chat">
          {conversationHistory.map((entry, index) => (
            <div key={index}>
              <p className="user-message">User: {entry.user}</p>
              <p className="bot-message">Bot: {entry.bot}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
