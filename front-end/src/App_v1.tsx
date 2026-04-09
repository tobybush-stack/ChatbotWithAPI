import React, { useState, useEffect } from 'react';

// 1. Define the Type to match Python's Pydantic model
interface Provider {
  id: number;
  name: string;
  status: string;
}

const ProviderDashboard: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([]);

  // 2. The Fetcher
  const loadData = async () => {
    const res = await fetch('/providers');
    setProviders(await res.json());
  };

  useEffect(() => {
    loadData();
    // 3. Senior Move: Poll every 2 seconds to see if "Syncing" finished
    const interval = setInterval(loadData, 2000);
    return () => clearInterval(interval);
  }, []);

  const triggerSync = (id: number) => fetch(`/sync/${id}`, { method: 'POST' });

  return (
    <div>
      <h1>Provider BI Dashboard</h1>
      {providers.map(p => (
        <div key={p.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
          <h3>{p.name} - <small>{p.status}</small></h3>
          <button onClick={() => triggerSync(p.id)} disabled={p.status === "Syncing..."}>
            {p.status === "Syncing..." ? "Processing..." : "Sync Data"}
          </button>
        </div>
      ))}
    </div>
  );
};

export default ProviderDashboard;

