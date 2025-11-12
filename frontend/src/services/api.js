import axios from 'axios';

// In production (Docker), nginx proxies API calls
// In development, Vite proxy handles it
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  signup: (username, password) =>
    api.post('/api/auth/signup', { username, password }),

  login: (username, password) =>
    api.post('/api/auth/login', { username, password }),
};

// CSV APIs
export const csvAPI = {
  getAll: () => api.get('/api/csv'),

  getContent: (fileId) => api.get(`/api/csv/${fileId}`),

  download: (fileId) =>
    api.get(`/api/csv/${fileId}/download`, { responseType: 'blob' }),
};

// Admin APIs
export const adminAPI = {
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/admin/csv/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  deleteCSV: (fileId) => api.delete(`/api/admin/csv/${fileId}`),

  getUsers: () => api.get('/api/admin/users'),

  deleteUser: (userId) => api.delete(`/api/admin/users/${userId}`),

  getAllCSV: () => api.get('/api/admin/csv'),
};

export default api;
