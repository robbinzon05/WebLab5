from django.urls import path
from .views import (
    create_lobby_view, join_lobby_view, select_game_view, start_view, dissolve_view,
    sudoku_start, sudoku_check,
    japanese_crossword_start, japanese_crossword_check,
    quiz_start, quiz_check,
    snake_state,
    tetris_state, tetris_action, tetris_start,
    rps_move_view, rps_state_view, get_rps_result,
    lobby_state_view, generate_lobby_code  # новые эндпоинты
)

urlpatterns = [
    path('sudoku/start/', sudoku_start, name='sudoku_start'),
    path('sudoku/check/', sudoku_check, name='sudoku_check'),
    path('japaneseCrossword/start/', japanese_crossword_start, name='japanese_crossword_start'),
    path('japaneseCrossword/check/', japanese_crossword_check, name='japanese_crossword_check'),
    path('quiz/start/', quiz_start, name='quiz_start'),
    path('quiz/check/', quiz_check, name='quiz_check'),
    path('snake/state/', snake_state, name='snake_state'),
    path('tetris/state/', tetris_state, name='tetris_state'),
    path('tetris/start/', tetris_start, name='tetris_start'),
    path('tetris/action/', tetris_action, name='tetris_action'),

    path('create', create_lobby_view, name='create_lobby'),
    path('join', join_lobby_view, name='join_lobby'),
    path('selectGame', select_game_view, name='select_game'),
    path('start', start_view, name='start_game'),
    path('dissolve', dissolve_view, name='dissolve_game'),

    # эндпоинты для RPS (двух игроков)
    path('rps/move', rps_move_view, name='rps_move'),
    path('rps/state', rps_state_view, name='rps_state'),

    path('state', lobby_state_view, name='lobby_state'),
]
