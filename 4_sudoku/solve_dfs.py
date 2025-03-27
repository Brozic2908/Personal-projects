# solve_dfs.py

from utils import find_empty_cell, is_valid

def solve_dfs(initial_board):
    empty_cell = find_empty_cell(initial_board)

    if not empty_cell: 
        return True

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(initial_board, row, col, num):
            initial_board[row][col] = num
            if solve_dfs(initial_board):
                return True
            initial_board[row][col] = 0 # Backtracking
    return False