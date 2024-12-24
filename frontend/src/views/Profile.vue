<template>
  <div>
    <h1>Редактирование профиля</h1>
    <form @submit.prevent="handleUpdate">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <label>Выберите аватар:</label>
        <div class="avatar-selection">
          <div
            v-for="avatar in avatars"
            :key="avatar.id"
            class="avatar"
            :class="{ selected: avatar.id === avatarId }" 
            @click="selectAvatar(avatar.id)"
          >
            <img :src="avatar.src" :alt="avatar.name" />
          </div>
        </div>
        <p v-if="selectedAvatarMessage">{{ selectedAvatarMessage }}</p> <!-- Сообщение о выбранном аватаре -->
      </div>
      <button type="submit">Сохранить изменения</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios'; // Используем настроенный экземпляр Axios
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      username: '', // Имя пользователя
      email: '', // Email
      password: '', // Пароль
      avatarId: '', // ID аватара
      selectedAvatarMessage: '', // Сообщение о выбранном аватаре
      avatars: [
        { id: 'id_1', name: 'Аватар 1', src: 'https://via.placeholder.com/100' }, // Заглушка 1
        { id: 'id_2', name: 'Аватар 2', src: 'https://via.placeholder.com/100' }, // Заглушка 2
        { id: 'id_3', name: 'Аватар 3', src: 'https://via.placeholder.com/100' }, // Заглушка 3
      ],
      message: '',
    };
  },
  computed: {
    ...mapGetters(['getUser ']), // Получаем данные пользователя из Vuex
  },
  created() {
    if (this.$store.getters.isAuthenticated) {
      this.loadUserData(); // Загружаем данные пользователя
    } else {
      this.$router.push('/login'); // Перенаправляем на страницу входа, если пользователь не аутентифицирован
    }
  },
  methods: {
    loadUserData() {
      const user = this.getUser ; // Получаем данные текущего пользователя
      if (user) {
        this.username = user.username; // Устанавливаем имя пользователя
        this.email = user.email; // Устанавливаем email
        this.avatarId = user.avatar_id || ''; // Устанавливаем ID аватара
      } else {
        console.error('Пользователь не найден.');
        this.message = 'Не удалось загрузить данные пользователя.';
      }
    },
    selectAvatar(id) {
      this.avatarId = id; // Устанавливаем выбранный аватар
      const selectedAvatar = this.avatars.find(avatar => avatar.id === id);
      this.selectedAvatarMessage = `Вы выбрали: ${selectedAvatar.name}`; // Обновляем сообщение о выбранном аватаре
    },
    async handleUpdate() {
      try {
        await axios.put('/api/auth/update/', {
          username: this.username,
          email: this.email,
          password: this.password,
          avatar_id: this.avatarId, // ID аватара
        });

        // Сохраняем обновленные данные в localStorage
        localStorage.setItem('username', this.username);
        localStorage.setItem('email', this.email);
        localStorage.setItem('avatarId', this.avatarId);

        this.message = 'Профиль успешно обновлен!';
      } catch (error) {
        console.error('Ошибка при обновлении профиля:', error);
        this.message = 'Не удалось обновить профиль.';
      }
    },
  },
};
</script>

<style>
.avatar-selection {
  display: flex;  gap: 10px; /* Расстояние между аватарами */
}

.avatar {
  cursor: pointer; /* Указатель при наведении */
  border: 2px solid transparent; /* Начальный стиль границы */
  transition: border-color 0.3s; /* Плавный переход для границы */
}

.avatar:hover {
  border-color: #007bff; /* Цвет границы при наведении */
}

.avatar.selected {
  border-color: #28a745; /* Цвет границы для выбранного аватара */
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Эффект тени для выделения */
}

.avatar img {
  width: 100px; /* Ширина аватара */
  height: 100px; /* Высота аватара */
  border-radius: 50%; /* Круглая форма аватара */
}
</style>