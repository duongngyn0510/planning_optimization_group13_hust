import numpy as np
from util import fitness, crossover, mutation

def create_individual(N, M):
    #an individual is a schedule, individual[i] is timetable for class[i]
    individual=[]
    
    for _ in range(N):
        individual.append([np.random.randint(5), np.random.randint(2), np.random.randint(1, 7), np.random.randint(1, M+1)])    
    
    return individual

def create_next_generation(parent1, parent2, population, M, t, g, s, c):
    """This function creates the next generation of individuals"""
    mutaion_rate = 0.1
    c1, c2 = crossover(parent1, parent2)
    if np.random.uniform(0, 1) < mutaion_rate:
        c1 = mutation(c1, M)
    if np.random.uniform(0, 1) < mutaion_rate:
        c2 = mutation(c2, M)
    population.append(c1)
    population.append(c2)

    fitness_values = [fitness(individual, t, g, s, c) for individual in population]
    sorted_list = sorted(fitness_values, reverse=False)
    position_1 = fitness_values.index(sorted_list[0])
    position_2 = fitness_values.index(sorted_list[1])
    
    if position_1 < position_2:
        population.pop(position_2)
        population.pop(position_1)
    else: 
        population.pop(position_1)
        population.pop(position_2)

    return population

def genetic_algorithm(N, M, generations, population_size, t, g, s, c):
    population = [create_individual(N, M) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate the fitness of each individual
        fitness_values = [fitness(individual, t, g, s, c) for individual in population]
        # Select the parents for crossover and mutation
        sorted_list = sorted(fitness_values, reverse=True)
        position_1 = fitness_values.index(sorted_list[0])
        position_2 = fitness_values.index(sorted_list[1])
        parent1 = population[position_1]
        parent2 = population[position_2]
        # Create the next generation
        population = create_next_generation(parent1, parent2, population, M, t, g, s, c)

    # Select the best individual
    fitness_values = [fitness(individual, t, g, s, c) for individual in population]
    best_individual = population[np.argmax(fitness_values)]
    return best_individual