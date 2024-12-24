<template>
  <div class="quiz-container" id="app-quiz">
    <h1>Quiz</h1>
    <div class="quiz">
      <h2>{{ question.question }}</h2>

      <div
        v-for="(option, index) in question.options"
        :key="index"
        :class="[
          'option',
          {
            selected: selectedOption === index,
            correct: index === answer,
            incorrect:
              selectedOption !== answer &&
              selectedOption === index &&
              answer !== -1
          }
        ]"
        @click="checkSolution(index)"
      >
        {{ option }}
      </div>
    </div>

    <div class="button-group">
      <button @click="back">Back</button>
    </div>

    <p v-if="message" class="quiz-message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
  data() {
    return {
      question: {},
      selectedOption: -1,
      message: "",
      answer: -1
    };
  },
  async created() {
    await this.load();
  },
  methods: {
    async back() {
      try {
        this.$router.push("/home");
      } catch (error) {
        console.error("Ошибка при возврате", error);
        this.message = "Ошибка при возврате.";
      }
    },
    async load() {
      try {
        const response = await axios.get("/api/quiz/start/");
        this.question = response.data.question;
        this.selectedOption = -1;
        this.answer = -1; // Сброс ответа
        this.message = ""; // Очистка сообщения
      } catch (error) {
        console.error("Ошибка при получении вопроса:", error);
        this.message = "Не удалось загрузить вопрос.";
      }
    },
    async checkSolution(index) {
      try {
        // Не даём несколько раз кликать на разные варианты
        if (this.selectedOption !== -1) {
          return;
        }
        this.selectedOption = index;

        const response = await axios.post("/api/quiz/check/", {
          answer: this.selectedOption
        });

        // Небольшая задержка, чтобы показать визуально выбор
        setTimeout(() => {
          this.answer = response.data.answer;
          if (response.data.correct) {
            this.message = "Решение верное! Поздравляем!";
          } else {
            this.message = "Решение неверно, попробуйте еще раз.";
          }
        }, 1000);

        // Потом через 2 секунды переходим к новому вопросу
        setTimeout(() => {
          this.load();
        }, 2000);
      } catch (error) {
        console.error("Ошибка при проверке решения:", error);
        this.message = "Произошла ошибка при проверке решения.";
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Play:wght@400;700&display=swap');

.quiz-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: #fff;
  font-family: "Play", sans-serif;
}

.quiz-container h1 {
  font-family: "Dela Gothic One", sans-serif;
  font-size: 50px;
  color: #38f2ba;
  user-select: none;
  margin-bottom: 30px;
}

.quiz {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 400px;
  border: 2px solid #444;
  border-radius: 10px;
  padding: 20px;
  background: #111;
}

.quiz h2 {
  margin-top: 0;
  font-size: 25px;
  font-family: "Play", sans-serif;
  color: #9faebf;
  text-align: center;
}

.option {
  padding: 10px 20px;
  margin: 5px 0;
  border-radius: 8px;
  border: 1px solid #444;
  background: #222;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.3s;
  font-family: "Play", sans-serif;
}

.option:hover {
  background: #333;
  box-shadow: 0 0 10px #333;
}

.option.selected {
  background-color: #484848;
  box-shadow: 0 0 10px #484848;
}

.option.correct {
  background-color: #28a745;
  box-shadow: 0 0 10px #28a745;
}

.option.incorrect {
  background-color: #dc3545;
  box-shadow: 0 0 10px #dc3545;
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

.quiz-message {
  margin-top: 20px;
  font-size: 18px;
  color: #ff4444;
}
</style>
