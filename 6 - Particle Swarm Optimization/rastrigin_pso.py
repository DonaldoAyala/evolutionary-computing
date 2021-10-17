# Particle Swarm Optimization for the Rastrigin's function
# Ayala Segoviano Donaldo Horacio
# Escuela Superior de Cómputo
# October 17th 2021

import numpy as np
import math

############################################################################
lower_limit =- 6
upper_limit = 6

n_particles = 100

n_dimensions = 3

# Definition of Rastrigin's function
def f(particle):
    x = particle[0]
    y = particle[1]
    z = particle[2]
    return 30 + x**2 + y**2 + z**2 - 10*math.cos(2*math.pi*x) - 10*math.cos(2*math.pi*y) - 10*math.cos(2*math.pi*z)

# Initialize the particle positions and their velocities with uniformly distributed random vector
particles = lower_limit + (upper_limit - lower_limit) * np.random.rand(n_particles, n_dimensions) 

V = -(upper_limit - lower_limit) + (upper_limit - lower_limit)*np.random.rand(n_particles, n_dimensions)

particles_local_best = particles.copy()
particles_global_best = particles_local_best[0].copy()

# Find the global best
for I in range(0, n_particles):
    if f(particles_local_best[I]) < f(particles_global_best):
        particles_global_best = particles_local_best[I].copy()

count = 0

def iteration():
    global count
    global particles, particles_local_best, particles_global_best, V

    # Loop until convergence, in this example a finite number of iterations chosen
    weight = 0.5 # Factor for the current velocity
    self_influence = 0.3 # The independence of taking decisions
    leader_influence = 0.2 # The influence of the leader over the others

    count += 1

    print (count, "Best particle in:", particles_global_best, " gbest: ", f(particles_global_best))

    # Update the particle velocity and position
    for I in range(0, n_particles):
        for J in range(0, n_dimensions):
          R1 = np.random.rand() # uniform_random_number()
          R2 = np.random.rand() # uniform_random_number()
          # Update the particle's velocity in the J dimention
          V[I][J] = (weight * V[I][J]
                    + self_influence * R1 * (particles_local_best[I][J] - particles[I][J])
                    + leader_influence * R2 * (particles_global_best[J] - particles[I][J]))
          # Update the particle's position in the J dimention
          particles[I][J] = particles[I][J] + V[I][J]
        
        # Check if the new position is better and update local best
        if f(particles[I]) < f(particles_local_best[I]):
            particles_local_best[I] = particles[I].copy()
            # Check if the new local best is better than the global and update the global best
            if f(particles_local_best[I]) < f(particles_global_best):
                particles_global_best = particles_local_best[I].copy()
          
    
####################################################################
# Execution
for i in range(100):
    iteration()