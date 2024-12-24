<template>
  <!-- Вся разметка обёрнута в общий контейнер лобби -->
  <div class="lobby-container">

    <!-- Шапка (nav) с данными пользователя и кнопками -->
    <nav class="top-bar">
      <div class="user-info">
        <!-- Если пользователь авторизован, показываем приветствие -->
        <span v-if="user">Привет, {{ user.username }}!</span>
        <!-- Иначе (не авторизован) => при клике переходим на логин -->
        <span v-else @click="redirectToLogin">Вы не авторизованы</span>
      </div>
      <!-- Кнопка выхода только для авторизованного пользователя -->
      <button v-if="user" @click="handleLogout">Выйти</button>
      <!-- Кнопка "Профиль" тоже только для авторизованного -->
      <button v-if="user" @click="goToProfile">Профиль</button>
    </nav>

    <h1>Лобби</h1>

    <!-- Если лобби существует, показываем инфо о лобби -->
    <div class="lobby-info" v-if="lobby">
      <p>Код лобби:
        <!-- Можно показать/скрыть код лобби -->
        <span v-if="showCode">{{ lobby.code }}</span>
        <span v-else>******</span>
      </p>
      <button @click="toggleShowCode">
        {{ showCode ? 'Скрыть код' : 'Показать код' }}
      </button>
      <!-- Список игроков в лобби, каждого берем username -->
      <p>Игроки: {{ lobby.players.map(p => p.username).join(', ') }}</p>
      <!-- Указываем, является ли текущий пользователь лидером -->
      <p>Вы: {{ isLeader ? 'Лидер лобби' : 'Обычный игрок' }}</p>
    </div>
    <!-- Если лобби не создано (или не пришли данные) => показываем текст о создании -->
    <div class="join-section" v-else>
      <p>Вы не в лобби, создаём новое...</p>
    </div>

    <!-- Поле ввода кода лобби, чтобы присоединиться -->
    <input v-model="joinCode" placeholder="Код лобби для входа">
    <button @click="joinLobby">Присоединиться к лобби по коду</button>

    <!-- Блок выбора игр -->
    <div class="games-grid">
      <!-- Каждая игра — это своя карточка, при клике вызов selectGame(...).
           В RPS нужно ровно 2 игрока, в остальных случаях — соло. -->
      <div class="game-card" @click="selectGame('sudoku')">
        <h2>Sudoku (Solo)</h2>
        <p>Нажмите, чтобы выбрать игру</p>
      </div>
      <div class="game-card" @click="selectGame('rps')">
        <h2>Rock Paper Scissors (2 игрока)</h2>
        <p>Нажмите, чтобы выбрать игру</p>
      </div>
      <div class="game-card" @click="selectGame('japanese_crossword')">
        <h2>Japanese Crossword (Solo)</h2>
        <p>Нажмите, чтобы выбрать игру</p>
      </div>
      <div class="game-card" @click="selectGame('quiz')">
        <h2>Quiz(Solo)</h2>
        <p>Нажмите, чтобы выбрать игру</p>
      </div>
    </div>

    <!-- Отображаем выбранную игру, если она есть -->
    <p v-if="lobby && lobby.selectedGame">
      Выбрана игра:
      <span v-if="lobby.selectedGame === 'sudoku'">Sudoku (соло)</span>
      <span v-else-if="lobby.selectedGame === 'rps'">Rock Paper Scissors (2 игрока)</span>
      <span v-else-if="lobby.selectedGame === 'japanese_crossword'">Japanese Crossword (соло)</span>
      <span v-else-if="lobby.selectedGame === 'quiz'">Quiz (соло)</span>
    </p>

    <!-- Кнопка "Старт" отображается, если игра выбрана -->
    <button v-if="lobby && lobby.selectedGame" @click="startGame">Старт</button>

    <!-- Вывод ошибок или сообщений -->
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from '../plugins/axios';

