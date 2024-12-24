<template>
  <div class="jcross-container" id="app-jcross">
    <h1>JAPANESE CROSSWORD</h1>

    <div class="nonogram">
      <!-- Подсказки для колонок -->
      <div class="clues clues-cols">
        <div v-for="(col, colIndex) in colClues" :key="colIndex" class="col-clue">
          <div v-for="(num, idx) in col" :key="idx" class="num">
            {{ num }}
          </div>
        </div>
      </div>

      <div class="grid">
        <!-- Подсказки для строк -->
        <div class="clues clues-rows">
          <div v-for="(row, rowIndex) in rowClues" :key="rowIndex" class="row-clue">
            <div v-for="(num, idx) in row" :key="idx" class="num">
              {{ num }}
            </div>
          </div>
        </div>

        <!-- Сами ячейки кроссворда -->
        <div class="cells">
          <div
            v-for="(row, rowIndex) in grid"
            :key="rowIndex"
            class="row"
          >
            <div
              v-for="(cell, colIndex) in row"
              :key="colIndex"
              class="cell"
              :class="{ filled: cell === 1, cross: cell === 2 }"
              @click="toggleCell(rowIndex, colIndex)"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Кнопки -->
    <div class="button-group">
      <button @click="checkSolution">Проверить решение</button>
      <button @click="load">Restart</button>
      <button @click="back">Back</button>
    </div>

    <!-- Сообщение -->
    <p v-if="message" class="jcross-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
  data() {
    return {
      grid: [],
      rowClues: [],
      colClues: [],
      size: 0,
      message: '',
    };
  },
  async created() {
    await this.load();
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
    async load() {
      try {
        const response = await axios.get('/api/japaneseCrossword/start/');
        this.rowClues = response.data.rowClues;
        this.colClues = response.data.colClues;
        this.size = response.data.size;
        // Изначально все ячейки false (0) => пусто
        this.grid = Array.from({ length: this.size }, () => Array(this.size).fill(0));
        this.message = '';
      } catch (error) {
        console.error('Ошибка при получении пазла:', error);
        this.message = 'Не удалось загрузить пазл.';
      }
    },
    toggleCell(row, col) {
      // 0 => 1 => 2 => 0 => ...
      // 0 (пусто), 1 (закрашено), 2 (крест)
      this.grid[row][col] = (this.grid[row][col] + 1) % 3;
    },
    async checkSolution() {
      try {
        const response = await axios.post('/api/japaneseCrossword/check/', {
          solution: this.grid,
          rowClues: this.rowClues,
          colClues: this.colClues,
          size: this.size,
        });

        if (response.data.correct) {
          this.message = 'Решение верное! Поздравляем!';
        } else {
          this.message = 'Решение неверно, попробуйте еще раз.';
        }
      } catch (error) {
        console.error('Ошибка при проверке решения:', error);
        this.message = 'Произошла ошибка при проверке решения.';
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.jcross-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #000;
  color: #fff;
  font-family: "Play", sans-serif;
}

.jcross-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 30px;
}

.nonogram {
  display: grid;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.clues-cols {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 5px;
}

.col-clue {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #111;
  border: 1px solid #444;
  padding: 5px;
  border-radius: 4px;
}

.grid {
  display: flex;
  gap: 5px;
}

.clues-rows {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.row-clue {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background: #111;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 5px;
}

.num {
  padding: 2px 4px;
  color: #9faebf;
  font-weight: bold;
  font-family: "Play", sans-serif;
}

.cells {
  display: grid;
  grid-template-rows: repeat(10, 40px);
  grid-template-columns: repeat(10, 40px);
  gap: 1px;
}

.cell {
  width: 40px;
  height: 40px;
  border: 1px solid #444;
  background-color: #222;
  transition: background 0.2s;
}

.cell.filled {
  background-color: #000;
}

.cell.cross {
  background-color: #444;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
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

.jcross-message {
  margin-top: 20px;
  font-size: 18px;
  color: #ff4444;
}
</style>
