import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css'; // Стили по умолчанию

const app = createApp(App);

app.use(router);
app.use(Toast, {
  timeout: 3000, // Длительность показа уведомления (мс)
  position: 'top-right', // Позиция (top-right, bottom-left и т.д.)
});

app.mount('#app');