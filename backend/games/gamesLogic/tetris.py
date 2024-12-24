import  random

SHAPES = {
    "I": [(-2, 0), (-1, 0), (0, 0), (1, 0)],
    "O": [(1, 1), (0, 0), (1, 0), (0, 1)],
    "T": [(0, 1), (-1, 0), (0, 0), (1, 0)],
    "S": [(-1, 1), (1, 0), (0, 0), (0, 1)],
    "Z": [(1, 1), (-1, 0), (0, 0), (0, 1)],
    "J": [(0, 1), (0, 0), (1, 1), (2, 1)],
    "L": [(-1, 1), (0, 0), (0, 1), (-2, 1)]
}

ROTATIONS = {
    "I": [
        [(-2, 0), (-1, 0), (0, 0), (1, 0)],
        [(0, 2), (0, 1), (0, 0), (0, -1)],
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [ (0, 1),(0, -2), (0, -1), (0, 0)]
        # (0, 0), (0, 0),(0, 0),(0, 0)
    ],
    "O": [
        [(0, 1), (0, 0), (1, 0), (1, 1)]
    ],
    "T": [
        [(0, 1), (-1, 0), (0, 0), (1, 0)],
        [(0, 0), (0, 1), (0, -1), (-1, 0)],
        [(-1, 0), (0, 0), (1, 0), (0, -1)],
        [(0, 0), (0, 1), (0, -1), (1, 0)]
    ],
    "S": [
        [(-1, 1), (1, 0), (0, 0), (0, 1)],
        [(0, 1), (0, 0), (-1, 0), (-1, -1)],
    ],
    "Z": [
        [(1, 1), (-1, 0), (0, 0), (0, 1)],
        [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    ],
    "J": [
        [(0, 1), (0, 0), (1, 1), (2, 1)],
        [(-1, 2), (-1, 1), (-1, 0), (0, 0)],
        [(0, 0), (0, -1), (-1, -1), (-2, -1)],
        [(0, 0), (1, -1), (2, -1), (0, -1)]
    ],

    "L": [
        [(-1, 1), (0, 0), (0, 1), (-2, 1)],
        [(-1, 0), (-1, -1), (-1, -2), (0, 0)],
        [(0, 0), (1, -1), (2, -1), (0, -1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ]
}

WIDTH = 10
HEIGHT = 15


def spawn_piece():
    shape = random.choice(list(SHAPES.keys()))
    positions = [(x + WIDTH // 2, y) for x, y in SHAPES[shape]]
    return {"shape": shape, "cells": positions, "rotation": 0}


def move_piece(cells, direction):
    if direction == "down":
        return [(x, y + 1) for x, y in cells]
    elif direction == "left":
        return [(x - 1, y) for x, y in cells]
    elif direction == "right":
        return [(x + 1, y) for x, y in cells]


def rotate_piece(piece):
    shape, cells, rotation = piece["shape"], piece["cells"], piece["rotation"]
    pivot_x, pivot_y = cells[0]  # Use the first cell as the pivot point
    new_rotation = (rotation + 1) % len(ROTATIONS[shape])
    new_cells = [(pivot_x - dx, pivot_y - dy) for dx, dy in ROTATIONS[shape][rotation]]
    pivot_x, pivot_y = new_cells[0]
    new_cells = [(pivot_x + dx, pivot_y + dy) for dx, dy in ROTATIONS[shape][new_rotation]]
    return {"shape": shape, "cells": new_cells, "rotation": new_rotation}


def is_valid_position(cells, block_cells):
    return all(0 <= x < WIDTH and 0 <= y < HEIGHT and (x, y) not in block_cells for x, y in cells)

