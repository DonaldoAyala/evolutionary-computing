import cv2
import numpy as np
from IPython import display as display

import ipywidgets as ipw
import PIL
from io import BytesIO
import random

class Particle:
  MAX_VELOCITY = np.sqrt(4)
  
  def __init__(self, x_position, y_position, x_velocity, y_velocity, radio, is_wall_particle = False):
    self.radio = radio
    self.position = np.array([float(x_position), float(y_position)])
    self.velocity = np.array([float(x_velocity), float(y_velocity)])
    self.is_wall_particle = is_wall_particle
    self.force = np.array([0.0, 0.0])
  
  def normalize_vector(self, x):
    norm = np.linalg.norm(x)
    if norm == 0:
      return x * np.inf
    return x / norm
    
  def calculate_force(self, particle):
    if self.is_wall_particle:
      return np.array([0.,0.])
    position2 = particle.position
    distance = np.linalg.norm(self.position - position2)
    if distance <= self.radio + particle.radio:
      return self.normalize_vector(self.position - position2) / (distance ** 2)*100
    
    return np.array([0.,0.])
  
  def update_position(self):
    if self.is_wall_particle:
      return
    self.position += self.velocity

  def update_velocity(self):
    if self.is_wall_particle:
      return
    self.velocity += self.force

    velocity_magnitude = np.linalg.norm(self.velocity)

    if velocity_magnitude > self.MAX_VELOCITY:
      self.velocity = self.normalize_vector(self.velocity) * self.MAX_VELOCITY
    return
    
  def graph(self, x0, y0, img):
    if self.is_wall_particle:
      color = (255, 255, 255)
      cv2.circle(img, (int(x0 + self.position[0]), int(y0 - self.position[1])), int(self.radio) - 10, color, -1)
    else:
      color = (255, 0, 0)
      cv2.circle(img, (int(x0 + self.position[0]), int(y0 - self.position[1])), int(self.radio), color, -1)

    
    return


particles = []

def lineOfWallParticles(x1, y1, x2, y2, N):
  x=np.linspace(x1, x2, N)
  y=np.linspace(y1, y2, N)
  for i in range(N):
    particles.append(Particle(x[i], y[i], 0, 0, 20, True))

wIm = ipw.Image()
display.display(wIm)

maxX=500
maxY=500
x0 = int(maxX/2)
y0 = int(maxY/2)
particles_radio = 6
  
img = np.zeros((500, 500, 3), dtype="uint8")

height = 100
width = 100
lineOfWallParticles(-width,height,width,height, int(width / 10 + 3)) # Bottom boundary
lineOfWallParticles(-width,-height,width,-height, int(width / 10 + 3)) # Upper boundary
lineOfWallParticles(-width,height,-width,-height, int(height / 10 + 3)) # Left boundary
#lineOfWallParticles(width,-height,width,height, int(height / 10 + 3))
lineOfWallParticles(width,-height,width,-20, int(height / 10 + 3)) 
lineOfWallParticles(width,20,width,height, int(height / 10 + 3))

# Draw obstacle in front of exit
lineOfWallParticles(45,5,55,0, 2)
lineOfWallParticles(55,0,45,-5, 2)
lineOfWallParticles(45,-5,35,0, 2)
lineOfWallParticles(35,0,45,5, 2)

for i in range(50):
  particles.append(Particle(random.randint(-width + 20, -width + 40), random.randint(-height + 20, height - 20), random.random(), random.random() - 0.5, particles_radio))
  #particles.append(Particle(random.randint(-width + 20, width - 20), random.randint(-height + 20, height - 20), random.random(), random.random() - 0.5, particles_radio))

MaxIterations = 10000

NumParticles = len(particles)
exit = np.array([200, 0])


for count in range(MaxIterations):
  img[:] = (0, 0, 0)
  for i in range(NumParticles):
    for j in range(NumParticles):
      if i != j:
        Fij = particles[i].calculate_force(particles[j])
        particles[i].force += Fij
        # Add a force to pull them to the exit
        norm = np.linalg.norm(exit - particles[i].position)
        exit_force = (exit - particles[i].position ) / (norm if norm > 0 else 1)
        exit_force[0] *= 0.001
        exit_force[1] *= 0.009
        particles[i].force += exit_force

  for particle in particles:
    particle.update_velocity()
    particle.update_position()
    particle.graph(x0, y0, img)
    particle.force[:] = 0
  pilIm = PIL.Image.fromarray(img, mode="RGB")
  with BytesIO() as fOut:
      pilIm.save(fOut, format="png")
      byPng = fOut.getvalue()
        
  wIm.value=byPng  