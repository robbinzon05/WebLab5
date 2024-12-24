<template>
  <div class="snake-container">
    <h1>ЗМЕЙКА</h1>

    <!-- Игровое поле -->
    <div id="game-container-snake">
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="{
          snake: snakeCells.includes(index),
          food: foodCell === index
        }"
        class="cell-snake">
      </div>
    </div>

    <!-- Кнопки управления -->
    <div class="button-group">
      <button @click="startGame">Начать игру</button>
      <button @click="back">Назад</button>
    </div>

    <!-- Сообщения -->
    <p v-if="message" class="snake-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios';

export default {
  data() {
    return {
      grid: Array(400).fill(null), // 20x20 grid
      snake: [],
      direction: "left",
      foodCell: null,
      intervalId: null,
      message: '',
    };
  },
  computed: {
    snakeCells() {
      return this.snake;
    }
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
        const response = await axios.post('/api/snake/state/', {
          snake: this.snake,
          direction: this.direction,
          food: this.foodCell,
        });

        this.snake = response.data.snake;
        this.foodCell = response.data.food;
        this.message = response.data.message;

        // Если змея пуста — конец игры
        if (!this.snake || this.snake.length === 0) {
          this.stopGame();
        }
      } catch (error) {
        console.error("Error fetching game state:", error);
      }
    },
    startGame() {
      this.snake = [145, 146, 147];
      this.direction = 'left';
      this.message = '';
      this.stopGame();

      this.foodCell = Math.floor(Math.random() * this.grid.length);
      this.intervalId = setInterval(async () => {
        await this.fetchNextState();
      }, 110);
      window.addEventListener("keydown", this.handleKeyDown);
    },
    handleKeyDown(event) {
      const directionMap = {
        ArrowUp: "up",
        ArrowDown: "down",
        ArrowLeft: "left",
        ArrowRight: "right"
      };
      if (directionMap[event.key]) {
        this.direction = directionMap[event.key];
      }
    },
    stopGame() {
      clearInterval(this.intervalId);
      window.removeEventListener("keydown", this.handleKeyDown);
    }
  },
  beforeUnmount() {
    this.stopGame();
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.snake-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: #fff;
  font-family: "Play", sans-serif;
}

.snake-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 10px;
}

#game-container-snake {
  display: grid;
  grid-template-columns: repeat(20, 20px);
  gap: 1px;
  width: 424px;
  margin: 0 auto 20px;
}

.cell-snake {
  width: 20px;
  height: 20px;
  background-color: #333;
  border: 1px solid #444;
  transition: background 0.2s;
}

.cell-snake.snake {
  background-color: #38f2ba;
}

.cell-snake.food {
  background-color: #ff5454;
}

.button-group {
  display: flex;
  gap: 10px;
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

.snake-message {
  margin-top: 10px;
  font-size: 18px;
  color: #ff4444;
}
</style>
