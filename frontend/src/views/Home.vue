<template>
  <div class="lobby-container">
    <nav class="top-bar">
      <div class="user-info">
        <span v-if="user">Привет, {{ user.username }}!</span>
        <span v-else>Вы не авторизованы</span>
      </div>
      <button v-if="user" @click="logout">Выйти</button>
      <button v-if="user" @click="goToProfile">Профиль</button>
    </nav>

    <h1>Лобби</h1>
    <div class="lobby-info" v-if="lobby">
      <p>Код лобби: <span v-if="showCode">{{ lobby.code }}</span><span v-else>******</span></p>
      <button @click="toggleShowCode">{{ showCode ? 'Скрыть код' : 'Показать код' }}</button>
      <p>Игроки: {{ lobby.players.map(p => p.username).join(', ') }}</p>
      <p>Вы: {{ isLeader ? 'Лидер лобби' : 'Обычный игрок' }}</p>
    </div>
    <div class="join-section" v-else>
      <p>Вы не в лобби, создаём новое...</p>
    </div>

    <input v-model="joinCode" placeholder="Код лобби для входа">
    <button @click="joinLobby">Присоединиться к лобби по коду</button>

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
        <h2>Quiz(Solo)</h2>
        <p>Нажмите, чтобы выбрать игру</p>
      </div>
    </div>

    <p v-if="lobby && lobby.selectedGame">
      Выбрана игра: {{ lobby.selectedGame === 'sudoku' ? 'Sudoku (соло)' : 'RPS (2 игрока)' }}
    </p>

    <button v-if="lobby && lobby.selectedGame" @click="startGame">Старт</button>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
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
    // Запускаем пульлинг состояния лобби
    // Пульлинг нужен, чтобы если лидер стартует игру RPS, второй игрок попал в rps
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

      if (game === 'sudoku') {
        // Соло игра

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
      }else if (game === 'japanese_crossword') {
        // Соло игра

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
      } else if (game === 'quiz') {
        // Соло игра

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
            game:this.lobby.selectedGame,
          });
          // Сохраняем код лобби, чтобы RPS.vue знал с каким лобби работать
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

        // Если мы не в лобби, вернёмся в home
        // Но мы уже на home, значит обновим lobby
        // Здесь можно обновить lobby, если хотите
        // Но главное следить за game/gameInProgress
        if (data.game === 'rps' && data.gameInProgress) {
          // Если не лидер, или даже лидер, если хотите чтобы оба шли в RPS,
          // Если вы хотите только второго игрока, то можно проверить !this.isLeader
          localStorage.setItem('lobbyCode', this.lobby.code);
          this.$router.push('/rps');
        }
      } catch (error) {
        console.error('Ошибка при пульлинге состояния лобби:', error);
        // Если лобби расформировано или ошибка 403/404, можно попытаться пересоздать или показать сообщение.
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
