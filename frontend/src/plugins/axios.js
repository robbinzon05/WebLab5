// frontend/src/plugins/axios.js

import axios from 'axios';
import store from '../store';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Замените на ваш URL
});

// Добавляем интерцептор для добавления токена к каждому запросу
instance.interceptors.request.use(
  config => {
    const token = store.state.accessToken;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Добавляем интерцептор для обработки ошибок 401 и обновления токена
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await store.dispatch('refreshToken');
        originalRequest.headers['Authorization'] = `Bearer ${store.state.accessToken}`;
        return instance(originalRequest);
      } catch (err) {
        store.dispatch('logout');
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default instance;
