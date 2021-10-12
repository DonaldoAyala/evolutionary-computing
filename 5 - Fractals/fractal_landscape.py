import cv2
import numpy as np
from google.colab.patches import cv2_imshow
import math
import random as r

class Color:
  def __init__(self):
    self.black = (255,255,255)
    self.red = (0,0,255)
    self.green = (0,255,0)
    self.blue = (255,0,0)

color_palette = Color()

HEIGHT = 500
WIDTH = 500

def get_rotated_point(x1, y1, angle, length):
  x2 = x1 + length
  y2 = y1
  radians = math.radians(angle)
  coseno = math.cos(radians)
  seno = math.sin(radians)
  rotated_x = (x2 - x1)*seno + (y2 - y1)*coseno
  rotated_y = (x2 - x1)*coseno - (y2 - y1)*seno
  x2 = rotated_x + x1
  y2 = rotated_y + y1

  return x2, y2


def draw_tree(img, x1, y1, length, angle, scale, angle_change, n, thickness, max_size):
    if n == 0 or max_size <= 0:
      cv2.circle(img, (int(x1),int(y1)), 3, (0,255,0), (-1))
      return
    # Rotation
    x2, y2 = get_rotated_point(x1, y1, angle, length)

    cv2.line(img, (int(x1),int(y1)), (int(x2),int(y2)), (50,93,145), (thickness))

    # With randoms
    branches = 1
    for i in range(branches*-1, branches + 1, 1):
      scale_factor = r.random()
      scale_factor = (scale_factor if scale_factor >= 0.7 else scale_factor + 0.5)
      steps = r.randint(1, max(n - 8, 1))
      thickness = thickness - 2 if thickness - 2 else thickness
      draw_tree(img, x2, y2, length * scale_factor,angle + angle_change * i, scale, angle_change, n - steps, thickness, max(max_size - length * scale_factor, 0))

def draw_sun(img, x1, y1, length, angle, scale, angle_change, n, thickness):
  if n == 0:
      return
  # Rotation
  x2, y2 = get_rotated_point(x1, y1, angle, length)

  cv2.line(img, (int(x1),int(y1)), (int(x2),int(y2)), (60,255,255), (thickness))

  draw_sun(img, x1, y1, length * scale, angle - angle_change, scale, angle_change, n - 1, thickness)

def draw_mountains(img, x1, y1, length, angle, scale, angle_change, n, thickness):
  if n == 0:
      return
  # Rotation
  x2, y2 = get_rotated_point(x1, y1, angle, length)

  cv2.line(img, (int(x1),int(y1)), (int(x2),int(y2)), (161,118,96), (50))    

  draw_mountains(img, x2, y2, length + scale, angle + angle_change, scale, angle_change, n - 1, thickness)



def draw_cloud(img, x1, y1, length, angle, scale, angle_change, n, thickness):
  if n == 0:
      return
  # Rotation
  x2, y2 = get_rotated_point(x1, y1, angle, length)

  cv2.circle(img,(int(x1),int(y1)),int(length),(255,255,255),-1)
  cv2.circle(img,(int(x1),int(y1)),int(length),(230,230,230),1)
  draw_cloud(img,x2,y2,length*scale,angle-angle_change,scale,angle_change,n-1, thickness)
  draw_cloud(img,x2,y2,length*scale,angle-2*angle_change,scale,angle_change,n-1, thickness)
  draw_cloud(img,x2,y2,length*scale,angle-3*angle_change,scale,angle_change,n-1, thickness)
  
img = np.zeros((HEIGHT, WIDTH, 3), dtype="uint8")
# Paint the sky background
cv2.rectangle(img, (0,0), (WIDTH, HEIGHT), (241,224,181), (-1))
# Paint the mountains
draw_mountains(img, -800,1500,900,30,0.1,50,250, 50)
# Paint the ground
cv2.rectangle(img, (0,450), (WIDTH, HEIGHT), (83,118,155), (-1))

# Draw the trees
for i in range(5):
  draw_tree(img, 50 + 100*i, 480, 25, 180, 0.7, 31, 9, 6, 100)

# Draw the sun at a random position in the sky
x = r.randint(0, 500)
y = r.randint(0, 300)
draw_sun(img, x, y, 70, 180, 0.98, 76, 50, 1)

# Draw the clouds at random positions in the sky
for i in range(10):
  x = r.randint(0, 500)
  y = r.randint(0, 300)
  size = r.randint(10,40)
  draw_cloud(img,x,y,size,120,0.8,30,7,1)


cv2_imshow(img)
