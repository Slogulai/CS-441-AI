# Christopher Sloggett
# CS 441 AI Fall 2024
# Christopher Sloggett
# CS 441 AI Fall 2024
import heapq
import math

class PuzzleState:
    def __init__(self, board, blank_pos, moves=0, previous=None):
        self.board = board
        self.blank_pos = blank_pos
        self.moves = moves
        self.previous = previous

    def __lt__(self, other):
        # This method is no longer needed to compare heuristics directly
        return False

    def heuristic_misplaced_tiles(self):
        goal = [(1, 2, 3), (4, 5, 6), (7, 8, 'b')]
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 'b' and self.board[i][j] != goal[i][j]:
                    misplaced += 1
        return misplaced

    def heuristic_manhattan(self):
        distance = 0
        goal = [(1, 2, 3), (4, 5, 6), (7, 8, 'b')]
        goal_positions = {goal[i][j]: (i, j) for i in range(3) for j in range(3)}
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 'b':
                    goal_pos = goal_positions[self.board[i][j]]
                    distance += abs(goal_pos[0] - i) + abs(goal_pos[1] - j)
        return distance

    def heuristic_euclidean(self):
        distance = 0
        goal = [(1, 2, 3), (4, 5, 6), (7, 8, 'b')]
        goal_positions = {goal[i][j]: (i, j) for i in range(3) for j in range(3)}
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 'b':
                    goal_pos = goal_positions[self.board[i][j]]
                    distance += math.sqrt((goal_pos[0] - i) ** 2 + (goal_pos[1] - j) ** 2)
        return distance

    def get_neighbors(self):
        neighbors = []
        x, y = self.blank_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [list(row) for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(new_board, (nx, ny), self.moves + 1, self))
        return neighbors

    def is_goal(self):
        return self.board == [(1, 2, 3), (4, 5, 6), (7, 8, 'b')]

    def __repr__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

def solve_puzzle(start_board, heuristic, max_steps=10000):
    start_blank_pos = [(i, row.index('b')) for i, row in enumerate(start_board) if 'b' in row][0]
    start_state = PuzzleState(start_board, start_blank_pos)
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(start_state), start_state))
    visited = set()
    steps = 0

    while priority_queue and steps < max_steps:
        _, current_state = heapq.heappop(priority_queue)
        if current_state.is_goal():
            return current_state
        visited.add(tuple(map(tuple, current_state.board)))
        for neighbor in current_state.get_neighbors():
            if tuple(map(tuple, neighbor.board)) not in visited:
                heapq.heappush(priority_queue, (heuristic(neighbor), neighbor))
        steps += 1

    return None

def print_solution(solution):
    path = []
    while solution:
        path.append(solution)
        solution = solution.previous
    path.reverse()
    for state in path:
        print(state)
        print()

# Example usage
initial_states = [
    [[4, 5, 'b'], [6, 1, 8], [7, 3, 2]],
    
]

heuristics = [
    ("Misplaced Tiles", PuzzleState.heuristic_misplaced_tiles),
    ("Manhattan Distance", PuzzleState.heuristic_manhattan),
    ("Euclidean Distance", PuzzleState.heuristic_euclidean)
]

for heuristic_name, heuristic in heuristics:
    print(f"Solving with {heuristic_name}:")
    for i, start_board in enumerate(initial_states):
        print(f"Initial state {i + 1}:")
        solution = solve_puzzle(start_board, heuristic)
        if solution:
            print("Solution found:")
            print_solution(solution)
        else:
            print("No solution found within the maximum number of steps.")
        print()