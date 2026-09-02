import './App.css'
import ReactMarkdown from 'react-markdown';
import { useState, useEffect, useRef } from 'react'
import ElizaIcon from './assets/Eliza-icon.png'

// Разграничаване на сесиите на потребителите:
const getOrCreateSessionId = () => {
  let id = localStorage.getItem('sirma_chat_session');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('sirma_chat_session', id);
  }
  return id;
};

function App() {

  const [session_id] = useState(getOrCreateSessionId());

  const [messages, setMessages] = useState([
    {sender: 'bot', text: 'Здравейте! Аз съм Eliza, вашият AI асистент. С какво мога да ви помогна днес?'},
  ]);

  const [inputText, setInputText] = useState('');

  const [isLoading, setIsLoading] = useState(false);

  //Чатът се скролва автоматично при нов въпрос:

  const messagesEndRef = useRef(null);

  const ScrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({behavior: 'smooth', block: 'end'});
    }, 50);
  };

  useEffect(() => {
    ScrollToBottom();
  }, [messages, isLoading]);

  const suggestedQuestions = [
    "С какво се занимава Sirma?",
    "Какви типове клиенти обслужвате?",
    "Какво представлява Sirma AI.Enterprise?"
  ];

  const sendMessage = async (textToSend = null) => {

    const userMessage = typeof textToSend === 'string' ? textToSend : inputText;

    if (!userMessage.trim()) return;
    
    setMessages(prevMessages => [...prevMessages, { sender: 'user', text: userMessage }]);

    if (typeof textToSend !== 'string') {
      setInputText('');
    }
    setIsLoading(true);
    
    // Създаване на заявка към backend сървъра за обработка на съобщението от потребителя
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: session_id,
          message: userMessage,
        }),
      });

      const data = await response.json();

      setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: data.reply }]);

    } catch (error) {
      console.error('Грешка при изпращане на съобщението:', error);
      setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: 'Възникна грешка при свързване със сървъра' }]);
    
    } finally {
      setIsLoading(false);
    }
  };

  // Може да изпращаме съобщения, натискайки enter:
  const handlePressEnter = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <img src={ElizaIcon} alt="Eliza" className="chat-icon" />
        <p> Eliza AI Sirma Assistant</p>
      </header>
      
      <main className="chat-window">
        {messages.map((message, index) => ( // Визуализиране на съобщенията с движението на чата
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-bubble">
              <ReactMarkdown>{message.text}</ReactMarkdown>
            </div>
          </div>
        ))}

       {/* Докато подаваме заявка към backend сървъра, показваме индикатор за зареждане */}
        {isLoading && (
          <div className="message bot">
            <div className="message-bubble">
              <div className="loading-indicator">
                <div className="spinner"></div>
                <span>Eliza пише...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref = {messagesEndRef} />
      </main>


      <div className="suggested-questions-container">
        {suggestedQuestions.map((question, index) => (
          <button
            key={index}
            className="suggested-question"
            onClick={() => sendMessage(question)}
            disabled={isLoading}
          >
            {question}
          </button>
        ))}
      </div>

      <footer className="chat-input-area">
        <input 
          type="text" 
          placeholder="Напишете съобщение..." 
          className="chat-input"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handlePressEnter}
        />
        <button 
          className="send-button"
          onClick={sendMessage}
          disabled={isLoading}
        > Изпрати
        </button>
      </footer>
    </div>
  );
}

export default App