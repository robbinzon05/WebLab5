from django.contrib import admin
from django.urls import path, include
from games.views import sudoku_start, sudoku_check
from accounts.views import RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Эндпоинты для Sudoku
    path('api/sudoku/start/', sudoku_start, name='sudoku_start'),
    path('api/sudoku/check/', sudoku_check, name='sudoku_check'),

    # Эндпоинты для аутентификации
    path('api/auth/', include('accounts.urls')),  # Подключаем маршруты из accounts

    # Эндпоинты для игр (включая новые для RPS)
    path('api/lobby/', include('games.urls')),  # Подключаем маршруты из games
]
