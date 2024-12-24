from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .gamesLogic.sudoku import is_valid_sudoku, get_sudoku
from .gamesLogic.japaneseCrossword import generate_nonogram, is_valid_japanese_crossword
from .gamesLogic.quiz import get_random_question, check_answer
from .gamesLogic.tetris import is_valid_position, spawn_piece, move_piece, rotate_piece, WIDTH
import random
import string

# Это упрощенная логика. В реальности вы должны хранить лобби в базе данных.
lobbies = {}  # Словарь вида { code: { code: '...', players: [...], leaderId: ..., selectedGame: None } }
answer_quiz = 0  # Потом можно закинуть этов бд
scope_tetris = 0

def generate_lobby_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lobby_view(request):
    user = request.user
    code = generate_lobby_code()
    lobbies[code] = {
        'code': code,
        'players': [{'id': user.id, 'username': user.username, 'isLeader': True}],
        'leaderId': user.id,
        'selectedGame': None
    }

    return Response(lobbies[code])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_lobby_view(request):
    user = request.user
    code = request.data.get('code', '')

    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)
    lobby = lobbies[code]

    if len(lobby['players']) >= 4:
        return Response({'detail': 'Лобби полно.'}, status=400)

    # Проверим, не в лобби ли уже пользователь
    for p in lobby['players']:
        if p['id'] == user.id:
            return Response(lobby)  # Уже в лобби
    lobby['players'].append({'id': user.id, 'username': user.username, 'isLeader': False})

    return Response(lobby)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_game_view(request):
    user = request.user
    code = request.data.get('code', '')
    game = request.data.get('game', '')

    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)

    lobby = lobbies[code]
    # Проверяем, в лобби ли пользователь
    if not any(p['id'] == user.id for p in lobby['players']):
        return Response({'detail': 'Вы не в этом лобби.'}, status=403)
    # Устанавливаем игру
    lobby['selectedGame'] = game

    return Response(lobby)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_view(request):
    user = request.user
    code = request.data.get('code', '')
    game = request.data.get('game')
    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)

    lobby = lobbies[code]
    lobby['game'] = game
    lobby['gameInProgress'] = True
    # Проверяем, лидер ли пользователь
    if lobby['leaderId'] != user.id:
        return Response({'detail': 'Только лидер лобби может начать игру.'}, status=403)
    # Здесь можно проверить условия запуска игры
    # Пока просто возвращаем успех
    return Response({'detail': 'Игра запущена.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dissolve_view(request):
    user = request.user
    code = request.data.get('code', '')

    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)
    lobby = lobbies[code]

    if lobby['leaderId'] != user.id:
        return Response({'detail': 'Только лидер может расформировать лобби.'}, status=403)
    # Удаляем лобби
    del lobbies[code]
    return Response({'detail': 'Лобби расформировано.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sudoku_start(request):
    sudoku = get_sudoku()

    return Response({"puzzle": sudoku})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sudoku_check(request):
    solution = request.data.get('solution', [])
    correct = True
    for i in range(9):
        for j in range(9):
            if not (is_valid_sudoku(solution, i, j, int(solution[i][j]))) or int(solution[i][j]) == 0:
                correct = False
                break
        if not correct:
            break

    return Response({"correct": correct})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def japanese_crossword_start(request):
    size = 10
    crossword = generate_nonogram(size)
    return Response({"rowClues": crossword["row_clues"], "colClues": crossword["col_clues"], "size": size})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def japanese_crossword_check(request):
    solution = request.data.get('solution', [])
    rows = request.data.get('rowClues', [])
    cols = request.data.get('colClues', [])
    size = request.data.get('size', [])
    correct = is_valid_japanese_crossword(solution, rows, cols, size)

    return Response({"correct": correct})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quiz_start(request):
    global answer_quiz
    question = get_random_question()
    answer_quiz = question["answer"]

    return Response({"question": {"question": question["question"], "options": question["options"]}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quiz_check(request):
    answer = request.data.get('answer', [])
    correct = check_answer(answer, answer_quiz)

    return Response({"correct": correct, "answer": answer_quiz})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rps_move_view(request):
    user = request.user
    code = request.data.get('code', '')
    move = request.data.get('move', '')

    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)

    lobby = lobbies[code]

    if lobby.get('game') != 'rps' or not lobby.get('gameInProgress'):
        return Response({'detail': 'Игра RPS не запущена.'}, status=400)
    # Проверяем, что пользователь в лобби
    player = None

    for p in lobby['players']:
        if p['id'] == user.id:
            player = p
            break
    if not player:
        return Response({'detail': 'Вы не в этом лобби.'}, status=403)

    if move not in ['rock', 'paper', 'scissors']:
        return Response({'detail': 'Некорректный ход.'}, status=400)

    if 'rpsMoves' not in lobby:
        lobby['rpsMoves'] = {}

    lobby['rpsMoves'][user.id] = move

    # Если оба сделали ход
    if len(lobby['rpsMoves']) == 2:
        # Определяем победителя
        moves = list(lobby['rpsMoves'].items())  # [(playerId, move), (playerId, move)]
        p1_id, p1_move = moves[0]
        p2_id, p2_move = moves[1]

        result = get_rps_result(p1_move, p2_move)

        # Результат: 'draw', 'p1', 'p2'
        if result == 'draw':
            lobby['rpsResult'] = 'draw'
        elif result == 'p1':
            lobby['rpsResult'] = p1_id
        else:
            lobby['rpsResult'] = p2_id

        # Завершаем игру
        lobby['gameInProgress'] = False

    return Response({'detail': 'Ход принят', 'rpsMoves': lobby['rpsMoves']})


def get_rps_result(m1, m2):
    if m1 == m2:
        return 'draw'
    if (m1 == 'rock' and m2 == 'scissors') or \
            (m1 == 'paper' and m2 == 'rock') or \
            (m1 == 'scissors' and m2 == 'paper'):
        return 'p1'
    else:
        return 'p2'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rps_state_view(request):
    # Этот эндпоинт будем дергать с фронта, чтобы узнать состояние игры
    user = request.user
    code = request.query_params.get('code', '')

    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)
    lobby = lobbies[code]

    # Проверим, в лобби ли пользователь
    if not any(p['id'] == user.id for p in lobby['players']):
        # Пользователя нет в лобби, значит его выкинуло
        return Response({'detail': 'Вы больше не в лобби.'}, status=403)

    if lobby.get('game') != 'rps':
        # Игра не rps, значит возможно вернуться в лобби
        return Response({'status': 'no_game'})

    if not lobby.get('gameInProgress'):
        # Игра завершилась, есть rpsResult
        if 'rpsResult' in lobby:
            res = lobby['rpsResult']
            if res == 'draw':
                result_msg = 'Ничья!'
            else:
                winner_id = res
                # Определим имя победителя
                winner_name = None
                for p in lobby['players']:
                    if p['id'] == winner_id:
                        winner_name = p['username']
                if winner_name:
                    result_msg = f'Победитель: {winner_name}'
                else:
                    result_msg = 'Ошибка при определении победителя'
            # Игра окончена, можно всех вернуть в лобби
            # Расформируем игру (или оставим лобби без игры)
            lobby['game'] = None
            lobby['rpsMoves'] = {}
            lobby['rpsResult'] = None
            return Response({'status': 'finished', 'message': result_msg})
        else:
            # Игра прервалась или кто-то вышел
            return Response({'status': 'no_game'})

    # Игра идёт
    # Проверим, сколько игроков в лобби
    if len(lobby['players']) < 2:
        # Один вышел, вернуть другого в лобби
        lobby['game'] = None
        lobby['rpsMoves'] = {}
        return Response({'status': 'opponent_left'})

    # Игра в процессе, оба игрока на месте
    moves_done = len(lobby.get('rpsMoves', {}))
    return Response({'status': 'in_progress', 'moves_done': moves_done})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lobby_state_view(request):
    user = request.user
    code = request.query_params.get('code', '')
    if code not in lobbies:
        return Response({'detail': 'Лобби не найдено.'}, status=404)
    lobby = lobbies[code]
    # Проверяем, в лобби ли пользователь
    if not any(p['id'] == user.id for p in lobby['players']):
        return Response({'detail': 'Вы не в этом лобби.'}, status=403)

    return Response({
        'game': lobby.get('game'),
        'gameInProgress': lobby.get('gameInProgress', False),
        'players': lobby['players'],
        'leaderId': lobby['leaderId'],
        'selectedGame': lobby.get('selectedGame'),
        'code': lobby['code'],
    })




def get_next_position(snake, direction):
    head_x, head_y = snake[0]
    if direction == "up":
        return (head_x, head_y - 1)
    elif direction == "down":
        return (head_x, head_y + 1)
    elif direction == "left":
        return (head_x - 1, head_y)
    elif direction == "right":
        return (head_x + 1, head_y)


@api_view(['Post'])
@permission_classes([IsAuthenticated])
def snake_state(request):
    data = request.data
    snake = [(pos % 20, pos // 20) for pos in data.get('snake', [])]
    direction = data.get('direction')
    food = (data.get('food') % 20, data.get('food') // 20)
    new_head = (0, 0)
    # Get new head position
    if len(snake) != 0:
        new_head = get_next_position(snake, direction)

    # Check collisions
    if new_head in snake or not (0 <= new_head[0] < 20 and 0 <= new_head[1] < 20) or len(snake) == 0:
        return Response({"snake": [], "food": data['food'], "message": "Game over"})  # Game over

    # Move snake
    new_snake = [new_head] + snake[:-1]

    # Check if food eaten
    if new_head == food:
        new_snake.append(snake[-1])
        food = (random.randint(0, 19), random.randint(0, 19))

    # Convert positions back to grid indices
    snake_indices = [pos[1] * 20 + pos[0] for pos in new_snake]
    food_index = food[1] * 20 + food[0]

    return Response({"snake": snake_indices, "food": food_index})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tetris_start(request):
    global scope_tetris
    scope_tetris = 0

    return Response({"scope": scope_tetris})


@api_view(['Post'])
@permission_classes([IsAuthenticated])
def tetris_state(request):
    global scope_tetris
    data = request.data
    message = ''
    incorrect = False

    active_piece = {
        "shape": data.get('shape'),
        "cells": [(pos % WIDTH, pos // WIDTH) for pos in data.get('cells', [])],
        "rotation": data.get('rotation', 0)
    }
    block_cells = [(pos % WIDTH, pos // WIDTH) for pos in data.get('blockCells', [])]

    # Move active piece down
    new_active_cells = move_piece(active_piece['cells'], "down")

    # Check collision with blocks or bottom
    if not is_valid_position(new_active_cells, block_cells) or len(active_piece['cells']) == 0:
        block_cells.extend(active_piece['cells'])
        new_active_piece = spawn_piece()
        scope_tetris += 1
    else:

        active_piece['cells'] = new_active_cells
        new_active_piece = active_piece

    # Check completed lines
    rows = {y for _, y in block_cells}
    completed_rows = {y for y in rows if sum(1 for x, y2 in block_cells if y2 == y) == WIDTH}
    block_cells = [(x, y) for x, y in block_cells if y not in completed_rows]

    scope_tetris += 100 * len(completed_rows)
    new_block_cells = []
    for x, y in block_cells:
        new_y = y
        for y2 in completed_rows:
            if y <= y2:
                new_y += 1
        new_block_cells.append((x, new_y))

    if sum(1 for x, y in new_block_cells if y == 0) > 0:
        message = "Game over"
        incorrect = True
    # Convert back to grid indices
    active_indices = [y * WIDTH + x for x, y in new_active_piece['cells']]
    block_indices = [y * WIDTH + x for x, y in new_block_cells]

    return Response({"shape": new_active_piece['shape'], "cells": active_indices,
                     "rotation": new_active_piece['rotation'], "blockCells": block_indices, 'message': message,
                     'incorrect': incorrect, "scope": scope_tetris})


@api_view(['Post'])
@permission_classes([IsAuthenticated])
def tetris_action(request):
    data = request.data
    action = data.get("action")
    message = ''
    incorrect = False

    active_piece = {
        "shape": data.get('shape'),
        "cells": [(pos % WIDTH, pos // WIDTH) for pos in data.get('cells', [])],
        "rotation": data.get('rotation', 0)
    }
    block_cells = [(pos % WIDTH, pos // WIDTH) for pos in data.get('blockCells', [])]

    if action == "left":
        new_cells = move_piece(active_piece['cells'], "left")
        if is_valid_position(new_cells, block_cells):
            active_piece['cells'] = new_cells
    elif action == "right":
        new_cells = move_piece(active_piece['cells'], "right")
        if is_valid_position(new_cells, block_cells):
            active_piece['cells'] = new_cells
    elif action == "down":
        new_cells = move_piece(active_piece['cells'], "down")
        if is_valid_position(new_cells, block_cells):
            active_piece['cells'] = new_cells
    elif action == "rotate":
        rotated_piece = rotate_piece(active_piece)
        if is_valid_position(rotated_piece['cells'], block_cells):
            active_piece = rotated_piece

    if sum(1 for x, y in block_cells if y == 0) > 0:
        message = "Game over"
        incorrect = True

    # Convert back to grid indices
    active_indices = [y * WIDTH + x for x, y in active_piece['cells']]
    return Response({"shape": active_piece['shape'], "cells": active_indices,
                     "rotation": active_piece['rotation'], 'message': message, 'incorrect': incorrect})