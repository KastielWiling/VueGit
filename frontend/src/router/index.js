import { createRouter, createWebHistory } from 'vue-router';
import TaskList from '../components/TaskList.vue';
import UserManagement from '../components/UserManagement.vue';


// Определение маршрутов
const routes = [
  { path: '/', component: TaskList },  // Главная страница с задачами
  { path: '/admin', component: UserManagement },  // Админская панель
];

// Создание роутера
const router = createRouter({
  history: createWebHistory(),  // Используем HTML5 History API
  routes,  // Передаем массив маршрутов
});

export default router;