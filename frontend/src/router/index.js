import { createRouter, createWebHistory } from 'vue-router';
import store from '../store';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Sudoku from '../views/Sudoku.vue';
import Quiz from '../views/Quiz.vue';
import JapaneseCrossword from '../views/JapaneseCrossword.vue';
import Snake from '../views/Snake.vue';
import Tetris from '../views/Tetris.vue';
import RPS from '../views/RPS.vue'; // Rock Paper Scissors
import Profile from '../views/Profile.vue'; // Убедитесь, что этот импорт правильный


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login, meta: { guestOnly: true, title: 'Вход' } },
  { path: '/register', name: 'Register', component: Register, meta: { guestOnly: true, title: 'Регистрация' } },
  { path: '/home', name: 'Home', component: Home, meta: { requiresAuth: true, title: 'Главная'} },
  { path: '/sudoku', name: 'Sudoku', component: Sudoku, meta: { requiresAuth: true, title: 'Sudoku' } },
  { path: '/quiz', name: 'Quiz', component: Quiz, meta: { requiresAuth: true, title: 'Quiz' } },
  { path: '/japaneseCrossword', name: 'JapaneseCrossword', component: JapaneseCrossword, meta: { requiresAuth: true, title: 'Crossword' } },
  { path: '/snake', name: 'Snake', component: Snake, meta: { requiresAuth: true, title: 'Змейка' } },
  { path: '/tetris', name: 'Tetris', component: Tetris, meta: { requiresAuth: true, title: 'Тетрис' } },
  { path: '/rps', name: 'RPS', component: RPS, meta: { requiresAuth: true, title: 'RPS' } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true, title: 'Профиль' } }, // Добавьте этот маршрут

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next('/login');
  } else if (to.meta.guestOnly && store.getters.isAuthenticated) {
    next('/home');
  } else {
    next();
  }
});

router.afterEach((to, from) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  } else {
    document.title = '???';
  }
});

export default router;
