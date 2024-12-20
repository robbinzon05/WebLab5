<template>
  <div>
    <h1>Rock Paper Scissors</h1>
    <div class="rps-container" v-if="!finished && inProgress">
      <button @click="play('rock')">Rock</button>
      <button @click="play('paper')">Paper</button>
      <button @click="play('scissors')">Scissors</button>
    </div>
    <p v-if="message">{{ message }}</p>
    <button v-if="finished" @click="goBackToLobby">Вернуться в лобби</button>
  </div>
</template>

<script>
import axios from '../plugins/axios';
export default {
  data() {
    return {
      message: '',
      code: '', // Код лобби, передадим через query или получим из Vuex (опционально)
      intervalId: null,
      inProgress: true,
      finished: false,
    };
  },
  async mounted() {
    // Предположим, что код лобби мы можем взять из localStorage или Vuex
    // Допустим, когда стартовали игру, код лобби сохранили в localStorage
    this.code = localStorage.getItem('lobbyCode') || '';
    if (!this.code) {
      // Нет кода лобби, возвращаем в home
      this.$router.push('/home');
      return;
    }
    // Запускаем пульлинг состояния
    this.intervalId = setInterval(() => this.checkState(), 2000);
  },
  beforeUnmount() {
    if (this.intervalId) clearInterval(this.intervalId);
  },
  methods: {
    async play(choice) {
      try {
        await axios.post('/api/lobby/rps/move', {
          code: this.code,
          move: choice,
        });
        this.message = 'Ваш ход сделан, ожидаем другого игрока...';
      } catch (error) {
        console.error('Ошибка при ходе:', error);
        this.message = 'Ошибка при ходе.';
      }
    },
    async checkState() {
      try {
        const response = await axios.get('/api/lobby/rps/state', {
          params: { code: this.code },
        });
        const data = response.data;
        if (data.status === 'no_game') {
          // Игра не активна, вернёмся в лобби
          this.message = 'Игра прервана, возвращаемся в лобби...';
          this.inProgress = false;
          clearInterval(this.intervalId);
          setTimeout(() => {
            this.$router.push('/home');
          }, 2000);
        } else if (data.status === 'opponent_left') {
          // Оппонент ушёл, возвращаемся в лобби
          this.message = 'Оппонент покинул игру, возвращаемся в лобби...';
          this.inProgress = false;
          clearInterval(this.intervalId);
          setTimeout(() => {
            this.$router.push('/home');
          }, 2000);
        } else if (data.status === 'in_progress') {
          this.inProgress = true;
          // moves_done можно использовать, чтобы показать сколько ходов сделано
          // Если moves_done == 2, значит скоро будет результат
        } else if (data.status === 'finished') {
          this.inProgress = false;
          this.finished = true;
          this.message = data.message; // Показываем результат
          clearInterval(this.intervalId);
        }
      } catch (error) {
        console.error('Ошибка при проверке состояния игры:', error);
        this.message = 'Ошибка при проверке состояния.';
      }
    },
    goBackToLobby() {
      this.$router.push('/home');
    },
  },
};
</script>

<style>
.rps-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style>
