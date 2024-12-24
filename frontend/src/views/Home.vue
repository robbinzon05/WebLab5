<template>
  <div class="lobby-container">
    <!-- Верхняя панель (навбар) -->
    <nav class="top-bar">
      <div class="user-info">
        <!-- Если пользователь авторизован, показываем приветствие -->
        <span v-if="user">Привет, {{ user.username }}!</span>
        <!-- Иначе (не авторизован) => при клике переходим на логин -->
        <span v-else @click="redirectToLogin">Вы не авторизованы</span>
      </div>

      <!-- Кнопка выхода и "Профиль" только если пользователь авторизован -->
      <div class="btn-group" v-if="user">
        <button @click="goToProfile">Профиль</button>
        <button @click="handleLogout">Выйти</button>
      </div>
    </nav>

    <!-- Родительский контейнер для 2 колонок -->
    <div class="main-content">

      <!-- Левая колонка: информация о лобби -->
      <div class="lobby-info-section">
        <h1>ЛОББИ</h1>

        <!-- Если лобби существует, показываем инфо о лобби -->
        <div class="lobby-info" v-if="lobby">
          <p>КОД ЛОББИ:
            <span v-if="showCode">{{ lobby.code }}</span>
            <span v-else>******</span>
          </p>
          <button @click="toggleShowCode">
            {{ showCode ? 'Скрыть код' : 'Показать код' }}
          </button>
          <p>ИГРОКИ: {{ lobby.players.map(p => p.username).join(', ') }}</p>
          <p>ВЫ: {{ isLeader ? 'ЛИДЕР ЛОББИ' : 'ОБЫЧНЫЙ ИГРОК' }}</p>
        </div>

        <!-- Если лобби не создано (или не пришли данные) => показываем текст -->
        <div class="join-section" v-else>
          <p>Вы не в лобби, создаём новое...</p>
        </div>

        <!-- Поле ввода кода лобби и кнопка "Присоединиться" -->
        <div class="input-but">
          <input v-model="joinCode" placeholder="КОД ЛОББИ ДЛЯ ВХОДА">
          <button @click="joinLobby">ПРИСОЕДИНИТЬСЯ</button>
        </div>

        <!-- Выбранная игра -->
        <p class="chosen-game" v-if="lobby && lobby.selectedGame">
          ВЫБРАНА:
          <span v-if="lobby.selectedGame === 'sudoku'">Sudoku (соло)</span>
          <span v-else-if="lobby.selectedGame === 'rps'">RPS (2 игрока)</span>
          <span v-else-if="lobby.selectedGame === 'japanese_crossword'">Japanese Crossword (соло)</span>
          <span v-else-if="lobby.selectedGame === 'quiz'">Quiz (соло)</span>
          <span v-else-if="lobby.selectedGame === 'snake'">Snake (соло)</span>
          <span v-else-if="lobby.selectedGame === 'tetris'">Tetris (соло)</span>
        </p>

        <!-- Кнопка Старт -->
        <button class="chosen-game-but" v-if="lobby && lobby.selectedGame" @click="startGame">СТАРТ</button>

        <!-- Сообщения об ошибках/информации -->
        <p v-if="message" class="message">{{ message }}</p>
      </div>
      <!-- /lobby-info-section -->

      <!-- Правая колонка: список игр -->
      <div class="games-section">
        <!-- Сетка карточек игр -->
        <div class="games-grid">
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
            <h2>Quiz (Solo)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
          <div class="game-card" @click="selectGame('snake')">
            <h2>Snake (Solo)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
          <div class="game-card" @click="selectGame('tetris')">
            <h2>Tetris (Solo)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
        </div>
      </div>
      <!-- /games-section -->
    </div>
    <!-- /main-content -->
  </div>
  <!-- /lobby-container -->
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from '../plugins/axios';

