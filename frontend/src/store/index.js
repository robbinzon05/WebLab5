import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: JSON.parse(localStorage.getItem('user')) || null,
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
    async login({ commit }, credentials) {
        try {
            const response = await axios.post('/api/auth/login/', credentials);
            commit('setUser', {
                user: response.data.user,
                access: response.data.access,
                refresh: response.data.refresh,
            });
        } catch (error) {
            console.error('Ошибка при авторизации:', error);
            throw error;
        }
    },
    logout({ commit }) {
        commit('clearUser');
    },
    async refreshToken({ state, commit }) {
        try {
            const response = await axios.post('/api/auth/token/refresh/', {
                refresh: state.refreshToken,
            });
            commit('setUser', {
                user: state.user,
                access: response.data.access,
                refresh: state.refreshToken,
            });
        } catch (error) {
            console.error('Ошибка обновления токена:', error);
            commit('clearUser');
        }
    },
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    getUser: state => state.user,
  },
});
