# Backend (Django)
FROM python:3.11-slim AS backend

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app/backend

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY backend .

# Выполнение миграций
RUN python manage.py collectstatic --noinput

# Frontend (Vue.js)
FROM node:16 AS frontend

# Установка рабочей директории
WORKDIR /app/frontend

# Копирование зависимостей и установка
COPY frontend/package.json frontend/package-lock.json .
RUN npm install

# Копирование проекта и сборка
COPY frontend .
RUN npm run build

# Финальный образ для запуска приложения
FROM python:3.11-slim AS production

# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование backend из предыдущего этапа
COPY --from=backend /app/backend /app/backend

# Копирование frontend (собранный) из предыдущего этапа
COPY --from=frontend /app/frontend/dist /app/frontend/dist

# Установка переменных окружения
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

# Выполнение миграций при старте контейнера
CMD ["sh", "-c", "cd backend && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
