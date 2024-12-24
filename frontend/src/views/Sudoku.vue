<template>
  <div class="sudoku-container">
    <h1>Sudoku</h1>
    <div class="sudoku-grid">
      <div v-for="(row, i) in puzzle" :key="i" class="sudoku-row">
        <input
          v-for="(cell, j) in row"
          :key="j"
          type="text"
          maxlength="1"
          v-model="userSolution[i][j]"
          :readonly="cell"
        />
      </div>
    </div>
    <div class="button-group">
      <button @click="checkSolution">Проверить решение</button>
      <button @click="load">Restart</button>
      <button @click="back">Back</button>
    </div>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
  data() {
    return {
      puzzle: [],
      userSolution: [],
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
        const response = await axios.get('/api/sudoku/start/');
        this.puzzle = response.data.puzzle;
        this.userSolution = JSON.parse(JSON.stringify(this.puzzle));
        this.message = '';
      } catch (error) {
        console.error('Ошибка при получении пазла:', error);
        this.message = 'Не удалось загрузить пазл.';
      }
    },
    async checkSolution() {
      try {
        const response = await axios.post('/api/sudoku/check/', {
          solution: this.userSolution,
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

<style>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.sudoku-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #000;
  color: #fff;
  font-family: "Play", sans-serif;
}

.sudoku-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 30px;
}

.sudoku-grid {
  display: grid;
  width: 270px;
  height: 270px;
  margin-bottom: 20px;
  margin-right: 50px;
}

.sudoku-row {
  display: flex;
}

.sudoku-row input {
  width: 30px;
  height: 30px;
  text-align: center;
  background: #111;
  color: #fff;
  border: 1px solid #444;
  outline: none;
  font-size: 18px;
  font-weight: bold;
  font-family: "Play", sans-serif;
  transition: box-shadow 0.2s, background 0.2s;
}

.sudoku-row input:focus {
  background: #222;
  box-shadow: 0 0 8px #38f2ba;
}

.sudoku-row input:nth-child(3n) {
  border-right: 3px solid #888;
}
.sudoku-row:nth-child(3n) input {
  border-bottom: 3px solid #888;
}

.sudoku-row input[readonly] {
  background: #333;
  color: #9faebf;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  margin-top: 35px;
}

/* Стили кнопок */
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

/* Сообщение (результат проверки) */
.message {
  margin-top: 10px;
  font-size: 18px;
  color: #ff4444; /* Можно сделать красным для ошибок */
  /* Или проверять, если верное решение => зелёный #28a745 */
}
</style>
