<template>
  <div>
    <nav>
      <span v-if="user">Привет, {{ user.username }}!</span>
      <span v-else>Вы не авторизованы</span>
      <button v-if="user" @click="logout">Выйти</button>
    </nav>
    <h1>Главная страница</h1>
    <div class="games-container">
      <div class="game-card" @click="goToGame('sudoku')">
        <h2>Sudoku</h2>
        <p>Нажмите, чтобы начать игру</p>
      </div>
      <div class="game-card" @click="goToGame('rps')">
        <h2>Rock Paper Scissors</h2>
        <p>Нажмите, чтобы начать игру</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
  },
  methods: {
    ...mapActions(['logout']),
    goToGame(game) {
      if (game === 'sudoku') {
        this.$router.push('/sudoku');
      } else if (game === 'rps') {
        this.$router.push('/rps');
      }
    },
  },
};
</script>

<style>
.games-container {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.game-card {
  background: #f7f7f7;
  border-radius: 8px;
  padding: 20px;
  width: 200px;
  text-align: center;
  cursor: pointer;
  transition: background 0.3s;
}

.game-card:hover {
  background: #e3e3e3;
}

.game-card h2 {
  margin-bottom: 10px;
}
</style>