export default {
  data() {
    return {
      showCode: false,    // Флаг, показывать ли код лобби или скрывать
      joinCode: '',       // Поле для ввода кода лобби
      message: '',        // Текст сообщений/ошибок
      lobby: null,        // Состояние текущего лобби (код, список игроков, т.д.)
      pollInterval: null, // Интервал для пульлинга состояния лобби
    };
  },
  computed: {
    ...mapGetters(['getUser']), // Берём user из Vuex

    // Возвращаем пользователя
    user() {
      return this.getUser;
    },

    // Проверяем, является ли пользователь лидером
    isLeader() {
      return this.lobby && this.user && this.lobby.leaderId === this.user.id;
    },
  },

  // При создании компонента (created) — создаём новое лобби сразу
  async created() {
    await this.createLobby();
  },

  // Когда компонент смонтирован (mounted) — запускаем пульлинг
  async mounted() {
    // Пульлинг состояния лобби каждые 200 мс
    // Цель: если лидер стартовал RPS, второй игрок увидит это и войдёт в игру
    this.pollInterval = setInterval(() => this.checkLobbyState(), 200);
  },

  // При демонтировании компонента (beforeUnmount) — останавливаем пульлинг
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  },

  methods: {
    // Берём экшены из Vuex: logout
    ...mapActions(['logout']),

    // Переход к профилю
    goToProfile() {
      this.$router.push('/profile');
    },

    // Показать/скрыть код лобби
    toggleShowCode() {
      this.showCode = !this.showCode;
    },

    // Выход из аккаунта => logout + перейти на /login
    handleLogout() {
      // Вызываем экшен logout из Vuex
      this.logout();
      // После выхода автоматически переходим на страницу логина
      this.$router.push('/login');
    },

    // Если пользователь оказался не авторизован, кликая по "Вы не авторизованы"
    redirectToLogin() {
      // Переходим на страницу логина
      this.$router.push('/login');
    },

    // Создание лобби на сервере через эндпоинт /api/lobby/create
    async createLobby() {
      try {
        const response = await axios.post('http://localhost:8000/api/lobby/create', {});
        this.lobby = response.data; // Сохраняем данные лобби (код, игроки, лидер и т.д.)
        this.message = '';
      } catch (error) {
        console.error('Ошибка при создании лобби:', error);
        this.message = 'Не удалось создать лобби.';
      }
    },

    // Вход в лобби по коду
    async joinLobby() {
      if (!this.joinCode) {
        this.message = 'Введите код лобби.';
        return;
      }
      try {
        const response = await axios.post('http://localhost:8000/api/lobby/join', {
          code: this.joinCode,
        });
        this.lobby = response.data; // Обновляем состояние лобби
        this.joinCode = '';
        this.message = 'Вы присоединились к лобби.';
      } catch (error) {
        console.error('Ошибка при присоединении к лобби:', error);
        this.message = 'Не удалось присоединиться к лобби: ' + (error.response?.data?.detail || error.message);
      }
    },

    // Выбираем одну из игр (sudoku, rps, japanese_crossword, quiz)
    async selectGame(game) {
      if (!this.lobby) {
        this.message = 'Вы не в лобби.';
        return;
      }
      try {
        const response = await axios.post('http://localhost:8000/api/lobby/selectGame', {
          code: this.lobby.code,
          game,
        });
        this.lobby = response.data; // Сервер возвращает обновлённое состояние лобби
        this.message = '';
      } catch (error) {
        console.error('Ошибка при выборе игры:', error);
        this.message = 'Не удалось выбрать игру.';
      }
    },

    // Нажатие на "Старт" => проверяем кол-во игроков и тип игры
    async startGame() {
      if (!this.lobby || !this.lobby.selectedGame) {
        this.message = 'Сначала выберите игру.';
        return;
      }

      const game = this.lobby.selectedGame;
      const playerCount = this.lobby.players.length;

      if (game === 'sudoku') {
        // Sudoku — соло
        if (playerCount > 1) {
          if (!this.isLeader) {
            // Если не лидер => предупреждаем, что выйдет в новое пустое лобби
            if (confirm('В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/sudoku');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            // Если лидер => лобби расформируется
            if (confirm('Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/sudoku');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          // Если 1 игрок => просто переходим на Sudoku
          this.$router.push('/sudoku');
        }
      }
      else if (game === 'japanese_crossword') {
        // Японский кроссворд — соло, аналогична логика
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (confirm('В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/japaneseCrossword');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (confirm('Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/japaneseCrossword');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          this.$router.push('/japaneseCrossword');
        }
      }
      else if (game === 'quiz') {
        // Quiz — соло
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (confirm('В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/quiz');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (confirm('Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/quiz');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          this.$router.push('/quiz');
        }
      }
      else if (game === 'rps') {
        // RPS — нужно ровно 2 игрока
        if (playerCount !== 2) {
          this.message = 'Для RPS нужно ровно 2 игрока в лобби.';
          return;
        }
        if (!this.isLeader) {
          this.message = 'Только лидер лобби может начать игру.';
          return;
        }
        try {
          // Сообщаем серверу, что стартуем RPS
          await axios.post('http://localhost:8000/api/lobby/start', {
            code: this.lobby.code,
            game: this.lobby.selectedGame,
          });
          // Сохраняем код лобби для RPS.vue
          localStorage.setItem('lobbyCode', this.lobby.code);
          // Переходим на экран RPS
          this.$router.push('/rps');
        } catch (error) {
          console.error('Ошибка при старте игры:', error);
          this.message = 'Не удалось начать игру.';
        }
      }
    },

    // Расформирование лобби (доступно только лидеру)
    async dissolveLobby() {
      if (!this.lobby || !this.isLeader) {
        return;
      }
      try {
        await axios.post('http://localhost:8000/api/lobby/dissolve', {
          code: this.lobby.code,
        });
        this.lobby = null;
        this.message = 'Лобби расформировано.';
      } catch (error) {
        console.error('Ошибка при расформировании лобби:', error);
        this.message = 'Не удалось расформировать лобби.';
      }
    },

    // Пульлинг состояния лобби (каждые 200 мс из mounted())
    // Нужно, чтобы второй игрок автоматически переходил в игру,
    // когда лидер нажимает "Старт" (особенно в RPS).
    async checkLobbyState() {
      if (!this.lobby || !this.lobby.code) return;
      try {
        const response = await axios.get('http://localhost:8000/api/lobby/state', {
          params: { code: this.lobby.code },
        });
        const data = response.data;

        // Если с сервера вернётся game='rps' + gameInProgress =>
        // даже второй игрок пойдёт на '/rps'
        if (data.game === 'rps' && data.gameInProgress) {
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        }
      } catch (error) {
        console.error('Ошибка при пульлинге состояния лобби:', error);
        // Если лобби расформировано или ошибка 403/404, можно заново создать или вывести сообщение.
      }
    },
  },
};
</script>

<style>
.lobby-container {
  padding: 20px;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.games-grid {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.game-card {
  background: #f7f7f7;
  border-radius: 8px;
  padding: 20px;
  width: 300px;
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

.message {
  margin-top: 20px;
  color: red;
}
</style>
