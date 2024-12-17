import { createStore } from 'vuex';

export default createStore({
  state: {
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  },
  mutations: {
    setUser (state, payload) {
      state.user = payload.user;
      state.accessToken = payload.access;
      state.refreshToken = payload.refresh;
      localStorage.setItem('user', JSON.stringify(payload.user));
      localStorage.setItem('accessToken', payload.access);
      localStorage.setItem('refreshToken', payload.refresh);
    },
    clearUser (state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
  actions: {
    async register({ commit }, userData) {
      const url = 'http://localhost:8080/api/auth/register/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.password || 'Ошибка при регистрации');
        }

        const result = await response.json();
        commit('setUser ', {
          user: result.user,
          access: result.access,
          refresh: result.refresh,
        });
      } catch (error) {
        console.error('Ошибка при регистрации:', error);
        throw error; // Пробрасываем ошибку для обработки в компоненте
      }
    },
    async login({ commit }, credentials) {
      const url = 'http://localhost:8080/api/auth/login/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(credentials),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Ошибка при авторизации');
        }

        const result = await response.json();
        commit('setUser ', {
          user: result.user,
          access: result.access,
          refresh: result.refresh,
        });
      } catch (error) {
        console.error('Ошибка при авторизации:', error);
        throw error; // Пробрасываем ошибку для обработки в компоненте
      }
    },
    logout({ commit }) {
      commit('clearUser ');
    },
    async refreshToken({ state, commit }) {
      const url = 'http://localhost:8080/api/auth/token/refresh/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: state.refreshToken }),
        });

        if (!response.ok) {
          throw new Error('Ошибка обновления токена');
        }

        const result = await response.json();
        commit('setUser ', {
          user: state.user,
          access: result.access,
          refresh: state.refreshToken,
        });
      } catch (error) {
        console.error('Ошибка обновления токена:', error);
        commit('clearUser '); // Очистка пользователя при ошибке
      }
    },
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    getUser: state => state.user,
  },
});