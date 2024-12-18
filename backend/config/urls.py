from django.contrib import admin
from django.urls import path, include
from games.views import sudoku_start, sudoku_check, rps_play

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/sudoku/start', sudoku_start),
    path('api/sudoku/check', sudoku_check),
    path('api/rps/play', rps_play),
]
