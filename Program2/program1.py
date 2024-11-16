# Christopher Sloggett
# CS 441 AI

import random

BOARD_SIZE = 8
POPULATION_SIZE = 200
MUTATION_RATE = 0.1
MAX_GENERATIONS = 10000

# This fitness function counts the number of pairs of queens, the number of attacking pairs of queens
# and then subtracts the attacking pairs from the total pairs to get the fitness value
def fitness(member):
    total_pairs = (len(member) * (len(member) - 1)) // 2

    attacking_pairs = 0
    for i in range(len(member)):
        for j in range(i + 1, len(member)):
            if member[i] == member[j] or abs(i - j) == abs(member[i] - member[j]):
                attacking_pairs += 1
                
    return total_pairs - attacking_pairs

# I believe this to be correct for normalizing, 
def normalize_fitness(population):
    fitness_values = []
    for member in population:
        current_fitness = fitness(member)
        fitness_values.append(current_fitness)

    total_fitness = sum(fitness_values)

    normalized_values = []
    for fitness_value in fitness_values: 
        normalized_value = fitness_value / total_fitness
        normalized_values.append(normalized_value)
    
    return normalized_values

# I believe this to be correct for select
def select(population, normalized_fitness):
    cumulative_fitness = []
    cumulative_sum = 0
    
    # Calculating the cumulative fitness of the population
    for fitness_value in normalized_fitness:
        cumulative_sum += fitness_value
        cumulative_fitness.append(cumulative_sum)

    parents = []
    # Selecting parents based on the cumulative fitness
    while len(parents) < 2:
        # Creating a threshold value for a random value based on cumulative fitness
        threshold = random.uniform(0, cumulative_sum)
        # Finding the parents with the cumulative fitness that is greater than the threshold
        for index, cumul_fitness in enumerate(cumulative_fitness):
            if threshold <= cumul_fitness:
                parents.append(population[index])
                break
    
    return parents[0], parents[1]

# I believe this to be correct for crossover
def crossover(parent1, parent2):
    # Randomly select a crossover point
    crossover_point = random.randint(0, BOARD_SIZE - 1)

    # Create two children by swapping the parents genes at the crossover point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2

def mutate(member):
    if random.random() < MUTATION_RATE: # This will apply a mutation if random.random() < 0.1
        i, j = random.sample(range(BOARD_SIZE), 2)
        member[i], member[j] = member[j], member[i]

def generate_population(): 
    population = []
    for i in range(POPULATION_SIZE):
        member = list(range(BOARD_SIZE))
        random.shuffle(member)
        population.append(member)
    
    return population

def run_genetic_algorithm(num_runs=5):
    """
    Run genetic algorithm multiple times and collect statistics
    
    Args:
        num_runs (int): Number of times to run the algorithm
    """
    print(f"Running genetic algorithm {num_runs} times...")
    print(f"Population size: {POPULATION_SIZE}")
    print(f"Board size: {BOARD_SIZE}")
    print("-" * 50)

    successful_runs = 0
    total_generations = 0
    solutions = []

    for run in range(num_runs):
        print(f"\nRun {run + 1}:")
        population = generate_population()
        best_fitness_overall = 0
        generations_without_improvement = 0

        for generation in range(MAX_GENERATIONS):
            fitness_values = [fitness(member) for member in population]
            best_fitness = max(fitness_values)
            avg_fitness = sum(fitness_values) / len(fitness_values)
            
            if best_fitness > best_fitness_overall:
                best_fitness_overall = best_fitness
                generations_without_improvement = 0
                print(f"Generation {generation}: Best={best_fitness}, Avg={avg_fitness:.2f}")
            else:
                generations_without_improvement += 1
            
            if generation % 100 == 0 and generation != 0:
                print(f"Generation {generation}: Best={best_fitness}, Avg={avg_fitness:.2f}")

            if best_fitness == (BOARD_SIZE * (BOARD_SIZE - 1)) // 2:
                print(f"Solution found in generation {generation}!")
                successful_runs += 1
                total_generations += generation
                solutions.append(population[fitness_values.index(best_fitness)])
                break

            if generations_without_improvement == MAX_GENERATIONS:
                print("Stalled - no improvement {MAX_GENERATIONS} generations")
                break

            new_population = []
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = select(population, normalize_fitness(population))
                child1, child2 = crossover(parent1, parent2)
                mutate(child1)
                mutate(child2)
                new_population.extend([child1, child2])
            population = new_population[:POPULATION_SIZE]

    # Print summary statistics
    print("\nFinal Statistics:")
    print(f"Success rate: {successful_runs}/{num_runs} ({successful_runs/num_runs*100:.1f}%)")
    if successful_runs > 0:
        print(f"Average generations to solution: {total_generations/successful_runs:.1f}")
        print("\nExample solutions:")
        for i, solution in enumerate(solutions[:3]):
            print(f"Solution {i+1}: {solution}")




if __name__ == "__main__":
    run_genetic_algorithm(50)