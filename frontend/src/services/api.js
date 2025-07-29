// frontend/src/services/api.js

import axios from 'axios';

// Get the API base URL from environment variables
// VITE_API_BASE_URL is exposed by Vite (note the VITE_ prefix)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout
  withCredentials: true, // Important for sending cookies (session IDs) with requests
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Optional: Add request interceptors (e.g., for adding tokens)
api.interceptors.request.use(
  (config) => {
    // If you implement JWTs instead of sessions, you'd add the token here:
    // const token = localStorage.getItem('authToken');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optional: Add response interceptors (e.g., for global error handling, refreshing tokens)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('API Error:', error.response.status, error.response.data);
      if (error.response.status === 401 && error.response.data.message !== "Invalid username or password") {
        // Handle unauthorized (e.g., redirect to login)
        // This is a common pattern, but be careful not to create redirect loops
        // if your current page is already login.
        console.warn("Unauthorized: Session might have expired. Redirecting to login...");
        // You would typically use React Router's navigate here, or dispatch a global event.
        // For now, just a console warning.
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API No Response:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('API Request Setup Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;