import apiRequest from '../services/api'
import { useEffect, useState } from 'react'

interface Provider {
    id: number;
    name: string;
    status: string;
    location: string;
}

interface ApiRequest {
  endpoint: string
  method: string
  body?: string
}

const ProviderList: React.FC = () => {
  const [messages, setMessages] = useState([]); // State to store incoming data chunks

  useEffect(() => {
    // 1. Define the async function inside useEffect or as a separate const
    const startStreaming = async () => {
      try {
        const response = await fetch("http://localhost:8000/providers/stream");
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop(); // Keep partial line for next chunk

          for (const line of lines) {
            if (line.trim()) {
              const jsonObject = JSON.parse(line);
              
              // 2. Update React state as each chunk arrives
              setMessages((prev) => [...prev, jsonObject]);
            }
          }
        }
      } catch (error) {
        console.error("Streaming error:", error);
      }
    };

    startStreaming();
  }, []);

  return (
    <div>
      <h1>Provider List</h1>
      <ul className="provider-list">
        {messages.map((m, index) => (
          <li key={index}>{JSON.stringify(m)}</li>
        ))}
      </ul>
    </div>
  );
};

export default ProviderList;

