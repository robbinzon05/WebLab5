<template>
  <div>
    <h1>Вход</h1>
    <form @submit.prevent="onSubmit">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <p>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '', // Используем username вместо nickname
      password: '',
    };
  },
  methods: {
    ...mapActions(['login']),
    async onSubmit() {
      try {
        await this.login({ username: this.username, password: this.password });
        this.$router.push('/home'); // Перенаправляем на главную страницу после успешного входа
      } catch (error) {
        console.error(error);
        alert('Ошибка при входе. Проверьте правильность введенных данных.');
      }
    },
  },
};
</script>
