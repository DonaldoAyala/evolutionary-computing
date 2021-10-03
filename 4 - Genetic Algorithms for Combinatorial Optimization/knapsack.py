#GA_for_knapsack.py
#Genetic algorithm find optimal solution to knapsack problem
#Ayala Segoviano Donaldo Horacio

import random
import time
from functools import cmp_to_key

# Knapsack problem
W = 1
n = 20
items_values = [random.randint(0, 100) for i in range(n)]
items_weights = [random.random() for i in range(n)]

print("[")
for i in range(n):
    print((items_values[i], items_weights[i]), end=' ')
print("]")

# Chromosomes will have n bits (same as number of items)
chromosome_length = n
possible_chains = 2**chromosome_length

# Number of chromosomes
number_chromosomes = 10

# Mutation probability
mutation_probability = 1

crossover_point = int(chromosome_length/2)

wheel_length = 10 * number_chromosomes

penalization_factor = 1000000

iterations = 100000

####### PARAMETERS ####### 

def random_binary_string():
    global chromosome_length
    chromosome = []
    for i in range(chromosome_length):
        if random.random() < 0.5:
            chromosome.append(0)
        else:
            chromosome.append(1)

    return chromosome

def calculate_value(chain):
    global items_values
    value = 0
    for i in range(len(chain)):
        if (chain[i] == 1):
            value += items_values[i]
    return value

def calculate_weight(chain):
    global items_weights
    weight = 0
    for i in range(len(chain)):
        if (chain[i] == 1):
            weight += items_weights[i]
    return weight

class Chromosome:
    def __init__(self, items = None):
        if (items is None):
            self.items = random_binary_string()
        else:
            self.items = items
        self.weight = calculate_weight(self.items)
        self.value = calculate_value(self.items)

    def change_items(self, index):
        self.items[index] ^= 1
        self.weight = calculate_weight(self.items)
        self.value = calculate_value(self.items)

# Create initial population
chromosomes = [] 
fitness_values = []

for i in range(0, number_chromosomes):
    chromosomes.append(Chromosome())
    # Initially all chromosomes have a fitnes of 0
    fitness_values.append(0)

# Fitness function
def fitness(chromosome: Chromosome):
    global W, penalization_factor
    fitness_value = chromosome.value
    if (chromosome.weight > W):
        fitness_value -= (chromosome.weight - W) * penalization_factor
    return fitness_value

# Get the fitness of each chromosome in the population
def evaluate_chromosomes():
    global number_chromosomes, chromosomes, fitness_values

    for i in range(number_chromosomes):
        fitness_values[i] = fitness(chromosomes[i])
        
def compare_chromosomes(chromosome1, chromosome2):
    fitness_c1 = fitness(chromosome1)
    fitness_c2 = fitness(chromosome2)
    if fitness_c1 < fitness_c2:
        return 1
    elif fitness_c1 == fitness_c2:
        return 0
    else:
        return -1

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

def crossover(chromosome1, chromosome2):
    global chromosome_length
    new_items1 = chromosome1.items[0:crossover_point] + chromosome2.items[crossover_point: chromosome_length]
    new_chromosome1 = Chromosome(new_items1)

    new_items2 = chromosome2.items[0:crossover_point] + chromosome1.items[crossover_point: chromosome_length]
    new_chromosome2 = Chromosome(new_items2)

    return new_chromosome1, new_chromosome2

def mutate(chromosome):
    global mutation_probability
    if random.random() < mutation_probability:
        chromosome.change_items(int(round(random.random() * (chromosome_length - 1))))

next_gen_chromosomes = chromosomes[:]

iteration_number = 0

def next_generation():
    global iteration_number
    
    chromosomes.sort(key=cmp_to_key(compare_chromosomes) )
    iteration_number += 1
    if (iteration_number == 1 or iteration_number == iterations):
        print( "Best solution so far in iteration ", iteration_number)
        best_chromosome = chromosomes[0]
        print(best_chromosome.items)
        print("f(",best_chromosome.weight, ", ", best_chromosome.value, ") = ", fitness(best_chromosome))

                                                                    
    # Elitism, the best two chromosomes go directly to the next generation
    next_gen_chromosomes[0] = chromosomes[0]
    next_gen_chromosomes[1] = chromosomes[1]

    roulette = create_wheel()

    for i in range(0, int((number_chromosomes - 2) / 2)):
        #Two parents are selected
        parent1 = chromosomes[random.choice(roulette)]
        parent2 = chromosomes[random.choice(roulette)]
        
        #Two descendants are generated with crossover
        new_chromosome1, new_chromosome2 = crossover(parent1, parent2)

        #Each descendant is mutated with probability mutation_probability
        mutate(new_chromosome1)
        mutate(new_chromosome2)

        #The descendants are added to F1
        next_gen_chromosomes[2*i + 2] = new_chromosome1
        next_gen_chromosomes[2*i + 3] = new_chromosome2

    #The generation replaces the old one
    chromosomes[:] = next_gen_chromosomes[:]

chromosomes.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

def get_decimal(items):
    value = 0
    for i in range(len(items)):
        value += items[i] * (2 ** (len(items) - i))


for i in range(iterations):
    next_generation()