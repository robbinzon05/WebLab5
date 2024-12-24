import random


# Создание подсказок
def get_clues(line):
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            clues.append(count)
            count = 0
    if count > 0:
        clues.append(count)
    return clues or [0]


def is_valid_japanese_crossword(grid, rows, cols, size=10):
    for i in range(size):
        index = 0
        flag = False

        for j in range(size):
            if index >= len(rows[i]) and grid[j][i]==1:
                return False
            elif grid[j][i]==1:
                rows[i][index] -= 1
                flag = True

                if rows[i][index] < 0:
                    return False
            elif flag:
                if rows[i][index] > 0:
                    return False

                index += 1
                flag = False
        if index < len(rows[i]) and rows[i][index] > 0:
            return False

    for i in range(size):
        index = 0
        flag = False

        for j in range(size):
            if index >= len(cols[i]) and grid[i][j]==1:
                return False
            elif grid[i][j]==1:
                cols[i][index] -= 1
                flag = True

                if cols[i][index] < 0:
                    return False
            elif flag:
                if cols[i][index] > 0:
                    return False

                index += 1
                flag = False
        if index < len(cols[i]) and cols[i][index] > 0:
            return False
    return True


def generate_nonogram(size=10):
    # Генерация случайной сетки
    grid = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    row_clues = [get_clues(row) for row in grid]
    col_clues = [get_clues(col) for col in zip(*grid)]

    return {"grid": grid, "row_clues": row_clues, "col_clues": col_clues}

