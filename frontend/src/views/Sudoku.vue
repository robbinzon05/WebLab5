<template>
  <div>
    <h1>Sudoku</h1>
    <div class="sudoku-grid">
      <div v-for="(row, i) in puzzle" :key="i" class="sudoku-row">
        <input
          v-for="(cell, j) in row"
          :key="j"
          type="text"
          maxlength="1"
          v-model="userSolution[i][j]"
        />
      </div>
    </div>
    <button @click="checkSolution">Проверить решение</button>
    <p v-if="message">{{ message }}</p>
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
    try {
      const response = await axios.get('/api/sudoku/start/');
      this.puzzle = response.data.puzzle;
      this.userSolution = JSON.parse(JSON.stringify(this.puzzle));
    } catch (error) {
      console.error('Ошибка при получении пазла:', error);
      this.message = 'Не удалось загрузить пазл.';
    }
  },
  methods: {
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
.sudoku-grid {
  display: grid;
  grid-template-rows: repeat(9, auto);
}

.sudoku-row {
  display: grid;
  grid-template-columns: repeat(9, auto);
}

.sudoku-row input {
  width: 30px;
  height: 30px;
  text-align: center;
}
</style>
