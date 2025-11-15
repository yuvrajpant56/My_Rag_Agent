'use client';

import { useState, FormEvent, useEffect, useRef } from 'react';

export default function Home() {
  const [question, setQuestion] = useState<string>('');
  const [ingestText, setIngestText] = useState<string>(''); // State for the text to ingest
  const [ingestStatus, setIngestStatus] = useState<string>(''); // To show ingestion status messages
  const [messages, setMessages] = useState<{ type: 'user' | 'bot'; text: string }[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handler for the new ingestion form
  const handleIngest = async (e: FormEvent) => {
    e.preventDefault();
    if (!ingestText.trim()) return;
    setIngestStatus('Ingesting...');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: ingestText }),
      });
      const result = await response.json();
      if (response.ok) {
        setIngestStatus(`Success: ${result.message}`);
        setIngestText('');
      } else {
        setIngestStatus(`Error: ${result.detail || 'Failed to ingest text.'}`);
      }
    } catch (error) {
      console.error('Ingestion error:', error);
      setIngestStatus('Error: Failed to connect to the server.');
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    setIsLoading(true);
    const userMessage = { type: 'user' as const, text: question };
    const botMessage = { type: 'bot' as const, text: '' };
    setMessages((prev) => [...prev, userMessage, botMessage]);
    
    setQuestion('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let leftover = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = leftover + decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        leftover = lines.pop() || '';

        for (const line of lines) {
          if (line.trim() === '') continue;
          if (line.startsWith('data: ')) {
            const messageContent = line.substring(6);
            setMessages((prev) =>
              prev.map((msg, index) =>
                index === prev.length - 1
                  ? { ...msg, text: msg.text + messageContent }
                  : msg
              )
            );
          }
        }
      }
    } catch (error) {
      console.error('Error fetching chat response:', error);
      setMessages((prev) =>
        prev.map((msg, index) =>
          index === prev.length - 1
            ? { ...msg, text: "Sorry, I encountered an error." }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4 shadow-md">
        <h1 className="text-2xl font-bold text-center">Agentic RAG Chatbot</h1>
        <p className="text-center text-sm text-gray-400">Powered by Anthropic, Qdrant & FastAPI</p>
      </header>

      {/* --- Ingestion Form --- */}
      <div className="bg-gray-800 p-4 border-b border-gray-700">
        <form onSubmit={handleIngest} className="max-w-3xl mx-auto">
          <h2 className="text-lg font-semibold mb-2">Add Knowledge</h2>
          <textarea
            value={ingestText}
            onChange={(e) => setIngestText(e.target.value)}
            placeholder="Paste text here to add it to the knowledge base..."
            className="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
          />
          <div className="flex justify-between items-center mt-2">
            <p className="text-sm text-gray-400">{ingestStatus}</p>
            <button
              type="submit"
              className="bg-green-600 text-white p-2 rounded-md hover:bg-green-700"
            >
              Ingest Text
            </button>
          </div>
        </form>
      </div>
      
      <main className="flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-3xl mx-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`flex my-4 ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`p-3 rounded-lg max-w-lg ${
                  msg.type === 'user' ? 'bg-blue-600' : 'bg-gray-700'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </main>
      
      <footer className="bg-gray-800 p-4 border-t border-gray-700">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 p-2 rounded-l-md bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-2 rounded-r-md hover:bg-blue-700 disabled:bg-blue-900 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </footer>
    </div>
  );
}

