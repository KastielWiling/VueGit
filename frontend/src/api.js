// api.js
import axios from 'axios';
import router from '@/router';


const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Новый перехватчик для логирования действий
api.interceptors.response.use(
  async (response) => {
    // Логируем успешные CRUD операции
    if (['post', 'put', 'delete'].includes(response.config.method)) {
      try {
        const entityType = getEntityTypeFromUrl(response.config.url);
        if (entityType) {
          await logAction(
            response.config.method.toUpperCase(),
            entityType,
            response.data._id || response.config.data?.id,
            getActionDetails(response)
          );
        }
      } catch (error) {
        console.error('Error logging action:', error);
      }
    }
    return response;
  },
  (error) => {
    // Обработка ошибок (как было ранее)
    const originalRequest = error.config;
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

// Вспомогательные функции для логирования
function getEntityTypeFromUrl(url) {
  const entityMap = {
    'projects': 'project',
    'files': 'file',
    'estimates': 'estimate',
    'records': 'record'
  };
  for (const [path, type] of Object.entries(entityMap)) {
    if (url.includes(path)) return type;
  }
  return null;
}

function getActionDetails(response) {
  const { method, url } = response.config;
  const entityName = response.data?.name || response.data?.tag || '';
  return `${method.toUpperCase()} operation on ${url} ${entityName ? `(${entityName})` : ''}`;
}

async function logAction(action, entityType, entityId, details = '') {
  try {
    await api.post('/admin/activity', {
      action,
      entityType,
      entityId,
      details
    });
  } catch (error) {
    console.error('Failed to log action:', error);
  }
}

export default api;