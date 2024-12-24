<template>
   <div class="login-container">
      <div>
        <h1>ВХОД</h1>
        <form @submit.prevent="handleLogin">
          <div class="form-row">
            <label for="username">Имя пользователя:</label>
            <input type="text" v-model="username" required />
          </div>
          <div class="form-row">
            <label for="password">Пароль:</label>
            <input type="password" v-model="password" required />
          </div>
          <button type="submit">Войти</button>
        </form>
        <p v-if="error">{{ error }}</p>
        <button @click="goToRegister">Регистрация</button> <!-- Новая кнопка переадресации -->
      </div>
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
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.login-container h1 {
  user-select: none;
  font-family: "Dela Gothic One", serif;
  color: #38f2ba;
  font-size: 50px;
  margin-bottom: 30px;
}

.login-container form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.login-container p {
    font-family: "Play", serif;
    color: #9faebf;
    user-select: none;
}

.form-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.form-row label {
  user-select: none;
  font-family: "Play", serif;
  color: #9faebf;
  flex: 0 0 150px;
}

.form-row input {
  flex: 1;
  max-width: 300px;
  padding: 5px;
  background: #222;
  color: #fff;
  border: 1px solid #444;
  border-radius: 4px;
  font-family: "Play", serif;
}

.login-container button {
  user-select: none;
  font-family: "Play", serif;
  font-size: 17px;
  background: #38f2ba;
  color: #000;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.3s;
}

.login-container button:hover {
  background: #48ffc9;
}

.login-container p[v-if="error"] {
  color: red;
  margin-top: 10px;
}

</style>
