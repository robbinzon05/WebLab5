<template>
  <div class="profile-edit-container">
    <h1>Редактирование профиля</h1>

    <form @submit.prevent="handleUpdate">
      <div class="form-row">
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required />
      </div>

      <div class="form-row">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>

      <div class="form-row">
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required />
      </div>

      <div class="form-row">
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
      </div>

      <p v-if="selectedAvatarMessage">{{ selectedAvatarMessage }}</p>

      <button type="submit">Сохранить изменения</button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from '../plugins/axios';
import { mapGetters } from 'vuex';

import avatar1 from '@/assets/avatars/avatar1.png';
import avatar2 from '@/assets/avatars/avatar2.png';
import avatar3 from '@/assets/avatars/avatar3.png';
import avatar4 from '@/assets/avatars/avatar4.png';
import avatar5 from '@/assets/avatars/avatar5.png';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      avatarId: '',
      selectedAvatarMessage: '',
      avatars: [
        { id: 'id_1', name: 'Аватар 1', src: avatar1 },
        { id: 'id_2', name: 'Аватар 2', src: avatar2 },
        { id: 'id_3', name: 'Аватар 3', src: avatar3 },
        { id: 'id_4', name: 'Аватар 4', src: avatar4 },
        { id: 'id_5', name: 'Аватар 5', src: avatar5 }
      ],
      message: '',
    };
  },
  computed: {
    ...mapGetters(['getUser']),
  },
  created() {
    if (this.$store.getters.isAuthenticated) {
      this.loadUserData();
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    loadUserData() {
      const user = this.getUser;
      if (user) {
        this.username = user.username;
        this.email = user.email;
        this.avatarId = user.avatar_id || '';
      } else {
        console.error('Пользователь не найден.');
        this.message = 'Не удалось загрузить данные пользователя.';
      }
    },
    selectAvatar(id) {
      this.avatarId = id;
      const selectedAvatar = this.avatars.find((avatar) => avatar.id === id);
      this.selectedAvatarMessage = `Вы выбрали: ${selectedAvatar.name}`;
    },
    async handleUpdate() {
      try {
        await axios.put('/api/auth/update/', {
          username: this.username,
          email: this.email,
          password: this.password,
          avatar_id: this.avatarId,
        });

        // Сохраняем обновленные данные в localStorage (пример)
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
@import url('https://fonts.googleapis.com/css2?family=Commissioner:wght@100..900&family=Dela+Gothic+One&family=Oswald:wght@200..700&family=Play:wght@400;700&display=swap');

.profile-edit-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.profile-edit-container h1 {
  user-select: none;
  font-family: "Dela Gothic One", serif;
  color: #38f2ba;
  font-size: 50px;
  margin-bottom: 30px;
}

.profile-edit-container form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.profile-edit-container p {
    font-family: "Play", serif;
    color: #9faebf;
    user-select: none;
}

.form-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.form-row label {
  user-select: none;
  font-family: "Play", serif;
  color: #9faebf;
  flex: 0 0 150px;
}

.form-row input {
  flex: 1;
  max-width: 300px;
  padding: 5px;
  background: #222;
  color: #fff;
  border: 1px solid #444;
  border-radius: 4px;
  font-family: "Play", serif;
}

.profile-edit-container button {
  user-select: none;
  font-family: "Play", serif;
  font-size: 17px;
  background: #38f2ba;
  color: #000;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.3s;
}
.profile-edit-container button:hover {
  background: #48ffc9;
}

.profile-edit-container p {
  margin-top: 10px;
}

.avatar-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 300px;
}
.avatar {
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}
.avatar:hover {
  border-color: #007bff;
}
.avatar.selected {
  border-color: #28a745;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}
.avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .form-row label {
    flex: none;
    margin-bottom: 5px;
  }
  .form-row input {
    max-width: 100%;
  }
  .profile-edit-container h1 {
    font-size: 35px;
  }
}
</style>
