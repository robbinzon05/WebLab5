<template>
  <div id="app">
   <h1>Japanese Crossword</h1>
    <div class="nonogram">
        <div class="clues clues-cols">
            <div v-for="col in colClues"  :key="col" class="col-clue">
                <div v-for="num in col" class="num" :key="num">{{ num }}</div>
            </div>
        </div>

        <div class="grid">
            <div class="clues clues-rows">
                <div v-for="row in rowClues"  :key="row" class="row-clue">
                    <div v-for="num in row" class="num" :key="num">{{ num }}</div>
                </div>
            </div>
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
                        :class="{ filled: cell==1, cross: cell == 2 }"
                        @click="toggleCell(rowIndex, colIndex)"
                    ></div>
                </div>
            </div>
        </div>
    </div>
    <button @click="checkSolution">Проверить решение</button>
    <button @click="load">Restart</button>
    <button @click="back">back</button>
    <p v-if="message">{{ message }}</p>
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
            this.rowClues= response.data.rowClues;
            this.colClues= response.data.colClues;
            this.size = response.data.size;
            this.grid = Array.from({ length: this.size }, () => Array(this.size).fill(false));
            this.message = '';

        } catch (error) {
          console.error('Ошибка при получении пазла:', error);
          alert(error)
          this.message = 'Не удалось загрузить пазл.';
        }
    },
    toggleCell(row, col) {
      this.grid[row][col] = (this.grid[row][col]+1)%3;
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

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
}
.nonogram {
  display: grid;
  justify-content: center;
  align-items: center;
}
.clues-rows {

  display: flex;
   align-items: center;
  flex-direction: column;
}
.clues-cols {
  display: flex;
  flex-direction: row;
  justify-content: center;

}

.col-clue {

  display: flex;
  margin: 0,100,0,0;
   align-items: center;
  flex-direction: column;
  padding: 2px;
  width: 40px;
}
.row-clue {
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding: 2px;
  height: 40px;
}

.num {
    padding: 4px;
}
.grid {
  display: flex;

}
.cells {

  display: grid;
  grid-template-rows: repeat(10, 40px);
  grid-template-columns: repeat(10, 40px);
}
.cell {
  width: 40px;
  height: 40px;
  border: 1px solid #000;
  background-color: #fff;
}
.cell.filled {
  background-color: #000;
}
.cell.cross {
  background-color: gray;
}
</style>
