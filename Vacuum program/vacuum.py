import random

# Define the environment
class Environment:
    def __init__(self, dirt_piles):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.agent_pos = (random.randint(0, 2), random.randint(0, 2))
        self.dirt_piles = dirt_piles
        self.place_dirt()

    def place_dirt(self):
        for _ in range(self.dirt_piles):
            while True:
                x, y = random.randint(0, 2), random.randint(0, 2)
                if self.grid[x][y] == 0 and (x, y) != self.agent_pos:
                    self.grid[x][y] = 1
                    break

    def is_dirty(self, pos):
        x, y = pos
        return self.grid[x][y] == 1

    def clean(self, pos):
        x, y = pos
        self.grid[x][y] = 0

    def move_agent(self, new_pos):
        self.agent_pos = new_pos

    def clean_murphy(self, pos):
        x, y = pos
        # Murphy's Law: 25% of the time, the suck action fails
        if random.random() < 0.25:
            self.grid[x][y] = 1 - self.grid[x][y]  # Toggle dirt state
        else:
            self.grid[x][y] = 0

    def print_grid(self):
        for i in range(3):
            for j in range(3):
                if (i, j) == self.agent_pos:
                    print("A", end=" ")
                elif self.grid[i][j] == 1:
                    print("D", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()

# Define the agent
class SimpleReflexAgent:
    def __init__(self, environment):
        self.environment = environment
        self.performance_score = 0
        self.steps = 0
        self.max_steps = 1000

    def next_move(self):
        x, y = self.environment.agent_pos
        if self.environment.is_dirty((x, y)):
            self.environment.clean((x, y))
            self.performance_score += 1
        else:
            # Check neighboring cells for dirt and move towards the nearest dirty cell
            neighbors = [
                (x - 1, y),  # Up
                (x + 1, y),  # Down
                (x, y - 1),  # Left
                (x, y + 1)   # Right
            ]
            dirty_neighbors = [pos for pos in neighbors if 0 <= pos[0] < 3 and 0 <= pos[1] < 3 and self.environment.is_dirty(pos)]
            if dirty_neighbors:
                self.environment.move_agent(dirty_neighbors[0])
            else:
                # If no dirty neighbors, move in a predefined pattern
                valid_moves = [pos for pos in neighbors if 0 <= pos[0] < 3 and 0 <= pos[1] < 3]
                if valid_moves:
                    self.environment.move_agent(random.choice(valid_moves))
        self.steps += 1
        #self.environment.print_grid()  # Print the grid after each move

    def run(self):
        while self.steps < self.max_steps:
            self.next_move()
            if all(self.environment.grid[i][j] == 0 for i in range(3) for j in range(3)):
                break

class SimpleMurphyReflexAgent:
    def __init__(self, environment):
        self.environment = environment
        self.performance_score = 0
        self.steps = 0
        self.max_steps = 1000

    def next_move(self):
        x, y = self.environment.agent_pos
        if self.environment.is_dirty((x, y)):
            self.environment.clean_murphy((x, y))
            self.performance_score += 1
        else:
            # Check neighboring cells for dirt and move towards the nearest dirty cell
            neighbors = [
                (x - 1, y),  # Up
                (x + 1, y),  # Down
                (x, y - 1),  # Left
                (x, y + 1)   # Right
            ]
            dirty_neighbors = [pos for pos in neighbors if 0 <= pos[0] < 3 and 0 <= pos[1] < 3 and self.environment.is_dirty(pos)]
            if dirty_neighbors:
                self.environment.move_agent(dirty_neighbors[0])
            else:
                # If no dirty neighbors, move in a predefined pattern
                valid_moves = [pos for pos in neighbors if 0 <= pos[0] < 3 and 0 <= pos[1] < 3]
                if valid_moves:
                    self.environment.move_agent(random.choice(valid_moves))
        self.steps += 1
        #self.environment.print_grid()  # Print the grid after each move

    def run(self):
        while self.steps < self.max_steps:
            self.next_move()
            if all(self.environment.grid[i][j] == 0 for i in range(3) for j in range(3)):
                break

class RandomizedAgent:
    def __init__(self, environment):
        self.environment = environment
        self.performance_score = 0
        self.steps = 0
        self.max_steps = 100  # Maximum number of steps to avoid infinite loops

    def next_move(self):
        x, y = self.environment.agent_pos
        if self.environment.is_dirty((x, y)) and random.choice([True, False]):
            self.environment.clean((x, y))
            self.performance_score += 1
        else:
            # Randomly choose a direction to move
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and x > 0:
                self.environment.move_agent((x - 1, y))
            elif direction == 'down' and x < 2:
                self.environment.move_agent((x + 1, y))
            elif direction == 'left' and y > 0:
                self.environment.move_agent((x, y - 1))
            elif direction == 'right' and y < 2:
                self.environment.move_agent((x, y + 1))
        self.steps += 1
        #self.environment.print_grid()  # Print the grid after each move

    def run(self):
        while self.steps < self.max_steps:
            self.next_move()
            if all(self.environment.grid[i][j] == 0 for i in range(3) for j in range(3)):
                break

class RandomizedMurphyAgent:
    def __init__(self, environment):
        self.environment = environment
        self.performance_score = 0
        self.steps = 0
        self.max_steps = 100  # Maximum number of steps to avoid infinite loops

    def next_move(self):
        x, y = self.environment.agent_pos
        if self.environment.is_dirty((x, y)) and random.choice([True, False]):
            self.environment.clean_murphy((x, y))
            self.performance_score += 1
        else:
            # Randomly choose a direction to move
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and x > 0:
                self.environment.move_agent((x - 1, y))
            elif direction == 'down' and x < 2:
                self.environment.move_agent((x + 1, y))
            elif direction == 'left' and y > 0:
                self.environment.move_agent((x, y - 1))
            elif direction == 'right' and y < 2:
                self.environment.move_agent((x, y + 1))
        self.steps += 1
        #self.environment.print_grid()  # Print the grid after each move

    def run(self):
        while self.steps < self.max_steps:
            self.next_move()
            if all(self.environment.grid[i][j] == 0 for i in range(3) for j in range(3)):
                break


# Run the simulation
def run_simulation_reflexive(dirt_piles):
    environment = Environment(dirt_piles)
    agent = SimpleReflexAgent(environment)
    #environment.print_grid()
    agent.run()
    return agent.performance_score, agent.steps

def run_simulation_random(dirt_piles):
    environment = Environment(dirt_piles)
    agent = RandomizedAgent(environment)
    #environment.print_grid()
    agent.run()
    return agent.performance_score, agent.steps

def run_simulation_random_murphy(dirt_piles):
    environment = Environment(dirt_piles)
    agent = RandomizedMurphyAgent(environment)
    #environment.print_grid()
    agent.run()
    return agent.performance_score, agent.steps

def run_simulation_reflexive_muprhy(dirt_piles):
    environment = Environment(dirt_piles)
    agent = SimpleMurphyReflexAgent(environment)
    #environment.print_grid()
    agent.run()
    return agent.performance_score, agent.steps

# Test cases
for dirt_piles in [1, 3, 5]:
    scores = []
    steps = []
    print()
    print("Reflexive Agent")    
    for _ in range(100):  # Run multiple simulations for each case
        score, step = run_simulation_reflexive(dirt_piles)
        scores.append(score)
        steps.append(step)
    print(f"Dirt Piles: {dirt_piles}, Average Score: {sum(scores)/len(scores)}, Average Steps: {sum(steps)/len(steps)}")
    scores = []
    steps = []
    print("Simple Murphy Reflexive Agent")
    for _ in range(100):  # Run multiple simulations for each case
        score, step = run_simulation_reflexive_muprhy(dirt_piles)
        scores.append(score)
        steps.append(step)
    print(f"Dirt Piles: {dirt_piles}, Average Score: {sum(scores)/len(scores)}, Average Steps: {sum(steps)/len(steps)}")
    scores = []
    steps = []
    print("Randomized Agent")
    for _ in range(100):  # Run multiple simulations for each case
        score, step = run_simulation_random(dirt_piles)
        scores.append(score)
        steps.append(step)
    print(f"Dirt Piles: {dirt_piles}, Average Score: {sum(scores)/len(scores)}, Average Steps: {sum(steps)/len(steps)}")
    scores = []
    steps = []
    print("Randomized Murphy Agent")
    for _ in range(100):  # Run multiple simulations for each case
        score, step = run_simulation_random_murphy(dirt_piles)
        scores.append(score)
        steps.append(step)
    print(f"Dirt Piles: {dirt_piles}, Average Score: {sum(scores)/len(scores)}, Average Steps: {sum(steps)/len(steps)}")