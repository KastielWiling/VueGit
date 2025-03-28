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
    if (error.response && error.response.status === 401) {
      // Токен истек или недействителен
      localStorage.removeItem('token');
      router.push('/login'); // Перенаправляем на страницу авторизации
    }
    return Promise.reject(error);
  }
);

export default api;