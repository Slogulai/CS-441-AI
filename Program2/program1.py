# Christopher Sloggett
# CS 441 AI

import random

BOARD_SIZE = 8
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
MAX_GENERATIONS = 1000

#Is this actually the fitness?? yes, but I would like to do it differently, should be pairs of non attacking queens
def fitness(member):
    # Count number of queens that are attacking each other
    attacking = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if member[i] == member[j] or abs(i - j) == abs(member[i] - member[j]):
                attacking += 1
    return BOARD_SIZE - attacking

# I believe this to be correct for normalizing, 
def normalize_fitness(population):
    fitness_val = [fitness(member) for member in population] # dig deeper into the assignment statement for fitness, and maybe do it in a readable matter
    total = sum(fitness_val) 
    return [f / total for f in fitness_val] 

# I believe this to be correct for select
def select(population, normalized_fitness):
    fitness = []
    sum = 0

    # Calculating the cumulutive sum of the normalized fitness
    for fitness in normalized_fitness:
        sum += fitness
        fitness.append(sum)

    # Selecting the 
    parents = []
    for i in range(2): # i is not used here, should double check this here
        rand = random.random() # This should be based on the best possible fitness, not random
        for j, value in enumerate(fitness):
            if rand <= value: #Rand would be always less than value, so this would pick bad candidates
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
    if random.random() < MUTATION_RATE: # This will always apply a mutation if random.random() < 0.1
        i, j = random.sample(range(BOARD_SIZE), 2)
        member[i], member[j] = member[j], member[i]