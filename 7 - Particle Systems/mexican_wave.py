import cv2
import numpy as np
from IPython import display as display
import time

import ipywidgets as ipw
import PIL
from io import BytesIO

wIm = ipw.Image()
display.display(wIm)

class CONSTANTS:
  def __init__(self):
    self.min_x = 100
    self.min_y = 100
    self.max_x = 500
    self.max_y = 500
    self.min_radio = 0
    self.max_radio = 5
    self.neighbor_influence = 0.1
    self.spacing = 0
    self.decay_factor = 0.5

const = CONSTANTS()

class Particle:
  def __init__(self, x, y, radio):
    self.x = x
    self.y = y
    self.radio = radio
    self.is_growing = True

class Vector:
  def __init__(self, x, y):
    self.x = x
    self.y = y

movements = [Vector(0,-1), # up
             #Vector(1,-1), # up-right
             Vector(1,0), # right
             #Vector(1,1), # bottom-right
             Vector(0,1), # bottom
             #Vector(-1, 1), # bottom-left
             Vector(-1, 0)] # left
             #Vector(-1, -1)] #up-left

n_x = 30
n_y = 30
part = [[Particle(const.min_x + j*2*(const.max_radio + const.spacing), const.min_x + i*2*(const.max_radio + const.spacing), const.min_radio) for j in range(n_x)] for i in range(n_y)]


def draw_particles(img, particles):
  for rows in particles:
    for particle in rows:
      cv2.circle(img, (particle.x, particle.y), int(particle.radio), (255 - int((particle.radio * 255)/5), 255 - int((particle.radio * 255)/5), 255), -1)

def update(particles):
  global movements, const
  rows = len(particles)
  columns = len(particles[0])
  for i in range(rows):
    for j in range(columns):
      if particles[i][j].is_growing and (0 < i < rows - 1) and (0 < j < columns - 1):
        # Update the radio of the particle influenced by the neighbors
        for move in movements:
          particles[i][j].radio += const.neighbor_influence * particles[i + move.x][j + move.y].radio
      
      if particles[i][j].is_growing and particles[i][j].radio >= const.max_radio:
        particles[i][j].is_growing = False
      
      if not particles[i][j].is_growing:
        if particles[i][j].radio <= 1:
          particles[i][j].radio = 0
        particles[i][j].radio *= const.decay_factor

img = np.zeros((1000, 1000, 3), dtype="uint8")

part[int(n_y/2)][0].radio = 4

draw_particles(img, part)
i = 0

const.neighbor_influence = 0.1
const.decay_factor = 0.9

while True:
  if i % 150 == 0:
    for row in part:
      for particle in row:
        particle.is_growing = True

    
  update(part)
  img[:] = (0,0,0)
  cv2.putText(img,str(i),(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
  i += 1
  draw_particles(img, part)
  pilIm = PIL.Image.fromarray(img, mode="RGB")
  with BytesIO() as fOut:
      pilIm.save(fOut, format="png")
      byPng = fOut.getvalue()
  
  wIm.value=byPng  