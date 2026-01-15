import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { 
  Send, 
  User, 
  Bot, 
  Loader2, 
  Sparkles, 
  Copy, 
  Check,
  Menu,
  X
} from 'lucide-react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => Date.now().toString());
  const messagesEndRef = useRef(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [copiedId, setCopiedId] = useState(null);

  // Example questions
  const exampleQuestions = [
    "What is machine learning?",
    "Explain neural networks",
    "What are the types of ML algorithms?",
    "How does supervised learning work?",
    "What is deep learning?",
    "What is reinforcement learning?"
  ];

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message
    setMessages(prev => [...prev, {
      id: Date.now(),
      text: userMessage,
      sender: 'user',
      timestamp: new Date()
    }]);

    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage,
        session_id: sessionId
      });

      // Add bot response
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: response.data.answer,
        sender: 'bot',
        timestamp: new Date(),
        processingTime: response.data.processing_time
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = async (question) => {
    setInput(question);
    // Small delay to show the question in input field before sending
    setTimeout(() => {
      document.getElementById('send-button')?.click();
    }, 100);
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app-container">
      {/* Mobile Sidebar Toggle */}
      <button 
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-gray-800 rounded-lg"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Sparkles size={24} />
            </div>
            <div>
              <h1 className="text-xl font-bold">🤖 ML Chatbot</h1>
              <p className="text-sm text-gray-400">Ask me about Machine Learning</p>
            </div>
          </div>
        </div>

        <div className="sidebar-content">
          <div className="mb-6">
            <h2 className="text-sm font-semibold text-gray-400 mb-3">QUICK QUESTIONS</h2>
            <div className="space-y-2">
              {exampleQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickQuestion(question)}
                  className="w-full text-left p-3 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors text-sm"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-auto">
            <button
              onClick={clearChat}
              className="w-full p-3 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-colors flex items-center justify-center space-x-2"
            >
              <span>Clear Chat</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"></div>
            <div>
              <h2 className="font-semibold">Machine Learning Assistant</h2>
              <p className="text-sm text-gray-400">
                {messages.filter(m => m.sender === 'user').length} messages
              </p>
            </div>
          </div>
          <div className="text-sm text-gray-400">
            Powered by LangChain & Groq
          </div>
        </div>

        {/* Messages Container */}
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">
                <Sparkles size={48} />
              </div>
              <h3 className="empty-state-title">Welcome to ML Chatbot!</h3>
              <p className="empty-state-description">
                Ask me anything about Machine Learning. Try one of the example questions or type your own.
              </p>
              <div className="example-questions-grid">
                {exampleQuestions.slice(0, 3).map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickQuestion(question)}
                    className="example-question-button"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
              >
                <div className="message-avatar">
                  {message.sender === 'user' ? (
                    <div className="avatar-user">
                      <User size={16} />
                    </div>
                  ) : (
                    <div className="avatar-bot">
                      <Bot size={16} />
                    </div>
                  )}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {message.sender === 'user' ? 'You' : 'Medical Assistant'}
                    </span>
                    <span className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </span>
                  </div>
                  <div className="message-text">
                    <ReactMarkdown
                      components={{
                        code({node, inline, className, children, ...props}) {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <div className="code-block-wrapper">
                              <div className="code-header">
                                <span>{match[1]}</span>
                                <button
                                  onClick={() => copyToClipboard(String(children), message.id)}
                                  className="copy-button"
                                >
                                  {copiedId === message.id ? (
                                    <Check size={14} />
                                  ) : (
                                    <Copy size={14} />
                                  )}
                                </button>
                              </div>
                              <SyntaxHighlighter
                                style={vscDarkPlus}
                                language={match[1]}
                                PreTag="div"
                                {...props}
                              >
                                {String(children).replace(/\n$/, '')}
                              </SyntaxHighlighter>
                            </div>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        }
                      }}
                    >
                      {message.text}
                    </ReactMarkdown>
                  </div>
                  {message.processingTime && (
                    <div className="message-footer">
                      <span className="processing-time">
                        Processed in {message.processingTime}s
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="message bot">
              <div className="message-avatar">
                <div className="avatar-bot">
                  <Bot size={16} />
                </div>
              </div>
              <div className="message-content">
                <div className="message-header">
                  <span className="message-sender">ML Assistant</span>
                </div>
                <div className="thinking-indicator">
                  <Loader2 className="animate-spin" />
                  <span>Thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form onSubmit={handleSend} className="input-area">
          <div className="input-wrapper">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about medical info..."
              className="message-input"
              disabled={isLoading}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  handleSend(e);
                }
              }}
            />
            <button
              id="send-button"
              type="submit"
              disabled={isLoading || !input.trim()}
              className="send-button"
            >
              {isLoading ? (
                <Loader2 className="animate-spin" />
              ) : (
                <Send />
              )}
            </button>
          </div>
          <div className="input-hint">
            Press Enter to send • Shift + Enter for new line
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;