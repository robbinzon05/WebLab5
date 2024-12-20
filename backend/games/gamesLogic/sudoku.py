import random


def is_valid_sudoku(board, row, col, num):
    """Проверяет, можно ли разместить число в указанной ячейке."""

    # Проверяем строку
    for i in range(len(board[row])):
        if i != col and board[row][i] == num:
            return False

    # Проверяем столбец
    if num in [board[i][col] for i in range(9) if i != row]:
        return False

    # Проверяем малый квадрат 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num and i != row and j != col:
                return False

    return True


def solve(board):
    """Решает судоку с использованием возвратного поиска."""
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                continue
            for num in range(1, 10):
                if not (is_valid_sudoku(board, row, col, num)):
                    continue
                board[row][col] = num

                if solve(board):
                    return True

                board[row][col] = 0
            return False
    return True


def generate_full_board():
    """Генерирует полностью заполненную доску судоку."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for num in numbers:
                if is_valid_sudoku(board, row, col, num):
                    board[row][col] = num
                    if solve(board):
                        break
                    board[row][col] = 0
    return board


def remove_numbers(board, difficulty="medium"):
    """Удаляет числа из заполненного судоку для создания задачи."""
    cells_to_remove = {
        'easy': 30,
        'medium': 40,
        'hard': 50
    }
    count = cells_to_remove.get(difficulty, 40)
    while count > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            count -= 1
    return board


def get_sudoku():
    board = generate_full_board()
    sudoku = remove_numbers(board)

    return sudoku
