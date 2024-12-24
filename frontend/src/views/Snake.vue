<template>
  <div id="app">
    <div id="game-container">
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="{
          snake: snakeCells.includes(index),
          food: foodCell === index
        }"
        class="cell">
      </div>
    </div>
    <button @click="startGame">Start Game</button>
    <button @click="back">back</button>
     <p v-if="message">{{ message }}</p>
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
          food: this.foodCell
        });

        this.snake = response.data.snake;
        this.foodCell = response.data.food;
        this.message = response.data.message;

        if (this.snake.isEmpty()){
            this.stopGame();
        }
      } catch (error) {
        console.error("Error fetching game state:", error);
      }
    },
    startGame() {
      this.snake = [145, 146,147];
      this.direction = 'left';
      this.message = '';
      clearInterval(this.intervalId);
      window.removeEventListener("keydown", this.handleKeyDown);

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
#game-container {
  display: grid;
  grid-template-columns: repeat(20, 20px);
  grid-gap: 2px;
  width: 420px;
  margin: 20px auto;
}
.cell {
  width: 20px;
  height: 20px;
  background-color: lightgray;
  border: 1px solid #ccc;
}
.cell.snake {
  background-color: green;
}
.cell.food {
  background-color: red;
}
</style>
