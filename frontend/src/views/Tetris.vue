<template>
  <div class="tetris-container">
    <h1>Тетрис</h1>

    <div id="game-container-tetris">
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="[
          'cell-tetris',
          {
            active: activeCells.includes(index),
            block: blockCells.includes(index),
          },
          shape
        ]"
      ></div>
    </div>

    <div class="button-group">
      <button @click="startGame">Start Game</button>
      <button @click="back">Back</button>
    </div>

    <p>Ваши очки: {{ scope }}</p>
    <p v-if="message" class="tetris-message">{{ message }}</p>

    <!-- Музыка -->
    <audio ref="audio" hidden controls>
      <source :src="audioFile" type="audio/mp3" />
    </audio>
  </div>
</template>

<script>
import axios from '../plugins/axios';
import audioFile from '../assets/tetrismusic.mp3';

export default {
  data() {
    return {
      grid: Array(150).fill(null), // 10x15 (или 10x20 ?) - проверяйте
      activeCells: [],
      blockCells: [],
      shape: null,
      rotation: 0,
      scope: 0,
      intervalId: null,
      message: '',
      audioFile: audioFile,
      musicInterval: null,
    };
  },
  methods: {
    async back() {
      try {
        this.$router.push('/home');
      } catch (error) {
        console.error('Ошибка при возврате', error);
        this.message = 'Ошибка при возврате.';
      }
    },
    async fetchNextState() {
      try {
        const response = await axios.post('/api/tetris/state/', {
          cells: this.activeCells,
          blockCells: this.blockCells,
          shape: this.shape,
          rotation: this.rotation,
        });

        this.activeCells = response.data.cells;
        this.blockCells = response.data.blockCells;
        this.shape = response.data.shape;
        this.rotation = response.data.rotation;
        this.message = response.data.message;
        const incorrect = response.data.incorrect;
        this.scope = response.data.scope;

        // Если game over
        if (incorrect) {
          this.stopGame();
        }
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    },
    startGame() {
      this.activeCells = [];
      this.blockCells = [];
      this.rotation = 0;
      this.message = '';
      this.scope = 0;

      this.stopGame();

      // Стартовое состояние (запрос к серверу)
      axios.get('/api/tetris/start/');

      // Включаем музыку
      this.$refs.audio.play();
      // По окончании трека повторяем (каждые 102сек, подгоняйте под длительность файла)
      this.musicInterval = setInterval(() => {
        this.$refs.audio.pause();
        this.$refs.audio.currentTime = 0;
        this.$refs.audio.play();
      }, 102000);

      // Пульс игры
      this.intervalId = setInterval(async () => {
        await this.fetchNextState();
      }, 300);

      // Управление стрелками
      window.addEventListener('keydown', this.handleKeyDown);
    },
    handleKeyDown(event) {
      const actionMap = {
        ArrowLeft: 'left',
        ArrowRight: 'right',
        ArrowDown: 'down',
        ArrowUp: 'rotate',
      };
      if (actionMap[event.key]) {
        this.updateDirection(actionMap[event.key]);
      }
    },
    async updateDirection(action) {
      try {
        const response = await axios.post('/api/tetris/action/', {
          action,
          cells: this.activeCells,
          blockCells: this.blockCells,
          shape: this.shape,
          rotation: this.rotation,
        });

        this.activeCells = response.data.cells;
        this.shape = response.data.shape;
        this.rotation = response.data.rotation;
        this.message = response.data.message;
        const incorrect = response.data.incorrect;

        if (incorrect) {
          this.stopGame();
        }
      } catch (error) {
        console.error('Error updating action:', error);
      }
    },
    stopGame() {
      // Останавливаем музыку
      this.$refs.audio.pause();
      this.$refs.audio.currentTime = 0;

      if (this.musicInterval) {
        clearInterval(this.musicInterval);
        this.$refs.audio.pause();
        this.$refs.audio.currentTime = 0;
      }
      clearInterval(this.intervalId);
      window.removeEventListener('keydown', this.handleKeyDown);
    },
  },
  beforeUnmount() {
    this.stopGame();
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.tetris-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #fff;
  font-family: "Play", sans-serif;
}

.tetris-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 30px;
}

#game-container-tetris {
  display: grid;
  grid-template-columns: repeat(10, 30px);
  gap: 2px;
  width: auto;
  margin: 20px auto;
}

.cell-tetris {
  width: 30px;
  height: 30px;
  background-color: #222;
  border: 1px solid #444;
  transition: background 0.15s;
}

.cell-tetris.active {
  background-color: #38f2ba;
}

.cell-tetris.block {
  background-color: #555;
}

.cell-tetris.I.active {
  background-color: #00e5ff;
}
.cell-tetris.T.active {
  background-color: #d084ff;
}
.cell-tetris.S.active,
.cell-tetris.Z.active {
  background-color: #ff5e5e;
}
.cell-tetris.J.active,
.cell-tetris.L.active {
  background-color: #f0f65e;
}
.cell-tetris.O.active {
  background-color: #48ffc9;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 0px;
}

.button-group button {
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
.button-group button:hover {
  background: #48ffc9;
  box-shadow: 0 0 10px #48ffc9;
}

.tetris-container p {
  margin-top: 0px;
}

.tetris-message {
  font-size: 18px;
  color: #ff4444;
}
</style>
