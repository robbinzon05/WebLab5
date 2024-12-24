<template>
  <div class="rps-game-container">
    <h1>Rock Paper Scissors</h1>

    <!-- Предыдущий раунд (если есть) -->
    <p v-if="lastRoundMessage" class="rps-last-round">
      Результат прошлого раунда: {{ lastRoundMessage }}
    </p>

    <!-- Кнопки выбора, если canMove === true -->
    <div class="rps-buttons" v-if="canMove">
      <button @click="play('rock')">Rock</button>
      <button @click="play('paper')">Paper</button>
      <button @click="play('scissors')">Scissors</button>
    </div>

    <!-- Если ход сделан и ждём оппонента -->
    <p v-else-if="!canMove && !opponentLeft" class="rps-waiting">
      Ожидаем ход соперника...
    </p>

    <!-- Основное сообщение (статусы, ошибки) -->
    <p v-if="message" class="rps-message">{{ message }}</p>

    <!-- Кнопка выхода -->
    <button class="exit-button" @click="exitGame">Выйти</button>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Настроенный экземпляр Axios с токеном

export default {
  data() {
    return {
      message: '',
      lastRoundMessage: '',
      code: '',
      intervalId: null,
      canMove: true,
      opponentLeft: false,
    };
  },
  async mounted() {
    // 1) Считываем код лобби из localStorage
    this.code = localStorage.getItem('lobbyCode') || '';
    if (!this.code) {
      this.$router.push('/home');
      return;
    }

    // 2) Запускаем пульлинг состояния каждые 500 мс
    this.intervalId = setInterval(() => this.checkState(), 500);
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
        // После хода временно блокируем кнопки
        this.canMove = false;
        this.message = 'Ход сделан. Ожидаем оппонента...';
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

        if (data.status === 'opponent_left') {
          // Оппонент покинул
          this.opponentLeft = true;
          this.message = 'Оппонент покинул игру. Возвращаемся в лобби...';
          this.canMove = false;
          clearInterval(this.intervalId);
          this.$router.push('/home');
          return;
        }

        if (data.status === 'no_game') {
          // Игра прервана (лобби расформировали)
          this.message = 'Игра прервана. Возвращаемся в лобби...';
          this.canMove = false;
          clearInterval(this.intervalId);
          this.$router.push('/home');
          return;
        }

        // Отображаем результат прошлого раунда
        if (data.lastRoundMessage) {
          this.lastRoundMessage = data.lastRoundMessage;
        }

        // Можно ли ходить?
        this.canMove = data.canMove === true;

        // Выводим message, если сервер вернул
        if (data.message) {
          this.message = data.message;
        }
      } catch (error) {
        console.error('Ошибка при проверке состояния игры:', error);
        this.message = 'Ошибка при проверке состояния.';
      }
    },
    async exitGame() {
      try {
        await axios.post('/api/lobby/stop_rps', { code: this.code });
        this.$router.push('/home');
      } catch (error) {
        console.error('Ошибка при выходе из игры RPS:', error);
        this.$router.push('/home');
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.rps-game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #000;
  color: #fff;
  font-family: "Play", sans-serif;
}

.rps-game-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 30px;
}

.rps-last-round {
  margin-bottom: 20px;
  font-size: 18px;
  color: #9faebf;
}

.rps-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.rps-buttons button {
  font-family: "Play", sans-serif;
  font-size: 16px;
  padding: 8px 12px;
  background: #38f2ba;
  color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s;
}
.rps-buttons button:hover {
  background: #48ffc9;
  box-shadow: 0 0 10px #48ffc9;
}

.rps-waiting {
  font-size: 18px;
  color: #9faebf;
  margin-bottom: 20px;
}

.rps-message {
  margin-top: 10px;
  font-size: 18px;
  color: #ff4444;
}

.exit-button {
  margin-top: 20px;
  font-family: "Play", sans-serif;
  font-size: 16px;
  padding: 8px 12px;
  background: #38f2ba;
  color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s;
}
.exit-button:hover {
  background: #48ffc9;
  box-shadow: 0 0 10px #48ffc9;
}
</style>
