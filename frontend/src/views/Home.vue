<template>
  <div>
    <nav>
      <span v-if="user">Привет, {{ user.username }}!</span>
      <span v-else>Вы не авторизованы</span>
      <button v-if="user" @click="logout">Выйти</button>
    </nav>
    <h1>Главная страница</h1>
    <!-- Здесь будет отображаться список игр -->
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser; // Проверяем наличие пользователя
    },
  },
  methods: {
    ...mapActions(['logout']),
  },
};
</script>
