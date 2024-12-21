<template>
  <div class = "field">
    <h1>Sudoku</h1>
    <div class="sudoku-grid">
      <div v-for="(row, i) in puzzle" :key="i" class="sudoku-row">
        <input
          v-for="(cell, j) in row"
          :key="j"
          type="text"
          maxLength="1"
          v-model="userSolution[i][j]"
          :readonly="cell"
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
.field {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;


}
.sudoku-grid {
  display: grid;
  width: 270px;
  height: 270px;

}

.sudoku-row {
  display: flex;
}

.sudoku-row input {
  width: 30px;
  height: 30px;
  text-align: center;

}


.sudoku-row input:nth-child(3n){
    border: 1px solid #000;
    border-right: 3px solid #000;

}

.sudoku-row:nth-child(3n){
    border-bottom: 3px solid #000;
}
</style>
