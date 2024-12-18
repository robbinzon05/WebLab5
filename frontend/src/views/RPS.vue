<template>
  <div>
    <h1>Rock Paper Scissors</h1>
    <div class="rps-container">
      <button @click="play('rock')">Rock</button>
      <button @click="play('paper')">Paper</button>
      <button @click="play('scissors')">Scissors</button>
    </div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    async play(choice) {
      try {
        const response = await axios.post('/api/rps/play/', {
          user_choice: choice,
        });
        const { result, server_choice } = response.data;
        if (result === 'win') {
          this.message = `Вы выиграли! Вы: ${choice}, Сервер: ${server_choice}`;
        } else if (result === 'lose') {
          this.message = `Вы проиграли! Вы: ${choice}, Сервер: ${server_choice}`;
        } else {
          this.message = `Ничья! Вы: ${choice}, Сервер: ${server_choice}`;
        }
      } catch (error) {
        console.error('Ошибка при игре:', error);
        this.message = 'Произошла ошибка при игре.';
      }
    },
  },
};
</script>

<style>
.rps-container {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style>