export default {
  data() {
    return {
      showCode: false,    // Флаг: показывать ли код лобби или скрывать
      joinCode: '',       // Поле для ввода кода лобби
      message: '',        // Текст сообщений/ошибок
      lobby: null,        // Состояние текущего лобби
      pollInterval: null, // Интервал для пульлинга состояния лобби
    };
  },

  computed: {
    ...mapGetters(['getUser']),
    user() {
      return this.getUser;
    },
    isLeader() {
      return this.lobby && this.user && this.lobby.leaderId === this.user.id;
    },
  },

  async created() {
    await this.createLobby();
  },

  async mounted() {
    // Пульлинг раз в 200 мс (или 2000 мс — на ваше усмотрение)
    this.pollInterval = setInterval(() => this.checkLobbyState(), 200);
  },

  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  },

  methods: {
    ...mapActions(['logout']),

    goToProfile() {
      this.$router.push('/profile');
    },

    // Выход из аккаунта => logout + редирект на /login
    handleLogout() {
      this.logout();
      this.$router.push('/login');
    },

    // Если пользователь не авторизован, клик => на /login
    redirectToLogin() {
      this.$router.push('/login');
    },

    toggleShowCode() {
      this.showCode = !this.showCode;
    },

    async createLobby() {
      try {
        const response = await axios.post('http://localhost:8000/api/lobby/create', {});
        this.lobby = response.data;
        this.message = '';
      } catch (error) {
        console.error('Ошибка при создании лобби:', error);
        this.message = 'Не удалось создать лобби.';
      }
    },

    async joinLobby() {
      if (!this.joinCode) {
        this.message = 'Введите код лобби.';
        return;
      }
      try {
        const response = await axios.post('http://localhost:8000/api/lobby/join', {
          code: this.joinCode,
        });
        this.lobby = response.data;
        this.joinCode = '';
        this.message = 'Вы присоединились к лобби.';
      } catch (error) {
        console.error('Ошибка при присоединении к лобби:', error);
        this.message = 'Не удалось присоединиться к лобби: ' + (error.response?.data?.detail || error.message);
      }
    },

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
        this.lobby = response.data;
        this.message = '';
      } catch (error) {
        console.error('Ошибка при выборе игры:', error);
        this.message = 'Не удалось выбрать игру.';
      }
    },

    async startGame() {
      if (!this.lobby || !this.lobby.selectedGame) {
        this.message = 'Сначала выберите игру.';
        return;
      }

      const game = this.lobby.selectedGame;
      const playerCount = this.lobby.players.length;

      // Логика соло-игр и RPS та же, что была в вашем «новом» коде
      if (game === 'sudoku') {
        // Sudoku (соло)
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (confirm('В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/sudoku');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (confirm('Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/sudoku');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          this.$router.push('/sudoku');
        }
      }
      else if (game === 'japanese_crossword') {
        // Japanese Crossword (соло)
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
        // Quiz (соло)
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
        // RPS (2 игрока)
        if (playerCount !== 2) {
          this.message = 'Для RPS нужно ровно 2 игрока в лобби.';
          return;
        }
        if (!this.isLeader) {
          this.message = 'Только лидер лобби может начать игру.';
          return;
        }
        try {
          await axios.post('http://localhost:8000/api/lobby/start', {
            code: this.lobby.code,
            game: this.lobby.selectedGame,
          });
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        } catch (error) {
          console.error('Ошибка при старте игры:', error);
          this.message = 'Не удалось начать игру.';
        }
      }
      // Snake, Tetris — если у вас аналогичная логика (соло):
      else if (game === 'snake') {
        // Соло
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (confirm('В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/snake');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (confirm('Вы лидер. При запуске соло игры лобби будет расформировано. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/snake');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          this.$router.push('/snake');
        }
      }
      else if (game === 'tetris') {
        // Соло
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (confirm('В лобби >1 игрок. Соло игра. Выйти и создать новое пустое лобби?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/tetris');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (confirm('Вы лидер. Соло игра расформирует лобби. Продолжить?')) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/tetris');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          }
        } else {
          this.$router.push('/tetris');
        }
      }
    },

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

    async checkLobbyState() {
      if (!this.lobby || !this.lobby.code) return;
      try {
        const response = await axios.get('http://localhost:8000/api/lobby/state', {
          params: { code: this.lobby.code },
        });
        const data = response.data;

        // Если лидер стартовал RPS (game='rps' + gameInProgress=true),
        // второй игрок тоже заходит на /rps
        if (data.game === 'rps' && data.gameInProgress) {
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        }
        // Аналогично можно добавить другие проверки
      } catch (error) {
        console.error('Ошибка при пульлинге состояния лобби:', error);
      }
    },
  },
};
</script>

<style>
/* Подключение нужных шрифтов (пример из старого кода) */
@import url('https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&family=Dela+Gothic+One&family=Oswald:wght@200..700&family=Play:wght@400;700&display=swap');

/* Общий контейнер */
.lobby-container {
  /* Вы можете здесь указать любой фон, например чёрный, градиент, etc. */
  /* background: #000; */
  /* color: #fff; */
  font-family: "Play", serif;
  padding: 20px;
}

