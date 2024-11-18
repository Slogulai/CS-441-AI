# Christopher Sloggett
# CS 441 AI

import random

BOARD_SIZE = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
MAX_GENERATIONS = 5000
MAX_FITNESS = 28

# This fitness function counts the number of pairs of queens, the number of attacking pairs of queens
# and then subtracts the attacking pairs from the total pairs to get the fitness value
def fitness(board) -> int:
    attacking_pairs = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j]: # Checking if queens are in the same row
                attacking_pairs += 1
            elif (i - j) == (board[i] - board[j]): # Checking if queens are in the same diagonal (/)
                attacking_pairs += 1 
            elif (j - i) == (board[i] - board[j]): # Checking if queens are in the same diagonal (\)
                attacking_pairs += 1

    return MAX_FITNESS - attacking_pairs # A perfect solution will return 28 which means there are no attacking pairs

# I believe this to be correct for select
def select(queen_positions) -> tuple:
    # Error checking to make sure I always have queen_positions
    if not queen_positions:
        raise ValueError("queen_positions is empty")
    
    fitness_values = []
    for board in queen_positions:
        fitness_values.append(fitness(board))
    total_fitness = sum(fitness_values)

    # Normalizing the fitness values as suggested on the assignment
    normalized_fitness_values = []
    for score in fitness_values:
        normalized_fitness_values.append(score / total_fitness)

    max_parent1, max_parent2 = -1, -1
    parent1, parent2 = None, None
    
    # Picking the best two parents out of the population
    for i in range(len(queen_positions)):
        board = queen_positions[i]
        score = normalized_fitness_values[i]

        if score > max_parent1:
            max_parent2 = max_parent1
            parent2 = parent1
            max_parent1 = score
            parent1 = board
        elif score > max_parent2:
            max_parent2 = score
            parent2 = board

    return parent1, parent2

# Crossover function that takes two parents and creates two children, returning a tuple
def crossover(parent1, parent2) -> tuple:
    child1, child2 = [], []

    for i in range(BOARD_SIZE):
        child1.append(parent1[i])
        child2.append(parent2[i])

    return child1, child2

def mutate(board) -> None:
    if random.random() < MUTATION_RATE: # This will apply a mutation if random.random() < 0.1
        i, j = random.sample(range(BOARD_SIZE), 2) # Using random.sample to select two unique indices of the children
        board[i], board[j] = board[j], board[i]

# I tried two different methods for generating the population with the random function. 
# Initially I tried with random.randint, which I figured would give a more true randomness to the distribution. 
# I found with random.randint it was very rare that I would find a solution, even with my generations set to 5000
# I went with random.sample as that does guarantee no two members of the population are the same which gave a much
# higher chance of finding a solution
def generate_queen_positions() -> list: 
    population = []
    board = []
    for _ in range(POPULATION_SIZE):
        board = random.sample(range(BOARD_SIZE), BOARD_SIZE)
        population.append(board)
    return population

# The beans of the program 
if __name__ == "__main__":
    num_runs = 5

    print(f"\n\nTesting genetic algorithm {num_runs} times...")
    print(f"Population size: {POPULATION_SIZE}")
    print(f"Board size: {BOARD_SIZE} x {BOARD_SIZE}")
    print("-----------------------------------------------------")

    successful_runs = 0
    total_generations = 0
    solutions = []

    for run in range(num_runs):
        print(f"\nRun {run + 1}:")
        population = generate_queen_positions()
        optimal_board = None
        best_board_fitness = 0

        for generation in range(MAX_GENERATIONS):
            # calculating the fitness of the population itself
            fitness_values = []
            for board in population:
                fitness_values.append(fitness(board))
            current_best_fitness = max(fitness_values)
            

            # Keep track of best solution, ie elitism
            if current_best_fitness >= best_board_fitness:
                best_board_fitness = current_best_fitness
                optimal_board = population[fitness_values.index(current_best_fitness)]
                if generation % 100 == 0 and (generation > 0 or generation < 50):
                    print(f"Generation {generation}: Best={current_best_fitness}, Avg={(sum(fitness_values) / len(fitness_values)):.2f}")
                    print(f"Best board: {optimal_board}")

            # Check if a solution has been found 
            if current_best_fitness == MAX_FITNESS:
                print(f"Solution found in generation {generation}!")
                successful_runs += 1
                total_generations += generation
                solutions.append(optimal_board)
                break

            # Create new populatoin with elitism
            new_population = [optimal_board] 
            
            # Creating the rest of the population with the new children
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = select(population)
                child1, child2 = crossover(parent1, parent2)
                mutate(child1)
                mutate(child2)
                new_population.extend([child1, child2])
            
            population = new_population[:POPULATION_SIZE]

            if generation == MAX_GENERATIONS - 1:
                print("\nNo solution found!!")

    # Printing the statisitics of the runs 
    print("\nFinal Stats:")
    print(f"Success rate: {successful_runs}/{num_runs} ({successful_runs/num_runs*100}%)")
    if successful_runs > 0:
        print(f"Average generations to solution: {total_generations/successful_runs:.2f}")
        print("\nSolutions:")
        num = 1
        for solution in solutions:
            print(f"Solution {num}: {solution}")
            num += 1 
        print()



