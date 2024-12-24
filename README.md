# 🎮 RPS (Rock, Paper, Scissors) Online Game

RPS (Rock, Paper, Scissors) Online Game — это многопользовательская игра, в которой игроки могут участвовать в быстрых матчах "Камень, Ножницы, Бумага". Проект включает в себя взаимодействия в реальном времени, простой пользовательский интерфейс и надежную логику бэкенда для обеспечения честной игры.

## Функции

### 🎲 Игровая функциональность
- **Многопользовательская поддержка**: Игроки в одной лобби могут присоединяться к матчу RPS и играть в реальном времени.
- **Динамическая система лобби**: Игроки могут присоединяться и покидать лобби без нарушения текущих игр.
- **Обеспечение честной игры**:
  - Игроки не могут делать несколько ходов в одном раунде.
  - Если игрок выходит из игры, другой игрок также получает уведомление и перенаправляется на главную страницу.

### 🌐 Фронтенд
- Построен с использованием Vue.js для адаптивного и удобного интерфейса.
- Обновления в реальном времени для игровых состояний, включая ходы и результаты раундов.
- Автоматическое перенаправление, если игрок покидает игру.

### ⚙️ Бэкенд
- Разработан с использованием Django.
- Реализует отслеживание состояния игры и надежную обработку ошибок для обеспечения плавного опыта.
- Предотвращает дублирование ходов в одном раунде с помощью серверной валидации.

## Как это работает

### 🛠️ Рабочий процесс
1. Игроки входят в лобби.
2. Игровая сессия начинается, когда два игрока присоединяются к матчу.
3. Каждый игрок делает свой ход (Камень, Ножницы или Бумага).
4. Бэкенд определяет победителя и обновляет состояние игры.
5. Игра сбрасывается для следующего раунда или заканчивается, если игрок покидает игру.

### 🚪 Выход из игры
- Когда игрок выходит, происходит следующее:
  - Выходящий игрок вызывает метод `stop_rps_view`.
  - Оставшийся игрок видит статус=`no_game` и перенаправляется на главную страницу.

### ❌ Предотвращение повторных ходов
- Бэкенд обеспечивает честную игру, проверяя, сделал ли пользователь уже ход в текущем раунде.
- Если обнаружен повторный ход, сервер отвечает с ошибкой 400.

## Настройка

### 📋 Предварительные требования
- Python 3.9+
- Node.js 14+
- Django
- Vue.js
  
### 🔧 Установка

#### Бэкенд
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/rps-game.git
2. Перейдите в директорию бэкенда:
   ```bash
   cd rps-game/backend
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
4. Запустите сервер:
   ```bash
   python manage.py runserver
#### Фронтенд
1. Перейдите в директорию фронтенда:
   ```bash
   cd rps-game/frontend
2. Установите зависимости:
   ```bash
   npm install
3. Запустите сервер разработки:
   ```bash
   npm run serve

## 🎉 Использование
- Доступ к приложению по адресу http://localhost:8000.
- Присоединяйтесь к лобби и начинайте играть в "Камень, Ножницы, Бумага"!
- Следуйте инструкциям на экране, чтобы делать ходы, просматривать результаты или выходить из игры.
## 🚀 Будущие улучшения
- Добавить поддержку нескольких лобби.
- Реализовать систему рейтинга для игроков.
- Расширить выбор игр, включая дополнительные мини-игры.
## 🤝 Содействие
- Pull-запросы приветствуются. Для крупных изменений, пожалуйста, сначала откройте проблему, чтобы обсудить, что вы хотели бы изменить.
## 📜 Лицензия
- Этот проект лицензирован под MIT License. См. файл LICENSE для подробностей.
## 🙏 Благодарности
-Особая благодарность всем участникам и тестировщикам, которые помогли улучшить проект!
## Технологический стек
-SPA - Vue 3 + TypeScript + Design System
-REST - Django REST Framework
-Docker
-CI - GitHub Actions / Buildbot / и

