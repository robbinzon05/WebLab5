<template>
  <div>
    <h1>Регистрация</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label for="password2">Подтверждение пароля:</label>
        <input type="password" v-model="password2" required />
      </div>
      <button type="submit">Зарегистрироваться</button>
    </form>
    <p v-if="error">{{ error }}</p>
    <button @click="goToLogin">Войти</button> <!-- Новая кнопка переадресации -->
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      error: '',
    };
  },
  methods: {
    ...mapActions(['register']),
    async handleRegister() {
      try {
        await this.register({
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
        });
        this.$router.push('/home');
      } catch (err) {
        this.error = err.message || 'Произошла ошибка при регистрации';
      }
    },
    goToLogin() {    /* Новый метод переадресации */
      this.$router.push('/login');
    },
  },
};
</script>

<style>
/* Добавьте стили по необходимости */
</style>
