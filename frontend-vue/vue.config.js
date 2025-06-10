// frontend-vue/vue.config.js

const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    host: "0.0.0.0", // This makes the development server listen on all network interfaces
    client: {
      // IMPORTANT: Adjust the port here (e.g., 8080 or 5173) based on your Vue app's actual port
      // Check the "Ports" tab in Codespaces to confirm your Vue frontend's port.
      webSocketURL: "wss://0.0.0.0:8080/ws", // This fixes the HMR WebSocket connection over HTTPS
    },
    // The proxy configuration to redirect API requests to your FastAPI backend
    proxy: {
      "/api": {
        // Any request from your frontend to /api will be proxied
        target: "http://localhost:8000", // Your FastAPI backend's internal URL
        changeOrigin: true, // Needed for virtual hosted sites
        secure: false, // For HTTPS backend, though Codespaces handles this
        pathRewrite: { "^/api": "" }, // Rewrite the path: remove /api when forwarding to backend
      },
    },
    // In some cases, this might also be needed (uncomment if issues persist)
    // disableHostCheck: true,
  },
});
