#GA_for_Ackley.ipynb
#Genetic algorithm to optimize Ackley's function
#Ayala Segoviano Donaldo Horacio

import math
import random
from functools import cmp_to_key

#Chromosomes are pairs of numbers of 20 bits each
chromosome_length = 40
possible_chains = 2**chromosome_length

# Search boundaries
x = (-20, 20)
z = (-20, 20)

crossover_point = int(chromosome_length/2)

def random_chromosome():
    chromosome = [[],[]]
    for i in range(0, chromosome_length):
        # More likely to be close to x1, z1
        if random.random() < 0.5:
            chromosome[0].append(0)
        else:
            chromosome[0].append(1)
    
    for i in range(0, chromosome_length):
        # More likely to be close to x1, z1
        if random.random() < 0.5:
            chromosome[1].append(0)
        else:
            chromosome[1].append(1)

    return chromosome

# Number of chromosomes
number_chromosomes = 1000

# Mutation probability
mutation_probability = 0.5

# Create initial population
chromosomes = [] 
fitness_values = []

for i in range(0, number_chromosomes):
    chromosomes.append(random_chromosome())
    # Initially all chromosomes have a fitnes of 0
    fitness_values.append(0)

# binary decodification
def decode_chromosome(chromosome):
    global chromosome_length, possible_chains, x, z
    value_x = 0
    for i in range(chromosome_length):
        value_x += (2**i)*chromosome[0][-1 - i]
    value_x = x[0] + (x[1] - x[0]) * float(value_x) / (possible_chains - 1)

    value_z = 0
    for i in range(chromosome_length):
        value_z += (2**i)*chromosome[1][-1 - i]

    value_z = z[0] + (z[1] - z[0]) * float(value_z) / (possible_chains - 1)
    return value_x, value_z

# Fitness function (Akcleys function)
def fitness(x,z):
    return -20*math.exp(-0.2*(math.sqrt(0.5*math.sqrt(x*x + z*z)))) - math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*z))) + math.exp(1) + 20

# Get the fitness of each chromosome in the population
def evaluate_chromosomes():
    global chromosomes

    for i in range(number_chromosomes):
        x, z = decode_chromosome(chromosomes[i])
        fitness_values[i] = fitness(x, z)
        
def compare_chromosomes(chromosome1, chromosome2):
    xc1, zc1 = decode_chromosome(chromosome1)
    xc2, zc2 = decode_chromosome(chromosome2)
    fitness_c1 = fitness(xc1, zc1)
    fitness_c2 = fitness(xc2, zc2)
    if fitness_c1 > fitness_c2:
        return 1
    elif fitness_c1 == fitness_c2:
        return 0
    else:
        return -1

wheel_length = 10*number_chromosomes

def create_wheel():
    global chromosomes, fitness_values

    max_value = max(fitness_values)
    acc = 0
    for i in range(number_chromosomes):
        acc += max_value - fitness_values[i]

    fraction = []
    for i in range(number_chromosomes):
        fraction.append( float(max_value - fitness_values[i]) / acc)
        if fraction[-1] <= 1.0 / wheel_length:
            fraction[-1] = 1.0 / wheel_length
    
    fraction[0] -= (sum(fraction) - 1.0) / 2
    fraction[1] -= (sum(fraction) - 1.0) / 2
    
    wheel = []

    pc = 0

    for f in fraction:
        Np = int(f * wheel_length)
        for i in range(Np):
            wheel.append(pc)
        pc += 1

    return wheel
        
next_gen_chromosomes = chromosomes[:]

iteration_number = 0

def next_generation():
    global iteration_number
    
    chromosomes.sort(key=cmp_to_key(compare_chromosomes) )
    iteration_number += 1
    print("Iteration", iteration_number)
    print( "Best solution so far:")
    decoded_chromosome = decode_chromosome(chromosomes[0])
    print( "f(",decoded_chromosome,")= ", fitness(decoded_chromosome[0], decoded_chromosome[1]) )
                                                                    
    # Elitism, the best two chromosomes go directly to the next generation
    next_gen_chromosomes[0] = chromosomes[0]
    next_gen_chromosomes[1] = chromosomes[1]

    roulette = create_wheel()

    for i in range(0, int((number_chromosomes - 2) / 2)):
        #Two parents are selected
        parent1 = random.choice(roulette)
        parent2 = random.choice(roulette)
        
        #Two descendants are generated with crossover
        x1 = chromosomes[parent1][0][0:crossover_point] + chromosomes[parent2][0][crossover_point:chromosome_length]
        z1 = chromosomes[parent1][1][0:crossover_point] + chromosomes[parent2][1][crossover_point:chromosome_length]
        new_chromosome1 = [x1, z1]

        x2 = chromosomes[parent2][0][0:crossover_point] + chromosomes[parent1][0][crossover_point:chromosome_length]
        z2 = chromosomes[parent2][1][0:crossover_point] + chromosomes[parent1][1][crossover_point:chromosome_length]
        new_chromosome2 = [x2, z2]

        #Each descendant is mutated with probability mutation_probability
        if random.random() < mutation_probability:
            if (random.random() < 0.5): # Picking x or z part of the chromosome to mutate
              new_chromosome1[0][int(round(random.random()*(chromosome_length - 1)))] ^= 1
            else:
              new_chromosome1[1][int(round(random.random()*(chromosome_length - 1)))] ^= 1

        if random.random() < mutation_probability:
            if (random.random() < 0.5): # Picking x or z part of the chromosome to mutate
              new_chromosome2[0][int(round(random.random()*(chromosome_length - 1)))] ^= 1
            else:
              new_chromosome2[1][int(round(random.random()*(chromosome_length - 1)))] ^= 1

        #The descendants are added to F1
        next_gen_chromosomes[2*i + 2] = new_chromosome1
        next_gen_chromosomes[2*i + 3] = new_chromosome2

    #The generation replaces the old one
    chromosomes[:] = next_gen_chromosomes[:]
    evaluate_chromosomes()

chromosomes.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

for i in range(30):
  next_generation()