<template>
  <!-- Заголовок игры -->
  <div>
    <h1>Rock Paper Scissors</h1>

    <!-- Выводим результат предыдущего раунда, если есть -->
    <p v-if="lastRoundMessage">Результат прошлого раунда: {{ lastRoundMessage }}</p>

    <!-- Если можно ходить (canMove === true) -->
    <div class="rps-container" v-if="canMove">
      <button @click="play('rock')">Rock</button>
      <button @click="play('paper')">Paper</button>
      <button @click="play('scissors')">Scissors</button>
    </div>

    <!-- Если ход сделан, но ждём оппонента, или иная ситуация -->
    <p v-else-if="!canMove && !opponentLeft">
      Ожидаем ход соперника...
    </p>

    <!-- Сообщения о ходе, ошибках и т.д. -->
    <p v-if="message">{{ message }}</p>

    <!-- Кнопка выхода из игры (просто уходим в лобби) -->
    <button @click="exitGame">Выйти</button>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Настроенный экземпляр Axios с токеном

export default {
  data() {
    return {
      message: '',               // Текстовое сообщение (ошибки, статусы)
      lastRoundMessage: '',      // Текст результата прошлого раунда (например, "Ничья", "Вы выиграли")
      code: '',                  // Код лобби (берём из localStorage)
      intervalId: null,          // Идентификатор setInterval (пульлинг)
      canMove: true,            // Показывает, можем ли мы сейчас сделать ход
      opponentLeft: false,       // Флаг: оппонент вышел
    };
  },
  async mounted() {
    // 1) Считываем код лобби из localStorage
    this.code = localStorage.getItem('lobbyCode') || '';
    if (!this.code) {
      // Если нет кода лобби => уходим в /home
      this.$router.push('/home');
      return;
    }

    // 2) Запускаем пульлинг состояния каждые 200 мс
    this.intervalId = setInterval(() => this.checkState(), 500);
  },
  async exitGame() {
      try {
        // 1) Шлём запрос на сервер, чтобы завершить RPS
        await axios.post('/api/lobby/stop_rps', { code: this.code });

        // 2) Переходим в лобби
        this.$router.push('/home');
      } catch (error) {
        console.error('Ошибка при выходе из игры RPS:', error);
        // Даже если ошибка, уйдём в home
        this.$router.push('/home');
      }
  },
  beforeUnmount() {
    // Остановить пульлинг при размонтировании
    if (this.intervalId) clearInterval(this.intervalId);
  },
  methods: {
    // Делать ход (rock/paper/scissors)
    async play(choice) {
      try {
        await axios.post('/api/lobby/rps/move', {
          code: this.code,
          move: choice,
        });
        // После хода временно блокируем кнопки
        this.canMove = false;
        this.message = 'Коннект есть';
      } catch (error) {
        console.error('Ошибка при ходе:', error);
        this.message = '...';
      }
    },

    // Пульлинг состояния
    async checkState() {
      try {
        const response = await axios.get('/api/lobby/rps/state', {
          params: { code: this.code },
        });
        const data = response.data;

        if (data.status === 'opponent_left') {
          // Оппонент покинул игру => вернёмся в лобби
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

        // Если сервер хранит результат последнего раунда в data.lastRoundMessage
        // выводим его. Например, "Вы выиграли", "Ничья", "Оппонент выиграл"
        if (data.lastRoundMessage) {
          this.lastRoundMessage = data.lastRoundMessage;
        }

        // canMove => можем ходить в новом раунде
        // Если сервер говорит, что ходить можно => canMove=true => показываем кнопки
        // Иначе => "Ожидание оппонента"
        this.canMove = data.canMove === true;

        // Если сервер вернёт data.message, можем отобразить
        if (data.message) {
          this.message = data.message;
        }
      } catch (error) {
        console.error('Ошибка при проверке состояния игры:', error);
        this.message = 'Ошибка при проверке состояния.';
      }
    },

    // Кнопка "Выйти" => возвращаемся в /home
    // Оппонент в пульлинге увидит "opponent_left" (если сервер так настроен)
    async exitGame() {
      try {
        // 1) Шлём запрос на сервер, чтобы завершить RPS
        await axios.post('/api/lobby/stop_rps', { code: this.code });

        // 2) Переходим в лобби
        this.$router.push('/home');
      } catch (error) {
        console.error('Ошибка при выходе из игры RPS:', error);
        // Даже если ошибка, уйдём в home
        this.$router.push('/home');
      }
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
