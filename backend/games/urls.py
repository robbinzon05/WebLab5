from django.urls import path
from .views import sudoku_start, sudoku_check, rps_play

urlpatterns = [
    path('sudoku/start/', sudoku_start, name='sudoku_start'),
    path('sudoku/check/', sudoku_check, name='sudoku_check'),
    path('rps/play/', rps_play, name='rps_play'),
]
