<template>
  <div class="register-container">
    <h1>РЕГИСТРАЦИЯ</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-row">
        <label for="username">ИМЯ ПОЛЬЗОВАТЕЛЯ:</label>
        <input type="text" v-model="username" required />
      </div>

      <div class="form-row">
        <label for="email">EMAIL:</label>
        <input type="email" v-model="email" required />
      </div>

      <div class="form-row">
        <label for="password">ПАРОЛЬ:</label>
        <input type="password" v-model="password" required />
      </div>

      <div class="form-row">
        <label for="password2">ПОДТВЕРЖДЕНИЕ ПАРОЛЯ:</label>
        <input type="password" v-model="password2" required />
      </div>

      <button type="submit">ЗАРЕГИСТРИРОВАТЬСЯ</button>
    </form>
    <p v-if="error">{{ error }}</p>
    <button @click="goToLogin">ВОЙТИ</button>
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
        this.error = err.message || 'Произошла о при регистрации';
      }
    },
    goToLogin() {    /* Новый метод переадресации */
      this.$router.push('/login');
    },
  },
};
</script>

<style>
.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* Если хотите занять всю высоту экрана и выровнять по центру: */
  min-height: 100vh;

  /* Или уберите min-height, если хотите минимизировать
     прокрутку при небольшом количестве контента */
}

.register-container h1 {
  user-select: none;
  font-family: "Dela Gothic One", serif;
  color: #38f2ba;
  font-size: 50px;
  margin-bottom: 30px;
}

.register-container p {
    font-family: "Play", serif;
    color: #9faebf;
    user-select: none;
}

.register-container form {
  display: flex;
  flex-direction: column;
  gap: 15px;
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
  /* Если хотите ещё меньше фиксированный размер, поставьте 120px */
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

/* Кнопки */
.register-container button {
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
.register-container button:hover {
  background: #48ffc9;
}

/* Сообщения об ошибке */
.register-container p[v-if="error"] {
  color: red;
  margin-top: 10px;
}

/* Адаптивная верстка: если ширина экрана меньше 600px */
@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
    align-items: flex-start; /* лейбл и инпут выровнены слева */
  }
  .form-row label {
    flex: none; /* убираем фиксированную ширину */
    margin-bottom: 5px;
  }
  .form-row input {
    max-width: 100%;
  }
  .register-container h1 {
    font-size: 35px; /* чуть меньше заголовок на маленьких экранах */
  }
}
</style>
