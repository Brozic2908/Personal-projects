# utils.py

def find_empty_cell(board):
    """Finds an empty cell on the board"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def is_valid(board, row, col, num):
    """Checks if a number is valid in the given cell"""
    # Check row, col
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check cell
    box_x, box_y = (col // 3) * 3, (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_y + i][box_x + j] == num:
                return False
    return True

def mrv_cell(board):
    """Tìm ô có ít lựa chọn nhất để chọn trước(MRV heuristic)"""
    best_cell = None
    min_options = 10
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                options = possible_candidates(board, i, j)
                if len(options) < min_options:
                    best_cell = (i, j, options)
                    min_options = len(options)
                    if min_options == 1:
                        return best_cell
    return best_cell

def possible_candidates(board, row, col):
    """Tìm các lựa chọn hợp lệ tại ô (row, col) lưu vào list"""
    return [num for num in range(1, 10) if is_valid(board, row, col, num)]


def zero_number(board):
    """Số các ô trống chưa điền"""
    return sum(cell == 0 for row in board for cell in row)

def is_right_number(board, row, col, num, goal_board):
    """Kiểm tra xem đáp án đúng với kết quả không"""
    return is_valid(board, row, col, num) and num == goal_board[row][col]