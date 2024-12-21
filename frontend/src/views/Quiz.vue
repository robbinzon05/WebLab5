<template>
    <div id="app">

         <h1>Quiz</h1>
        <div class="quiz">
            <h2>{{ question.question }}</h2>
            <div v-for="(option, index) in question.options"
                 :key="index"
                 :class="['option', { selected: selectedOption === index, correct: index===answer, incorrect: (selectedOption != answer) && (selectedOption === index) && (answer!=-1)}]"
                 @click="checkSolution(index)">
                {{ option }}
            </div>
        </div>
        <p v-if="message">{{ message }}</p>
    </div>


</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios

export default {
    data() {
        return {
            question: {},
            selectedOption: null,
            message: "",
            answer: -1,
        };
    },
    async created() {
        await this.loadQuestion();
    },
    methods: {
        async loadQuestion() {
            try {
                const response = await axios.get('/api/quiz/start/');
                this.question = response.data.question;
                this.selectedOption = -1;
                this.answer = -1; // Сброс ответа
                this.message = ""; // Очистка сообщения
            } catch (error) {
                console.error('Ошибка при получении пазла:', error);
                this.message = 'Не удалось загрузить пазл.';
            }
        },
        async checkSolution(index) {
            try {
                if (this.selectedOption != -1){
                    return;
                }
                this.selectedOption = index;

                const response = await axios.post('/api/quiz/check/', {
                        answer: this.selectedOption,
                    });

                setTimeout(() => {
                    this.answer = response.data.answer;
                    if (response.data.correct) {
                        this.message = 'Решение верное! Поздравляем!';
                    } else {
                        this.message = 'Решение неверно, попробуйте еще раз.';
                    }
                },1000);
                setTimeout(() => {
                    this.loadQuestion(); // Вызываем loadQuestion вместо created
                }, 2000);
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

.quiz {
  display: grid;
  justify-content: center;
  align-items: center;
  border: 3px solid #000;
}
.option {
    padding: 10px 20px;
    border: 1px solid #ccc;
    margin: 5px 0;
    cursor: pointer;
}

.option.selected {
    background-color: yellow;
}

.option.correct {
    background-color: green;
}

.option.incorrect {
    background-color: red;
}
</style>
