<template>
  <!-- Заголовок игры -->
  <div>
    <h1>Rock Paper Scissors</h1>

    <!-- Если игра продолжается (inProgress) и не закончена (finished) -->
    <div class="rps-container" v-if="!finished && inProgress">
      <!-- Три кнопки для выбора: rock, paper, scissors -->
      <button @click="play('rock')">Rock</button>
      <button @click="play('paper')">Paper</button>
      <button @click="play('scissors')">Scissors</button>
    </div>

    <!-- Сообщения о ходе, результате, ошибках и т.д. -->
    <p v-if="message">{{ message }}</p>

    <!-- Кнопка возвращения в лобби (видна только когда finished=true) -->
    <button v-if="finished" @click="goBackToLobby">Вернуться в лобби</button>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
  data() {
    return {
      message: '',     // Поле для вывода сообщений (ожидание, результат и т.д.)
      code: '',        // Код лобби (читаем из localStorage при входе)
      intervalId: null,// Идентификатор setInterval для пульлинга состояния
      inProgress: true,// Флаг: игра идёт (пока не закончена)
      finished: false, // Флаг: игра закончена (показать результат)
    };
  },
  async mounted() {
    // При монтировании компонента:
    // 1) Считываем из localStorage код лобби, который туда записали в Home.vue при старте
    this.code = localStorage.getItem('lobbyCode') || '';
    if (!this.code) {
      // Если нет кода, значит мы не знаем, в каком лобби, => идём на /home
      this.$router.push('/home');
      return;
    }

    // 2) Запускаем пульлинг (checkState) каждые 2 секунды, чтобы отслеживать статус игры
    this.intervalId = setInterval(() => this.checkState(), 2000);
  },
  beforeUnmount() {
    // При размонтировании компонента останавливаем пульлинг
    if (this.intervalId) clearInterval(this.intervalId);
  },
  methods: {
    // Обработка выбора (rock, paper или scissors)
    async play(choice) {
      try {
        // Отправляем ход на сервер: '/api/lobby/rps/move'
        // Параметры: code (код лобби), move (выбор)
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

    // Пульлинг: спрашиваем состояние игры у сервера
    async checkState() {
      try {
        const response = await axios.get('/api/lobby/rps/state', {
          // Передаём code как query-параметр
          params: { code: this.code },
        });
        const data = response.data;

        // Интерпретируем статус
        if (data.status === 'no_game') {
          // Игра не активна => возвращаемся в лобби
          this.message = 'Игра прервана, возвращаемся в лобби...';
          this.inProgress = false;
          clearInterval(this.intervalId);
          setTimeout(() => {
            this.$router.push('/home');
          }, 2000);
        } else if (data.status === 'opponent_left') {
          // Оппонент покинул игру => выкидываем пользователя обратно в лобби
          this.message = 'Оппонент покинул игру, возвращаемся в лобби...';
          this.inProgress = false;
          clearInterval(this.intervalId);
          setTimeout(() => {
            this.$router.push('/home');
          }, 2000);
        } else if (data.status === 'in_progress') {
          // Игра идёт, ждём ходов
          this.inProgress = true;
          // moves_done (data.moves_done) можно вывести пользователю
        } else if (data.status === 'finished') {
          // Игра завершилась => показываем результат
          this.inProgress = false;
          this.finished = true;
          this.message = data.message; // data.message содержит например "Ничья!" или "Победитель: ... "
          clearInterval(this.intervalId);
        }
      } catch (error) {
        console.error('Ошибка при проверке состояния игры:', error);
        this.message = 'Ошибка при проверке состояния.';
      }
    },

    // Кнопка возвращения в лобби после окончания игры
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
