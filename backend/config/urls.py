from django.contrib import admin
from django.urls import path, include
from games.views import sudoku_start, sudoku_check, japanese_crossword_start, japanese_crossword_check, quiz_start, quiz_check, snake_state, tetris_state, tetris_action,tetris_start
from accounts.views import RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Эндпоинты для Sudoku
    path('api/sudoku/start/', sudoku_start, name='sudoku_start'),
    path('api/sudoku/check/', sudoku_check, name='sudoku_check'),
    path('api/quiz/start/', quiz_start, name='quiz_start'),
    path('api/quiz/check/', quiz_check, name='quiz_check'),
    path('api/japaneseCrossword/start/', japanese_crossword_start, name='japanese_crossword_start'),
    path('api/japaneseCrossword/check/', japanese_crossword_check, name='japanese_crossword_check'),
    path('api/snake/state/', snake_state, name='snake_state'),
    path('api/tetris/state/', tetris_state, name='tetris_state'),
    path('api/tetris/start/', tetris_start, name='tetris_start'),
    path('api/tetris/action/', tetris_action, name='tetris_action'),

    # Эндпоинты для аутентификации
    path('api/auth/', include('accounts.urls')),  # Подключаем маршруты из accounts

    # Эндпоинты для игр (включая новые для RPS)
    path('api/lobby/', include('games.urls')),  # Подключаем маршруты из games
]
