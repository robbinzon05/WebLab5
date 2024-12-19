from django.contrib import admin
from django.urls import path, include
from games.views import sudoku_start, sudoku_check, rps_play
from accounts.views import RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Эндпоинты для Sudoku
    path('api/sudoku/start/', sudoku_start, name='sudoku_start'),
    path('api/sudoku/check/', sudoku_check, name='sudoku_check'),

    # Эндпоинт для RPS (Rock Paper Scissors)
    path('api/rps/play/', rps_play, name='rps_play'),

    # Эндпоинты для аутентификации
    path('api/auth/', include('accounts.urls')),  # Убедитесь, что это правильно
]
