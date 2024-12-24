<template>
  <div class="lobby-container">
    <nav class="top-bar">
      <div class="user-info">
        <span v-if="user">ПРИВЕТ, {{ user.username }}!</span>
        <span v-else>ВЫ НЕ АВТОРИЗОВАНЫ</span>
      </div>
      <div class="btn-group" v-if="user">
        <button @click="goToProfile">ПРОФИЛЬ</button>
        <button @click="logout">ВЫЙТИ</button>
      </div>
    </nav>

    <!-- Родительский блок, который разделит содержимое на две колонки -->
    <div class="main-content">

      <!-- Левая колонка: информация о лобби -->
      <div class="lobby-info-section">
        <h1>ЛОББИ</h1>
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

        <div class="join-section" v-else>
          <p>Вы не в лобби, создаём новое...</p>
        </div>
        <div class="input-but">
            <input v-model="joinCode" placeholder="КОД ЛОББИ ДЛЯ ВХОДА">
            <button @click="joinLobby">ПРИСОЕДИНИТЬСЯ</button>
        </div>
        <p v-if="lobby && lobby.selectedGame">
          ВЫБРАНА: {{ lobby.selectedGame === 'sudoku' ? 'Sudoku (соло)' : 'RPS (2 игрока)' }}
        </p>

        <button v-if="lobby && lobby.selectedGame" @click="startGame">Старт</button>
        <p v-if="message" class="message">{{ message }}</p>
      </div>

      <!-- Правая колонка: игры -->
      <div class="games-section">
        <div class="games-grid">
          <div class="game-card" @click="selectGame('sudoku')">
            <h2>SUDOKU (SOLO)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
          <div class="game-card" @click="selectGame('rps')">
            <h2>ROCK PAPER SCISSORS (2 ИГРОКА)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
          <div class="game-card" @click="selectGame('japanese_crossword')">
            <h2>JAPANESE CROSSWORD (SOLO)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
          <div class="game-card" @click="selectGame('quiz')">
            <h2>QUIZ (SOLO)</h2>
            <p>Нажмите, чтобы выбрать игру</p>
          </div>
        </div>
      </div>
    </div> <!-- /main-content -->
  </div> <!-- /lobby-container -->
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from '../plugins/axios';

export default {
  data() {
    return {
      showCode: false,
      joinCode: '',
      message: '',
      lobby: null,
      pollInterval: null,
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
    this.pollInterval = setInterval(() => this.checkLobbyState(), 2000);
  },
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  },
  methods: {
    ...mapActions(['logout']),
    goToProfile() {
      this.$router.push('/profile');
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
        this.message =
          'Не удалось присоединиться к лобби: ' +
          (error.response?.data?.detail || error.message);
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
      if (game === 'sudoku') {
        // Соло игра
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (
              confirm(
                'В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?'
              )
            ) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/sudoku');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (
              confirm(
                'Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?'
              )
            ) {
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
      } else if (game === 'japanese_crossword') {
        // Соло игра
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (
              confirm(
                'В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?'
              )
            ) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/japaneseCrossword');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (
              confirm(
                'Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?'
              )
            ) {
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
      } else if (game === 'quiz') {
        // Соло игра
        if (playerCount > 1) {
          if (!this.isLeader) {
            if (
              confirm(
                'В лобби >1 игрок. Соло игра. Вы выйдете из этого лобби и создадите новое пустое. Продолжить?'
              )
            ) {
              await this.dissolveLobby();
              await this.createLobby();
              this.$router.push('/quiz');
            } else {
              this.message = 'Вы отменили старт игры.';
            }
          } else {
            if (
              confirm(
                'Вы лидер и в лобби >1 игрока. При запуске соло игры лобби будет расформировано. Продолжить?'
              )
            ) {
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
      } else if (game === 'rps') {
        // RPS - 2 игрока
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
          });
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        } catch (error) {
          console.error('Ошибка при старте игры:', error);
          this.message = 'Не удалось начать игру.';
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
        if (data.game === 'rps' && data.gameInProgress) {
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        }
      } catch (error) {
        console.error('Ошибка при пульлинге состояния лобби:', error);
      }
    },
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&family=Dela+Gothic+One&family=Oswald:wght@200..700&family=Play:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&family=Play:wght@400;700&display=swap');
.lobby-container {
  font-family: "Play", serif;
  padding: 20px;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.btn-group {
  display: flex;
  gap: 10px;
}

.top-bar button {
    background: transparent;
    color: #9faebf;
    font-family: "Play", serif;
    font-weight: 700;
    border: none;
    font-size: 25px;
    user-select: none;
    transition: text-shadow 0.2s, color 0.2s
}

.top-bar button:hover {
    cursor: pointer;
    color: #38f2ba;
    text-shadow: 0 0 15px #38f2ba;
}

.user-info span {
    user-select: none;
    font-size: 35px;
    font-weight: 700;
    font-family: "Dela Gothic One", serif;
    color: #38f2ba;
}

.main-content {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.lobby-info-section {
  flex: 0 0 30%;
  background-color: rgba(31, 31, 31, 0.5);
  border-radius: 15px;
}

.lobby-info-section h1 {
    color: white;
    font-style: italic;
    font-size: 40px;
    user-select: none;
}

.lobby-info p {
    color: #38f2ba;
    font-family: "Dela Gothic One", serif;
}

.lobby-info {
    font-size: 23px;
}

.lobby-info button,
 .input-but button{
    background: transparent;
    color: #9faebf;
    font-family: "Play", serif;
    font-weight: bold;
    border: none;
    font-size: 23px;
    user-select: none;
    transition: color 0.2s;
}

.lobby-info button:hover,
 .input-but button:hover{
    color: #38f2ba;
    text-shadow: 0 0 10px #38f2ba;
}

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
    outline:none;
    box-shadow: 0 0 10px #38f2ba;
}

.games-section {
  flex: 0 0 50%;
  display: flex;
  flex-direction: column;
  background-color: rgba(31, 31, 31, 0.5);
  border-radius: 15px;
  user-select: none;
}

.game-card h2 {
  color: #fff;

}

.games-grid {
  padding: 15px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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

.game-card p {
    color: #9faebf;
}

.game-card:hover {
  background: #494949;
  box-shadow: 0 0 10px rgba(56, 242, 186), 0 0 10px rgba(56, 242, 186);
}

.game-card h2,
.game-card p {
    transition: color 0.3s, text-shadow 0.3s;
}

.game-card:hover h2 {
    text-shadow: 0 0 20px rgba(56, 242, 186);
}

.game-card:hover p {
    text-shadow: 0 0 10px rgba(177, 200, 227);
}

.game-card h2 {
  margin-bottom: 10px;
}

.message {
  margin-top: 20px;
  color: red;
}
</style>
