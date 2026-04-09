import fetchStream from '../services/stream'
import { useEffect, useState } from 'react'

const ChatBot: React.FC = () => {
  const [messages, setMessages] = useState([]); // State to store incoming data chunks

  useEffect(() => {
    // 1. Define the async function inside useEffect or as a separate const
    const startStreaming = async () => {
        fetchStream('/llm/stream', setMessages)
    };

    startStreaming();
  }, []);

  return (
    <div>
      <h1>Response</h1>
      <ul className="provider-list">
        {messages.map((m, index) => (
          <li key={index}>{JSON.stringify(m)}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChatBot;

