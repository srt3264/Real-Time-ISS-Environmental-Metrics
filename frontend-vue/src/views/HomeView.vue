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

    <div class="card">
      <h2>Solar Wind Data Viewer (`/api/data/solar_wind`)</h2>
      <p v-if="solarWindLoading">Loading...</p>
      <p v-if="!solarWindLoading && solarWindData.length === 0">
        No solar wind data available for this time range.
      </p>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th v-for="(value, key) in solarWindData[0]" :key="key">
              {{ key }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in solarWindData" :key="index">
            <td v-for="(value, colKey) in row" :key="colKey">{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

// --- API URLs ---
const BACKEND_HTTP_URL = "/api";
const BACKEND_WS_URL =
  "wss://curly-space-orbit-9rw97jj7j54cx7q-8000.app.github.dev/ws/echo";

// --- HTTP Test ---
const httpMessage = ref("Fetching HTTP...");
onMounted(async () => {
  try {
    const response = await fetch(BACKEND_HTTP_URL);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    httpMessage.value = `HTTP Success: ${data.message} (Server Time: ${data.server_time})`;
  } catch (error) {
    httpMessage.value = `HTTP Error: ${error.message}`;
    console.error("HTTP fetch error:", error);
  }
});

// --- WebSocket Test ---
const wsMessages = ref([]);
const wsInput = ref("");
const wsStatus = ref("Connecting...");
let ws = null;

onMounted(() => {
  ws = new WebSocket(BACKEND_WS_URL);

  ws.onopen = () => {
    wsStatus.value = "Connected!";
    wsMessages.value.push({ type: "system", text: "WebSocket Connected!" });
  };

  ws.onmessage = (event) => {
    wsMessages.value.push({ type: "server", text: event.data });
  };

  ws.onclose = (event) => {
    wsStatus.value = `Disconnected: Code ${event.code}`;
    wsMessages.value.push({
      type: "system",
      text: `WebSocket Disconnected: Code ${event.code}`,
    });
  };

  ws.onerror = (error) => {
    wsStatus.value = "Error! Check console.";
    wsMessages.value.push({
      type: "system",
      text: `WebSocket Error: ${error.message || "Unknown"}`,
    });
  };
});

onUnmounted(() => {
  if (ws && ws.readyState === WebSocket.OPEN) {
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

// --- Solar Wind Data Viewer ---
const solarWindData = ref([]);
const solarWindLoading = ref(true);

onMounted(async () => {
  try {
    const now = new Date();
    const end = now.toISOString();
    const start = new Date(
      now.getTime() - 7 * 24 * 60 * 60 * 1000
    ).toISOString();

    const res = await fetch(
      `${BACKEND_HTTP_URL}/data/solar_wind?start_time=${start}&end_time=${end}`
    );

    if (!res.ok) throw new Error(`Status ${res.status}`);

    const data = await res.json();
    solarWindData.value = data;
    console.log("Fetched solar wind data:", data);
  } catch (err) {
    console.error("Error fetching solar wind data:", err);
  } finally {
    solarWindLoading.value = false;
  }
});
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
  color: #2196f3;
  font-weight: bold;
}

.messages-box .server {
  color: #4caf50;
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
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.input-send button:hover {
  background-color: #368a6f;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.data-table th,
.data-table td {
  border: 1px solid #ccc;
  padding: 6px 10px;
  text-align: left;
  font-size: 0.9em;
}

.data-table th {
  background-color: #eee;
}
</style>
