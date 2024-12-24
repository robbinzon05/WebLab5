<template>
  <div id="app">
    <div id="game-container-tetris">
      <div
        v-for="(cell, index) in grid"
        :key="index"
        :class="[{
          active: activeCells.includes(index),
          block: blockCells.includes(index),
        }, shape]"
        class="cell-tetris">
      </div>
    </div>
    <button @click="startGame">Start Game</button>
    <button @click="back">back</button>
    <p>Ваши очки: {{ scope }}</p>
    <p v-if="message">{{ message }}</p>
  </div>
      <audio ref="audio" hidden controls>
      <source :src="audioFile" type="audio/mp3">
      </audio>
</template>

<script >
import axios from '../plugins/axios';
import audioFile from '../assets/tetrismusic.mp3'

export default {
  data() {
    return {
      grid: Array(150).fill(null), // 10x20 grid
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
        let incorrect = response.data.incorrect;
        this.scope = response.data.scope;
        if (incorrect){
            this.stopGame()
        }
      } catch (error) {
        console.error("Error fetching game state:", error);
      }
    },
    startGame() {
      this.activeCells= [];
      this.blockCells = [];
      this.rotation = 0;
      this.message = '';

      this.stopGame();

      axios.get('/api/tetris/start/');
      this.scope = 0;

      this.$refs.audio.play();

       this.musicInterval = setInterval(() => {
           this.$refs.audio.pause();
           this.$refs.audio.currentTime = 0;
           this.$refs.audio.play();
       }, 102000);//время музыки

      this.intervalId = setInterval(async () => {
        await this.fetchNextState();
      }, 300);
      window.addEventListener("keydown", this.handleKeyDown);
    },
    handleKeyDown(event) {
      const actionMap = {
        ArrowLeft: "left",
        ArrowRight: "right",
        ArrowDown: "down",
        ArrowUp: "rotate"
      };
      if (actionMap[event.key]) {
        this.updateDirection(actionMap[event.key]);
      }
    },
    async updateDirection(action) {
      try {
        const response = await axios.post('/api/tetris/action/', {
         action: action,
         cells: this.activeCells,
         blockCells: this.blockCells,
          shape: this.shape,
          rotation: this.rotation,
        });

        this.activeCells = response.data.cells;
        this.shape = response.data.shape;
        this.rotation = response.data.rotation;
        this.message = response.data.message;
        let incorrect = response.data.incorrect;

        if (incorrect){
            this.stopGame()
        }
      } catch (error) {
        console.error("Error updating action:", error);
      }
    },
    stopGame() {
        this.$refs.audio.pause();
        this.$refs.audio.currentTime = 0;

        if (this.musicInterval) {
            clearInterval(this.musicInterval);
            this.$refs.audio.pause();
            this.$refs.audio.currentTime = 0;
        }
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

#game-container-tetris {
  display: grid;
  grid-template-columns: repeat(10, 30px);
  grid-gap: 2px;
  width: 320px;
  margin: 20px auto;
}
.cell-tetris {
  width: 30px;
  height: 30px;
  background-color: lightgray;
  border: 1px solid #ccc;
}
.cell-tetris.active {
  background-color: blue;
}
.cell-tetris.block {
  background-color: gray;
}
.cell-tetris.I.active {
  background-color: purple;
}
.cell-tetris.T.active {
  background-color: yellow;
}
.cell-tetris.S.active {
  background-color: red ;
}
.cell-tetris.Z.active {
  background-color: red;
}
.cell-tetris.J.active {
  background-color: blue;
}
.cell-tetris.L.active {
  background-color: blue;
}
.cell-tetris.O.active {
  background-color: green;
}
</style>

