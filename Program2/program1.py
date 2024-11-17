# Christopher Sloggett
# CS 441 AI

import random

BOARD_SIZE = 8
POPULATION_SIZE = 25 
MUTATION_RATE = 0.1
MAX_GENERATIONS = 1000

# This fitness function counts the number of pairs of queens, the number of attacking pairs of queens
# and then subtracts the attacking pairs from the total pairs to get the fitness value
def fitness(board) -> int:
    total_pairs = (len(board) * (len(board) - 1)) // 2

    attacking_pairs = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j]:
                attacking_pairs += 1
            elif (i - j) == (board[i] - board[j]):
                attacking_pairs += 1
            elif (j - i) == (board[i] - board[j]):
                attacking_pairs += 1

    return total_pairs - attacking_pairs

# I believe this to be correct for normalizing, 
def normalize_fitness(queen_positions) -> list:
    # Error checking to make sure I always have queen_positions
    if not queen_positions:
        raise ValueError("queen_positions is empty")
    
    # Setting up the fitness values list to calculate against the total fitness later
    fitness_values = []
    normalized_values = []
    
    # Creating a current_fitness list that holds that fitness of the board itself 
    for board in queen_positions:
        current_fitness = fitness(board)
        fitness_values.append(current_fitness) # Appending current_fitness to fitness_values

    total_fitness = sum(fitness_values) # Summing the fitness values to get the total fitness

    for fitness_value in fitness_values: 
        normalized_value = fitness_value / total_fitness
        normalized_values.append(normalized_value)
    
    return normalized_values

# I believe this to be correct for select
def select(queen_positions, normalized_fitness) -> tuple:
    if not queen_positions:
        raise ValueError("queen_positions is empty")

    cumulative_fitness = []
    parents = []
    cumulative_sum = 0
    
    # Calculating the cumulative fitness of the queen_positions
    for fitness_value in normalized_fitness:
        cumulative_sum += fitness_value
        cumulative_fitness.append(cumulative_sum)

    # Selecting parents based on the cumulative fitness
    while len(parents) < 2:
        # Creating a threshold value for a random value based on cumulative fitness
        threshold = random.uniform(0, cumulative_sum)
        # Finding the parents with the cumulative fitness that is greater than the threshold
        for index, cumul_fitness in enumerate(cumulative_fitness):
            if threshold <= cumul_fitness:
                parents.append(queen_positions[index])
                break
    
    return parents[0], parents[1]

# I believe this to be correct for crossover
def crossover(parent1, parent2) -> tuple:
    
    # Randomly selecting a crossover point for the childrens mutation
    crossover_point = random.randint(0, BOARD_SIZE - 1)

    # Creating two children by swapping the parents genes at the crossover point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

def mutate(board) -> None:
    if random.random() < MUTATION_RATE: # This will apply a mutation if random.random() < 0.1
        i, j = random.sample(range(BOARD_SIZE), 2)
        board[i], board[j] = board[j], board[i]

def generate_queen_positions() -> list: 
    # using list comprehension to make a population of randomly generated queen positions
    return [random.sample(range(BOARD_SIZE), BOARD_SIZE) for _ in range(POPULATION_SIZE)]

def run_genetic_algorithm(num_runs=1) -> None:
    print(f"\nRunning genetic algorithm {num_runs} times...")
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
            fitness_values = [fitness(board) for board in population] # Using list comprehension
            current_best_fitness = max(fitness_values)
            avg_queen_conflicts = sum(fitness_values) / len(fitness_values)
            
            # Keep track of best solution
            if current_best_fitness >= best_board_fitness:
                best_board_fitness = current_best_fitness
                optimal_board = population[fitness_values.index(current_best_fitness)]
                if generation % 100 == 0 and generation > 0:
                    print(f"Generation {generation}: Best={current_best_fitness}, Avg={avg_queen_conflicts}")

            # Check for solution
            if current_best_fitness == (BOARD_SIZE * (BOARD_SIZE - 1)) // 2:
                print(f"Solution found in generation {generation}!")
                successful_runs += 1
                total_generations += generation
                solutions.append(optimal_board)
                break

            # Create new queen_positions with elitism
            new_population = [optimal_board]  # Preserve best solution
            
            # Fill rest of queen_positions
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = select(population, normalize_fitness(population))
                child1, child2 = crossover(parent1, parent2)
                mutate(child1)
                mutate(child2)
                new_population.extend([child1, child2])
            
            population = new_population[:POPULATION_SIZE]

    # Print summary statistics
    print("\nFinal Statistics:")
    print(f"Success rate: {successful_runs}/{num_runs} ({successful_runs/num_runs*100}%)")
    if successful_runs > 0:
        print(f"Average generations to solution: {total_generations/successful_runs:.2f}")
        print("\nSolutions:")
        for i, solution in enumerate(solutions):
            print(f"Solution {i+1}: {solution}")
        print()




if __name__ == "__main__":
    run_genetic_algorithm(10)