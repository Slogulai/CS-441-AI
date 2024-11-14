# Christopher Sloggett
# CS 441 AI

import random

BOARD_SIZE = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
MAX_GENERATIONS = 1000

#Is this actually the fitness??
def fitness(member):
    # Count number of queens that are attacking each other
    attacking = 0
    for i in range(BOARD_SIZE):
        for j in range(i + 1, BOARD_SIZE):
            if member[i] == member[j] or abs(i - j) == abs(member[i] - member[j]):
                attacking += 1
    return BOARD_SIZE - attacking

# I believe this to be correct for normalizing
def normalize_fitness(population):
    fitness = [fitness(member) for member in population]
    total = sum(fitness)
    return [f / total for f in fitness] 

# I believe this to be correct for select
def select(population, normalized_fitness):
    fitness = []
    sum = 0

    # Calculating the cumulutive sum of the normalized fitness
    for fitness in normalized_fitness:
        sum += fitness
        fitness.append(sum)

    # Selecting the two best parents
    parents = []
    for i in range(2):
        rand = random.random()
        for j, value in enumerate(fitness):
            if rand <= value:
                parents.append(population[j])
    
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
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(BOARD_SIZE), 2)
        member[i], member[j] = member[j], member[i]