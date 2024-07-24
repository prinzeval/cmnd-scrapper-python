// src/api.ts
import axios from "axios";

// Set the base URL for the API requests
const api = axios.create({
  baseURL: "http://localhost:8000", // Replace with your FastAPI backend URL
  headers: {
    "Content-Type": "application/json", // Ensure content type is set
  },
});

export default api;
