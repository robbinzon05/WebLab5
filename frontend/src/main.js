import { createApp } from 'vue'; // Импорт Vue
import App from './App.vue'; // Главный компонент приложения
import router from './router'; // Импорт маршрутизатора
import store from './store'; // Импорт Vuex хранилища
import axios from 'axios'; // Импорт Axios для запросов

// Добавление токена в заголовки всех запросов Axios
axios.interceptors.request.use(config => {
  const token = store.state.accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Добавляем токен в заголовок Authorization
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Создаем экземпляр приложения Vue
const app = createApp(App);

// Подключаем Vue Router и Vuex
app.use(router);
app.use(store);

// Монтируем приложение
app.mount('#app');
