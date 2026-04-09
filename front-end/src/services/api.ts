interface ApiRequest {
  endpoint: string
  method: string
  body?: string
}

const apiRequest = async (api_request: ApiRequest) => {
  const endpoint = api_request.endpoint;
  const method = api_request.method;
  const body = api_request.body;

  const url = 'http://127.0.0.1:8000' + endpoint;

  var options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': 'Bearer YOUR_TOKEN' // Add auth here if needed
    },
  };

  // Only add a body for methods like POST or PUT
  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    console.log(response.text)
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

const fetchStream = async (endpoint: string) => {
  const response = await fetch("http://localhost:8000" + endpoint);
  
  // 1. Get the reader from the response body
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer: string | undefined = ""; // To hold partial chunks

  while (true) {
    // 2. Read the next chunk of data
    const { value, done } = await reader.read();
    if (done) break;

    // 3. Decode the chunk and add it to our buffer
    buffer += decoder.decode(value, { stream: true });

    // 4. Split the buffer by newlines to find complete JSON objects
    const lines: string[] | undefined = buffer.split("\n");

    // The last element in 'lines' might be an incomplete JSON string
    // Keep it in the buffer for the next chunk to complete it
    buffer = lines.pop();

    for (const line of lines) {
      if (line.trim()) {
        try {
          const jsonObject = JSON.parse(line);
          console.log("New data arrived:", jsonObject);
          // 5. Update your React state with this single object
        } catch (e) {
          console.error("Error parsing individual line:", e);
        }
      }
    }
  }
};

export default apiRequest;
// export default fetchStream;

