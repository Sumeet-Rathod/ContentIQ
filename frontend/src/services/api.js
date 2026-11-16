import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercept requests to attach JWT bearer token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('contentiq_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercept responses for auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid or expired
      localStorage.removeItem('contentiq_token');
      localStorage.removeItem('contentiq_user');
      localStorage.removeItem('contentiq_tenant');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (payload) => api.post('/auth/register', payload),
  getMe: () => api.get('/auth/me'),
};

export const postsApi = {
  getPosts: (params) => api.get('/posts', { params }),
  getPost: (id) => api.get(`/posts/${id}`),
  createPost: (data) => api.post('/posts', data),
  updatePost: (id, data) => api.put(`/posts/${id}`, data),
  deletePost: (id) => api.delete(`/posts/${id}`),
};

export const teamApi = {
  getMembers: () => api.get('/team/members'),
  inviteMember: (data) => api.post('/team/invite', data),
  updateRole: (userId, role) => api.put(`/team/members/${userId}/role`, { role }),
};

export const predictionApi = {
  scorePost: (payload) => api.post('/predictions/score', payload),
  getBestTime: (payload) => api.post('/predictions/best-time', payload),
  explainPost: (payload) => api.post('/predictions/explain', payload),
};

export const intelligenceApi = {
  scoreThumbnail: (formData) =>
    api.post('/intelligence/thumbnail/score', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getTrends: () => api.get('/intelligence/trends'),
  getRecommendations: (niche) =>
    api.get('/intelligence/recommendations', { params: niche ? { niche } : {} }),
  getForecast: (platform = 'instagram', daysAhead = 30) =>
    api.get('/intelligence/forecast', { params: { platform, days_ahead: daysAhead } }),
  addSnapshot: (data) => api.post('/intelligence/forecast/snapshots', data),
  importSnapshotCsv: (formData) =>
    api.post('/intelligence/forecast/import-csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
};

export const analyticsApi = {
  getDashboard: () => api.get('/analytics/dashboard'),
};

export const feedbackApi = {
  logMetrics: (data) => api.post('/feedback/metrics', data),
  importMetricsCsv: (formData) =>
    api.post('/feedback/metrics/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  retrainModel: () => api.post('/feedback/retrain'),
  createABTest: (data) => api.post('/feedback/ab-tests', data),
  getABTests: () => api.get('/feedback/ab-tests'),
  getABTest: (id) => api.get(`/feedback/ab-tests/${id}`),
  addCompetitor: (data) => api.post('/feedback/competitors', data),
  getCompetitors: () => api.get('/feedback/competitors'),
  addComment: (data) => api.post('/feedback/comments', data),
  getComments: (postId) => api.get(`/feedback/comments/${postId}`),
};

export const notificationApi = {
  getNotifications: (unreadOnly = false) =>
    api.get('/notifications', { params: { unread_only: unreadOnly } }),
  markRead: (id) => api.put(`/notifications/${id}/read`),
  markAllRead: () => api.put('/notifications/read-all'),
};

export default api;
