# Importing the library
import pygame
import time
import random

class Painter:
    def __init__(self, dimensions, cellSize):
        self.cellSize = cellSize
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.dimensions = dimensions # (width, height)
        pygame.init()
        windowDimensions = (self.dimensions[0]*self.cellSize, self.dimensions[1]*self.cellSize)
        self.screen = pygame.display.set_mode(windowDimensions)
        self.running = True
        self.update = False
    
    def paintGrid(self, grid):
        for row in range(self.dimensions[1]):
            for col in range(self.dimensions[0]):
                rect = (row*self.cellSize, col*self.cellSize, self.cellSize, self.cellSize)
                if grid[col][row] == 0:
                    pygame.draw.rect(self.screen, (255,255,255), rect)
                elif grid[col][row] == 2:
                    pygame.draw.rect(self.screen, (0,0,0), rect)
                else:
                    pygame.draw.rect(self.screen, (90,90,90), rect)
            
        for row in range(self.dimensions[1]):
            pygame.draw.line(self.screen, (0,0,0), (row*self.cellSize,0), (row*self.cellSize, self.width*self.cellSize))
        for col in range(self.dimensions[0]):
            pygame.draw.line(self.screen, (0,0,0), (0, col*self.cellSize), (self.height*self.cellSize, col*self.cellSize))
        
        
    
    def start(self, ca):        
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            mousePosition = pygame.mouse.get_pos()
            pressedLeft = pygame.mouse.get_pressed()[0]
            pressedRight = pygame.mouse.get_pressed()[2]
            if pressedLeft:
                col = int(mousePosition[0]/self.cellSize)
                row = int(mousePosition[1]/self.cellSize)
                ca.grid[row][col] = 1
            if pressedRight:
                col = int(mousePosition[0]/self.cellSize)
                row = int(mousePosition[1]/self.cellSize)
                ca.grid[row][col] = 2
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                ca.grid = [[random.randint(0,2) for j in range(self.width)] for i in range(self.height)]
                for i in range(0,8,2):
                    ca.rules[i] = random.randint(0,8)
                    ca.rules[i + 1] = random.randint(ca.rules[i],8)
                    ca.b = ca.rules[0:2]
                    ca.s = ca.rules[2:4]
                    ca.u = ca.rules[4:6]
                    ca.r = ca.rules[6:8]
                    print(ca.rules)
            if keys[pygame.K_SPACE]:
                self.update = not self.update
            
            if self.update:
                ca.update()
            self.paintGrid(ca.grid)
            pygame.display.flip()
            time.sleep(0.1)
        