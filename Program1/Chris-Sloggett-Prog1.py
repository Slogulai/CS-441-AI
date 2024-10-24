# Christopher Sloggett
# CS 441 AI Fall 2024

# All credit for this code goes to the below site
# https://www.geeksforgeeks.org/8-puzzle-problem-in-ai/#

import heapq
#import math
from termcolor import colored # Must install term color with pip3 for program to run

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
state_1 = [2, 1, 3, 4, 5, 6, 0, 8, 7]
state_2 = [4, 8, 3, 1, 5, 6, 7, 2, 0]  # 14 inversions
state_3 = [8, 1, 2, 7, 3, 4, 6, 5, 0]  # 8 inversions
state_4 = [6, 8, 3, 0, 1, 5, 7, 4, 2]  # 14 inversions 

# Odd parity state
state_5 = [1, 2, 3, 4, 5, 0, 6, 8, 7]  # 1 inversion

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
    
def heuristic1(board): # Misplaced tile heuristic
    misplaced = 0;
    for i in range(len(board)):
        if board[i] != 0 and board[i] != goal_state[i]:
            misplaced += 1
    return misplaced

def heuristic2(board): # Manhattan distance heuristic
    distance = 0
    for i in range(9):
        if board[i] != 0:
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(board[i] - 1, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def heuristic3(): # Unchosen heuristic
    pass

def count_inversions(board):
    inversions = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                inversions += 1
    return inversions

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

    formatted_path = []
    for step in path:
        formatted_board = []
        for tile in step.board:
            if tile == 0:
                formatted_board.append('b')
            else:
                formatted_board.append(str(tile))
        formatted_path.append(f"({' '.join(formatted_board)})")

    for i in range(len(formatted_path)):
        if i > 0 and i % 5 == 0:
            print()  # Print a new line after every 5 steps
        if i < len(formatted_path) - 1:
            print(formatted_path[i], end=" → ")
        else:
            print(formatted_path[i])

def best_first_search():
    pass

def a_star(start_state, heuristic):
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, PuzzleState(start_state, None, None, 0, heuristic(start_state)))

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

            new_state = PuzzleState(new_board, current_state, move, current_state.depth + 1, current_state.depth + 1 + heuristic(new_board))
            heapq.heappush(open_list, new_state)

    return None


def main():
    initial_states = [state_1, state_2, state_3, state_4, state_5]

    total_steps_h1 = 0
    solutions_h1 = []
    print("Heuristic 1 (Misplaced Tile):")
    for i, state in enumerate(initial_states, start=1):
        print(f"\nState {i}:")
        print_board(state)
        if count_inversions(state) % 2 == 0:
            solution = a_star(state, heuristic1)
            steps = 0
            current = solution
            while current.parent is not None:
                steps += 1
                current = current.parent
            total_steps_h1 += steps
            solutions_h1.append(solution)
            print(f"Solution path {i}:")
            print_solution(solution)
        else:
            print(colored("Odd number of inversions, no solution possible", "red"))
            solutions_h1.append(None)
    average_steps_h1 = total_steps_h1 / len(initial_states)
    print(f"\nAverage number of steps (Heuristic 1): {average_steps_h1}")

    # Compare heuristic 2 (Manhattan distance)
    total_steps_h2 = 0
    solutions_h2 = []
    print("\nHeuristic 2 (Manhattan Distance):")
    for i, state in enumerate(initial_states, start=1):
        print(f"\nState {i}:")
        print_board(state)
        if count_inversions(state) % 2 == 0:
            solution = a_star(state, heuristic2)
            steps = 0
            current = solution
            while current.parent is not None:
                steps += 1
                current = current.parent
            total_steps_h2 += steps
            solutions_h2.append(solution)
            print(f"Solution path {i}:")
            print_solution(solution)
        else:
            print(colored("Odd number of inversions, no solution possible", "red"))
            solutions_h2.append(None)
    average_steps_h2 = total_steps_h2 / len(initial_states)
    print(f"\nAverage number of steps (Heuristic 2): {average_steps_h2}")


#    while True:
#        print("Welcome to the 8 Puzzle using the A* and Best First Search Algorithms!")
#        print("Please choose from the following options:")
#        print("1. A* Algorithm")
#        print("2. Best First Search Algorithm")
#        print("3. Exit")
#
#        choice = input("Enter your choice: ")
#
#        if choice == "1":
#            print("You chose the A* Algorithm")
#            print("The initial state is:")
#            print_board(initial_state)
#            print("Choose a heuristic:")
#            print("1. Misplaced Tiles")
#            print("2. Manhattan Distance")
#            print("3. Unchosen Heuristic")
#
#            a_star_choice = input("Enter your choice: ")
#            
#            if a_star_choice == "1":
#                print("You chose the Misplaced Tiles heuristic")
#                solution = a_star(initial_state, heuristic1)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#            elif a_star_choice == "2":
#                print("You chose the Manhattan Distance heuristic")
#                solution = a_star(initial_state, heuristic2)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#            elif a_star_choice == "3":
#                print("You chose the Unchosen Heuristic")
#                solution = a_star(initial_state, heuristic1)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#
#        elif choice == "2":
#            print("You chose the Best First Search Algorithm")
#            print("The initial state is:")
#            print_board(initial_state)
#            print("Choose a heuristic:")
#            print("1. Misplaced Tiles")
#            print("2. Manhattan Distance")
#            print("3. Unchosen Heuristic")
#
#            bfs_choice = input("Enter your choice: ")
#
#            if bfs_choice == "1":
#                print("You chose the Misplaced Tiles heuristic")
#                solution = best_first_search(initial_state, heuristic1)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#            elif bfs_choice == "2":
#                print("You chose the Manhattan Distance heuristic")
#                solution = best_first_search(initial_state, heuristic2)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#            elif bfs_choice == "3":
#                print("You chose the Unchosen Heuristic")
#                solution = best_first_search(initial_state, heuristic1)
#                if solution:
#                    print(colored("Sloution found: ", "green"))
#                    print_solution(solution)
#                else:
#                    print(colored("No solution found", "red"))
#
#        elif choice == "3":
#            print("You chose to exit the program")
#            break



if __name__ == "__main__":
    main()