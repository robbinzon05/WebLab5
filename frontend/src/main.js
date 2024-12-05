import { createApp } from 'vue'; // Импорт Vue
import App from './App.vue'; // Главный компонент приложения
import router from './router'; // Импорт маршрутизатора
import store from './store'; // Импорт Vuex хранилища
import axios from 'axios'; // Импорт Axios для запросов
import jwt_decode from 'jwt-decode'; // Для работы с токенами JWT

// Проверка срока действия токена при загрузке приложения
if (store.state.accessToken) {
  const decoded = jwt_decode(store.state.accessToken); // Расшифровка токена
  const exp = decoded.exp * 1000; // Конвертация времени истечения в миллисекунды
  const now = Date.now(); // Текущее время

  if (exp < now) {
    // Если токен истек, пробуем обновить
    store.dispatch('refreshToken');
  }
}

// Добавление токена в заголовки всех запросов Axios
axios.interceptors.request.use(config => {
  const token = store.state.accessToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Добавляем токен в заголовок Authorization
  }
  return config;
});

// Создаем экземпляр приложения Vue
const app = createApp(App);

// Подключаем Vue Router и Vuex
app.use(router);
app.use(store);

// Монтируем приложение
app.mount('#app');
