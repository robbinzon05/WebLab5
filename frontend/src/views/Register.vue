<template>
  <div>
    <h1>Регистрация</h1>
    <form @submit.prevent="onSubmit">
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
        <label for="password2">Повторите пароль:</label>
        <input type="password" v-model="password2" required />
      </div>
      <button type="submit">Зарегистрироваться</button>
    </form>
    <p>Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '', // Заменил nickname на username
      email: '',
      password: '',
      password2: '',
    };
  },
  methods: {
    ...mapActions(['register']),
    async onSubmit() {
      if (this.password !== this.password2) {
        alert('Пароли не совпадают.');
        return;
      }
      try {
        await this.register({
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.$router.push('/home');
      } catch (error) {
        console.error(error);
        alert('Ошибка при регистрации.');
      }
    },
  },
};
</script>
