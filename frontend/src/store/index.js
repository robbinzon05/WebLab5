import { createStore } from 'vuex';

export default createStore({
  state: {
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload.user;
      state.accessToken = payload.access;
      state.refreshToken = payload.refresh;
      localStorage.setItem('user', JSON.stringify(payload.user));
      localStorage.setItem('accessToken', payload.access);
      localStorage.setItem('refreshToken', payload.refresh);
    },
    clearUser(state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
  actions: {
    async register({ dispatch }, userData) {
      const url = 'http://localhost:8000/api/auth/register/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || 'Ошибка при регистрации');
        }

        // После успешной регистрации автоматически выполняем логин
        await dispatch('login', {
          username: userData.username,
          password: userData.password,
        });

        return result;
      } catch (error) {
        console.error('Ошибка при регистрации:', error);
        throw error;
      }
    },
    async login({ commit }, credentials) {
      const url = 'http://localhost:8000/api/auth/login/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(credentials),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || 'Ошибка при авторизации');
        }

        // Проверяем, что в ответе есть пользовательские данные
        if (!result.user) {
          throw new Error('Не удалось получить данные пользователя');
        }

        // Сохраняем данные о пользователе и токенах
        commit('setUser', {
          user: result.user,
          access: result.access,
          refresh: result.refresh,
        });

        return result;
      } catch (error) {
        console.error('Ошибка при авторизации:', error);
        throw error;
      }
    },
    logout({ commit }) {
      commit('clearUser');
    },
    async refreshToken({ state, commit }) {
      const url = 'http://localhost:8000/api/auth/token/refresh/'; // Замените на ваш URL
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: state.refreshToken }),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || 'Ошибка обновления токена');
        }

        commit('setUser', {
          user: state.user, // Предполагается, что user уже известен
          access: result.access,
          refresh: state.refreshToken,
        });

        return result;
      } catch (error) {
        console.error('Ошибка обновления токена:', error);
        commit('clearUser');
        throw error;
      }
    },
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    getUser:  state => state.user
  },
});
