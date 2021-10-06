#GA_for_knapsack.py
#Genetic algorithm find optimal solution to knapsack problem
#Ayala Segoviano Donaldo Horacio

import random
import time
from functools import cmp_to_key

# Knapsack problem
n = 7

D = [
    [0, 2318, 6663, 2094, 5716, 4771, 6366],
    [2318, 0, 4386, 320, 3422, 5097, 4080],
    [6663, 4386, 0, 4665, 1544, 7175, 1474],
    [2094, 320, 4665, 0, 3624, 4817, 4281],
    [5716, 3422, 1544, 3624, 0, 5699, 697],
    [4771, 5097, 7175, 4817, 5699, 0, 5684],
    [6366, 4080, 1474, 4281, 697, 5684, 0]
    ]

for r in D:
    for e in r:
        print(e, end="")
    print("\\\\ \\hline")

# Chromosomes will permutations of length n
chromosome_length = n

# Number of chromosomes
number_chromosomes = 10

# Mutation probability
mutation_probability = 0.5

# Wheel length
wheel_length = 10 * number_chromosomes

# Number of iterations
iterations = 20

####### PARAMETERS ####### 

def random_permutation():
    global chromosome_length
    permutation = [i for i in range(n)]
    random.shuffle(permutation)

    return permutation[:]
    

class Chromosome:
    def __init__(self, path = None):
        if (path is None):
            self.path = random_permutation()
        else:
            self.path = path

    def change_path(self, index1, index2):
        self.path[index1], self.path[index2] = self.path[index2], self.path[index1]
        
# Create initial population
chromosomes = [] 
fitness_values = []

for i in range(0, number_chromosomes):
    chromosomes.append(Chromosome())
    # Initially all chromosomes have a fitnes of 0
    fitness_values.append(0)

# Fitness function
def fitness(chromosome: Chromosome):
    global D, n
    path = chromosome.path
    cost = 0
    for i in range(len(D) - 1):
        cost += D[path[i]][path[i + 1]]
    cost += D[path[-1]][path[0]]
    
    return cost

# Get the fitness of each chromosome in the population
def evaluate_chromosomes():
    global number_chromosomes, chromosomes, fitness_values

    for i in range(number_chromosomes):
        fitness_values[i] = fitness(chromosomes[i])
        
def compare_chromosomes(chromosome1, chromosome2):
    fitness_c1 = fitness(chromosome1)
    fitness_c2 = fitness(chromosome2)
    if fitness_c1 > fitness_c2:
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
    used_numbers = set()
    option = 0
    new_chromosome = [0 for i in range(chromosome_length)]

    path1 = chromosome1.path
    path2 = chromosome2.path

    def get_next_index(path):
        for i in range(chromosome_length):
            if (path[i] not in used_numbers):
                return i
        return -1

    def get_element_index(path, target):
        for i in range(n):
            if (path[i] == target):
                return i

    while len(used_numbers) < chromosome_length:
        if option == 0:
            insert = get_next_index(path1)
            if insert == -1:
                continue
            new_chromosome[insert] = path1[insert]
            used_numbers.add(path1[insert])

            while True:
                insert = get_element_index(path2, path1[insert])
                if path1[insert] not in used_numbers:
                    new_chromosome[insert] = path1[insert]
                    used_numbers.add(path1[insert])
                else:
                    option = 1
                    break
        else:
            insert = get_next_index(path2)
            if insert == -1:
                continue
            new_chromosome[insert] = path2[insert]
            used_numbers.add(path2[insert])

            while True:
                insert = get_element_index(path1, path2[insert])
                if path2[insert] not in used_numbers:
                    new_chromosome[insert] = path2[insert]
                    used_numbers.add(path2[insert])
                else:
                    option = 0
                    break
    return Chromosome(new_chromosome)

def mutate(chromosome):
    global mutation_probability
    if random.random() < mutation_probability:
        index1 = int(round(random.random() * (chromosome_length - 1)))
        index2 = int(round(random.random() * (chromosome_length - 1)))
        chromosome.change_path(index1, index2)

next_gen_chromosomes = chromosomes[:]

iteration_number = 0

def next_generation():
    global iteration_number
    
    chromosomes.sort(key=cmp_to_key(compare_chromosomes))
    iteration_number += 1
    #if (iteration_number == 1 or iteration_number == iterations):
    print( "Best solution so far in iteration ", iteration_number)
    best_chromosome = chromosomes[0]
    print(best_chromosome.path)
    print("f(", best_chromosome.path, ") = ", fitness(best_chromosome))

                                                                    
    # Elitism, the best two chromosomes go directly to the next generation
    next_gen_chromosomes[0] = chromosomes[0]
    next_gen_chromosomes[1] = chromosomes[1]

    roulette = create_wheel()

    for i in range(0, int((number_chromosomes - 2) / 2)):
        #Two parents are selected
        parent1 = chromosomes[random.choice(roulette)]
        parent2 = chromosomes[random.choice(roulette)]
        
        #Two descendants are generated with crossover
        new_chromosome1 = crossover(parent1, parent2)
        new_chromosome2 = crossover(parent2, parent1)

        #Each descendant is mutated with probability mutation_probability
        mutate(new_chromosome1)
        mutate(new_chromosome2)

        #The descendants are added to F1
        next_gen_chromosomes[2*i + 2] = new_chromosome1
        next_gen_chromosomes[2*i + 3] = new_chromosome2

    #The generation replaces the old one
    chromosomes[:] = next_gen_chromosomes[:]
    evaluate_chromosomes()

chromosomes.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

for i in range(iterations):
    time.sleep(0.5)
    next_generation()
