const fetchStream = async (endpoint: string, setMessages: any) => {
 try {
        const response = await fetch("http://localhost:8000" + endpoint);
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
              // console.log(line)
              const jsonObject = JSON.parse(line);
              // var jsonObject = ''
              // try {
              //   jsonObject = JSON.parse(line);
              // } catch {
              //   jsonObject = line;
              // };
              
              // 2. Update React state as each chunk arrives
              // const jsonObjectClean = jsonObject.replaceAll('\"', 'double-quote').replaceAll('"', '').replaceAll('double-quote', '"');
              setMessages((prev) => [...prev, jsonObject]);
            }
          }
        }
      } catch (error) {
        console.error("Streaming error:", error);
      };
};

export default fetchStream;

