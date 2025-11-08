import type { NextPage } from 'next';
import Head from 'next/head';
import styles from '../styles/Home.module.css';
import { Geist, Geist_Mono } from "next/font/google";
import { useState, FormEvent } from 'react';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

interface Message {
  sender: 'user' | 'ai';
  text: string;
}

const ChatPage: NextPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    setIsLoading(true);
    const userMessage: Message = { sender: 'user', text: userInput };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setUserInput('');

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiResponseText = '';

      setMessages(prevMessages => [...prevMessages, { sender: 'ai', text: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        aiResponseText += chunk;
        setMessages(prevMessages => {
          const lastMessage = prevMessages[prevMessages.length - 1];
          if (lastMessage.sender === 'ai') {
            return [
              ...prevMessages.slice(0, -1),
              { ...lastMessage, text: aiResponseText },
            ];
          }
          return prevMessages;
        });
      }
    } catch (error) {
      console.error("Error fetching chat response:", error);
      setMessages(prevMessages => [...prevMessages, { sender: 'ai', text: "Sorry, I'm having trouble connecting." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`${styles.page} ${geistSans.variable} ${geistMono.variable}`}>
      <Head>
        <title>Chat with AI Assistant</title>
        <meta name="description" content="Chat with the AI Teacher Assistant" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <div className={styles.intro}>
          <h1>
            Chat with Your AI Assistant
          </h1>
          <p>
            Ask questions about your curriculum, generate lesson plan ideas, or get help with activities.
          </p>
        </div>

        <div className="chat-container">
          <div className="message-history">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <p>{msg.text}</p>
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmit} className="chat-input">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
};

export default ChatPage;
