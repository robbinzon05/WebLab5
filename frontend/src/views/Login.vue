<template>
  <div>
    <h1>Вход</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <p v-if="error">{{ error }}</p>
    <button @click="goToRegister">Регистрация</button> <!-- Новая кнопка переадресации -->
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
    };
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      try {
        await this.login({ username: this.username, password: this.password });
        this.$router.push('/home');
      } catch (err) {
        this.error = err.message || 'Произошла ошибка при входе';
      }
    },
    goToRegister() {    /* Новый метод переадресации */
      this.$router.push('/register');
    },
  },
};
</script>

<style>
/* Добавьте стили по необходимости */
</style>
