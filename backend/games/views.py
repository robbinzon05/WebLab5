# backend/games/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import random

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sudoku_start(request):
    puzzle = [
        [0,0,3, 0,2,0, 6,0,0],
        [9,0,0, 3,0,5, 0,0,1],
        [0,0,1, 8,0,6, 4,0,0],

        [0,0,8, 1,0,2, 9,0,0],
        [7,0,0, 0,0,0, 0,0,8],
        [0,0,6, 7,0,8, 2,0,0],

        [0,0,2, 6,0,9, 5,0,0],
        [8,0,0, 2,0,3, 0,0,9],
        [0,0,5, 0,1,0, 3,0,0],
    ]
    return Response({"puzzle": puzzle})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sudoku_check(request):
    solution = request.data.get('solution', [])
    correct = True
    for row in solution:
        if any(cell == 0 or cell == '' for cell in row):
            correct = False
            break
    return Response({"correct": correct})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rps_play(request):
    user_choice = request.data.get('user_choice')
    choices = ['rock', 'paper', 'scissors']
    server_choice = random.choice(choices)

    def rps_result(u, s):
        if u == s:
            return 'draw'
        if (u == 'rock' and s == 'scissors') or \
           (u == 'paper' and s == 'rock') or \
           (u == 'scissors' and s == 'paper'):
            return 'win'
        else:
            return 'lose'

    result = rps_result(user_choice, server_choice)
    return Response({"result": result, "server_choice": server_choice})
