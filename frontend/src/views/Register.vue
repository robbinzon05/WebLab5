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
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      errorMessage: '',
    };
  },
  methods: {
    async onSubmit() {
      this.errorMessage = ''; // Сброс ошибки перед отправкой
      if (this.password !== this.password2) {
        this.errorMessage = 'Пароли не совпадают.';
        return;
      }

      const url = 'http://localhost:8080/api/auth/register/'; // Замените на ваш URL

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            password2: this.password2,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.password || 'Ошибка при регистрации');
        }

        const result = await response.json();
        console.log('Пользователь успешно зарегистрирован:', result);
        // Перенаправление после успешной регистрации
        this.$router.push('/home'); // Замените на нужный маршрут
      } catch (error) {
        this.errorMessage = error.message || 'Ошибка при регистрации.';
      }
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
  margin-top: 10px;
}
</style>