/* Верхняя панель */
.top-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* Группа кнопок в шапке */
.btn-group {
  display: flex;
  gap: 10px;
}

/* Стили кнопок в top-bar */
.top-bar button {
  background: transparent;
  color: #9faebf;
  font-family: "Play", serif;
  font-weight: 700;
  border: none;
  font-size: 25px;
  user-select: none;
  transition: text-shadow 0.2s, color 0.2s;
}
.top-bar button:hover {
  cursor: pointer;
  color: #38f2ba;
  text-shadow: 0 0 15px #38f2ba;
}

/* Стили приветствия */
.user-info span {
  user-select: none;
  font-size: 35px;
  font-weight: 700;
  font-family: "Dela Gothic One", serif;
  color: #38f2ba; /* Неоновый голубой */
}

/* Родительский контейнер для двух колонок */
.main-content {
  display: flex;
  gap: 20px;
  /* Можно добавить justify-content: space-between;
     если хотите, чтобы колонки растягивались */
}

/* Левая колонка (лобби) */
.lobby-info-section {
  flex: 0 0 30%; /* Задаём ~30% ширины для левой колонки */
  background-color: rgba(31, 31, 31, 0.5);
  border-radius: 15px;
  padding: 20px;
}

/* Заголовок "ЛОББИ" */
.lobby-info-section h1 {
  color: white;
  font-style: italic;
  font-size: 40px;
  user-select: none;
  margin-bottom: 20px;
}

/* Текст в блоке лобби */
.lobby-info {
  font-size: 23px;
  margin-bottom: 20px;
}
.lobby-info p {
  color: #38f2ba;
  font-family: "Dela Gothic One", serif;
}

/* Кнопки в блоке лобби */
.lobby-info button {
  background: transparent;
  color: #9faebf;
  font-family: "Play", serif;
  font-weight: bold;
  border: none;
  font-size: 23px;
  user-select: none;
  transition: color 0.2s;
}
.lobby-info button:hover {
  color: #38f2ba;
  text-shadow: 0 0 10px #38f2ba;
}

/* Поле ввода + кнопка "Присоединиться" */
.input-but {
  display: flex;
  gap: 10px;
  flex-direction: column;
  max-width: 200px;
  align-items: center;
  margin: 0 auto;
}
.input-but input {
  padding: 3px;
  border: 1px solid #9faebf;
  border-radius: 8px;
  color: white;
  font-family: "Play", serif;
  background: transparent;
  font-size: 18px;
  transition: box-shadow 0.3s;
}
.input-but input:focus {
  outline: none;
  box-shadow: 0 0 10px #38f2ba;
}

.input-but button {
  background: transparent;
  color: #9faebf;
  font-family: "Play", serif;
  font-weight: bold;
  border: none;
  font-size: 23px;
  user-select: none;
  transition: color 0.2s;
}
.input-but button:hover {
  color: #38f2ba;
  text-shadow: 0 0 10px #38f2ba;
}

.games-section {
  flex: 1; /* Остаток ширины */
  display: flex;
  flex-direction: column;
  background-color: rgba(31, 31, 31, 0.5);
  border-radius: 15px;
  padding: 20px;
  user-select: none;
}

.games-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.game-card {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s, text-shadow 0.3s;
}
.game-card h2 {
  margin-bottom: 10px;
  color: #fff;
  transition: color 0.3s, text-shadow 0.3s;
}
.game-card p {
  color: #9faebf;
  transition: color 0.3s, text-shadow 0.3s;
}

.game-card:hover {
  background: #494949;
  box-shadow: 0 0 10px rgba(56, 242, 186), 0 0 10px rgba(56, 242, 186);
}
.game-card:hover h2 {
  text-shadow: 0 0 20px rgba(56, 242, 186);
}
.game-card:hover p {
  text-shadow: 0 0 10px rgba(177, 200, 227);
}

.message {
  margin-top: 20px;
  color: red;
}

.chosen-game {
    color: #38f2ba;
    font-family: "Dela Gothic One", serif;
    margin-top: 25px;
}

.chosen-game-but {
    background: transparent;
  color: #9faebf;
  font-family: "Play", serif;
  font-weight: bold;
  border: none;
  font-size: 23px;
  user-select: none;
  transition: color 0.2s;
}

.chosen-game-but:hover {
  color: #38f2ba;
  text-shadow: 0 0 10px #38f2ba;
}
</style>
