import axios from "axios";

const api = axios.create({
  baseURL: "https://agrishield-5j83.onrender.com", 
});

// Attach auth token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
