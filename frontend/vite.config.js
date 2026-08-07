import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Requests to /api/* are forwarded to the FastAPI backend, so the frontend
// code can use relative URLs like fetch("/api/search?q=ED").
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
