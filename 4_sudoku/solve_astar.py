# solve_astar.py
import heapq
import copy
from utils import mrv_cell, is_valid, zero_number

def board_to_tuple(board):
    """Chuyển bảng điền từ list sang tuple"""
    return tuple(tuple(row) for row in board)

def solve_astar(initial_board):
    """Giải Sudoku bằng A* và heuristic MRV"""
    initial = copy.deepcopy(initial_board)
    initial_tuple = board_to_tuple(initial)

    # key, value
    gScore = {initial_tuple: 0}                     # Chi phí từ start đến vị trí hiện tại
    fScore = {initial_tuple: zero_number(initial)}  # Ước tính: gScore + heuristic

    # OpenSet là các priority queue chứa các tuple (fScore, gScore, state)
    openSet = [(fScore[initial_tuple], gScore[initial_tuple], initial)]
    closeSet = set()

    while openSet:
        _, current_g, current_state = heapq.heappop(openSet)
        current_tuple = board_to_tuple(current_state)

        # Nếu không còn ô trống là đã tìm được lời giải
        if zero_number(current_state) == 0:
            for i in range(9):
                initial_board[i][:] = current_state[i][:]
            return True
    
        closeSet.add(current_tuple)
        cell = mrv_cell(current_tuple)
        if cell is None:
            continue
        row, col, candidates = cell

        for num in candidates:
            if is_valid(current_state, row, col, num):
                new_state = copy.deepcopy(current_state)
                new_state[row][col] = num
                new_tuple = board_to_tuple(new_state)

                tentative_g = current_g + 1 # mỗi bước +1
                # Nếu tuple là trường hợp trùng và tốn nhiều bước hơn thì bỏ qua
                if new_tuple in gScore and tentative_g >= gScore[new_tuple]:
                    continue
                
                # Cập nhật trạng thái hiện tại và đi tiếp
                gScore[new_tuple] = tentative_g
                new_f = tentative_g + zero_number(new_state)
                fScore[new_tuple] = new_f
                if new_tuple not in closeSet:
                    heapq.heappush(openSet, (new_f, tentative_g, new_state))

    return False