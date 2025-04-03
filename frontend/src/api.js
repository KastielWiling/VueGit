import axios from 'axios';
import router from '@/router'; // Импортируйте router

const api = axios.create({
  baseURL: 'http://localhost:8000', // URL вашего FastAPI сервера
});

// Добавляем токен в заголовки запросов
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const originalRequest = error.config;
    
    // Игнорируем ошибки для эндпоинтов авторизации и логирования
    const ignoredEndpoints = ['/token/', '/admin/activity'];
    if (ignoredEndpoints.some(endpoint => originalRequest.url.includes(endpoint))) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      localStorage.removeItem('token');
      router.push('/login');
    }
    
    return Promise.reject(error);
  }
);

export default api;