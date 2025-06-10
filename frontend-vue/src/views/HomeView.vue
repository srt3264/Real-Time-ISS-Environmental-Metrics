<template>
  <div class="test-container">
    <h1>Simple API & WebSocket Test (Vue.js)</h1>

    <div class="card">
      <h2>HTTP API Test (Root Path `/`)</h2>
      <p>Status: {{ httpMessage }}</p>
      <p class="caption">
        Try visiting {{ BACKEND_HTTP_URL }} in your browser directly.
      </p>
    </div>

    <div class="card">
      <h2>WebSocket Test (`/ws/echo`)</h2>
      <p>Status: {{ wsStatus }}</p>
      <div class="messages-box">
        <p v-for="(msg, index) in wsMessages" :key="index" :class="msg.type">
          {{ msg.text }}
        </p>
      </div>
      <div class="input-send">
        <input
          type="text"
          v-model="wsInput"
          placeholder="Message to Server"
          @keyup.enter="sendWsMessage"
        />
        <button @click="sendWsMessage">Send</button>
      </div>
      <p class="caption">WebSocket URL: {{ BACKEND_WS_URL }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

// --- IMPORTANT: Adjust these URLs based on your Codespace! ---
const BACKEND_HTTP_URL = "/api"; // This will now be proxied to your FastAPI backend's root
const BACKEND_WS_URL =
  "wss://curly-space-orbit-9rw97jj7j54cx7q-8000.app.github.dev/ws/echo";
// -----------------------------------------------------------

const httpMessage = ref("Fetching HTTP...");
const wsMessages = ref([]);
const wsInput = ref("");
const wsStatus = ref("Connecting...");
let ws = null; // Declare ws outside to be accessible for cleanup

// --- HTTP Test ---
onMounted(async () => {
  try {
    const response = await fetch(BACKEND_HTTP_URL);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    httpMessage.value = `HTTP Success: ${data.message} (Server Time: ${data.server_time})`;
  } catch (error) {
    httpMessage.value = `HTTP Error: ${error.message}. Is backend running on ${BACKEND_HTTP_URL}?`;
    console.error("HTTP fetch error:", error);
  }
});

// --- WebSocket Test ---
onMounted(() => {
  ws = new WebSocket(BACKEND_WS_URL);

  ws.onopen = () => {
    console.log("WebSocket Connected!");
    wsStatus.value = "Connected!";
    wsMessages.value.push({ type: "system", text: "WebSocket Connected!" });
  };

  ws.onmessage = (event) => {
    console.log("WS Message:", event.data);
    wsMessages.value.push({ type: "server", text: event.data });
  };

  ws.onclose = (event) => {
    console.log("WebSocket Disconnected:", event);
    wsStatus.value = `Disconnected: Code ${event.code}`;
    wsMessages.value.push({
      type: "system",
      text: `WebSocket Disconnected: Code ${event.code}`,
    });
  };

  ws.onerror = (error) => {
    console.error("WebSocket Error:", error);
    wsStatus.value = "Error! Check console.";
    wsMessages.value.push({
      type: "system",
      text: `WebSocket Error: ${error.message || "Unknown"}`,
    });
  };
});

// Cleanup: Close WebSocket when component unmounts
onUnmounted(() => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    console.log("Closing WebSocket...");
    ws.close();
  }
});

const sendWsMessage = () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(wsInput.value);
    wsMessages.value.push({ type: "client", text: `You: ${wsInput.value}` });
    wsInput.value = "";
  } else {
    wsMessages.value.push({
      type: "system",
      text: "WebSocket not open. Cannot send message.",
    });
  }
};
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.card {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #34495e;
  margin-top: 0;
  margin-bottom: 15px;
}

p {
  margin: 5px 0;
}

.caption {
  font-size: 0.85em;
  color: #666;
  margin-top: 10px;
}

.messages-box {
  border: 1px solid #eee;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
  background-color: #fff;
  margin-top: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
}

.messages-box p {
  word-wrap: break-word;
}

.messages-box .system {
  color: #888;
  font-style: italic;
}

.messages-box .client {
  color: #2196f3; /* Blue */
  font-weight: bold;
}

.messages-box .server {
  color: #4caf50; /* Green */
}

.input-send {
  display: flex;
  gap: 10px;
}

.input-send input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.input-send button {
  padding: 8px 15px;
  background-color: #42b983; /* Vue Green */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.input-send button:hover {
  background-color: #368a6f;
}
</style>
