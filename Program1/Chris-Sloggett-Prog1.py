# Christopher Sloggett
# CS 441 AI Fall 2024

# All credit for this code goes to the below site
# https://www.geeksforgeeks.org/8-puzzle-problem-in-ai/#

import heapq
#import math
from termcolor import colored

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
initial_state = [4, 5, 0, 6, 1, 8, 7, 3, 2]

moves = {
    'U': -3,
    'D': 3,
    'L': -1,
    'R': 1
}
class PuzzleState:
    def __init__(self, board, parent, move, depth, cost):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost
    
def heuristic1(board):
    distance = 0
    for i in range(9):
        if board[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(board[i] - 1, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def move_tile(board, move, blank_pos):
    new_board = board[:]
    new_blank_pos = blank_pos + moves[move]
    new_board[blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[blank_pos]
    return new_board

def print_board(board):
    print
    print("+---+---+---+")
    for row in range(0, 9, 3):
        row_visual = "|"
        for tile in board[row:row + 3]:
            if tile == 0:  # Blank tile
                row_visual += f" {colored(' ', 'cyan')} |"
            else:
                row_visual += f" {colored(str(tile), 'yellow')} |"
        print(row_visual)
        print("+---+---+---+")        

def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for step in path:
        print(f"Move: {step.move}")
        print_board(step.board)


def a_star(start_state):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic1(start_state)))

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.board == goal_state:
            return current_state

        closed_list.add(tuple(current_state.board))

        blank_pos = current_state.board.index(0)

        for move in moves:
            if move == 'U' and blank_pos < 3:  # Invalid move up
                continue
            if move == 'D' and blank_pos > 5:  # Invalid move down
                continue
            if move == 'L' and blank_pos % 3 == 0:  # Invalid move left
                continue
            if move == 'R' and blank_pos % 3 == 2:  # Invalid move right
                continue

            new_board = move_tile(current_state.board, move, blank_pos)

            if tuple(new_board) in closed_list:
                continue

            new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1, current_state.depth + 1 + heuristic1(new_board))
            heapq.heappush(open_list, new_state)

    return None

solution = a_star(initial_state)

if solution:
    print(colored("Sloution found: ", "green"))
    print_solution(solution)
else:
    print(colored("No solution found", "red"))
