import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // Импортируем роутер

// Создаем приложение и подключаем роутер
createApp(App)
  .use(router)  // Используем роутер
  .mount('#app');