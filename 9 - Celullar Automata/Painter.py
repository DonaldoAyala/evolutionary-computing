# Importing the library
import pygame
import time

class Painter:
    def __init__(self, dimensions, cellSize):
        self.cellSize = cellSize
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.dimensions = dimensions # (width, height)
        pygame.init()
        windowDimensions = (self.dimensions[0]*self.cellSize, self.dimensions[1]*self.cellSize)
        print(windowDimensions)
        self.screen = pygame.display.set_mode(windowDimensions)
        self.running = True
    
    def paintGrid(self, grid):
        for row in range(self.dimensions[1]):
            for col in range(self.dimensions[0]):
                rect = (row*self.cellSize, col*self.cellSize, self.cellSize, self.cellSize)
                if grid[row][col] == 1:
                    pygame.draw.rect(self.screen, (0,0,0), rect)
                else:
                    pygame.draw.rect(self.screen, (255,255,255), rect)
        
        for row in range(self.dimensions[1]):
            pygame.draw.line(self.screen, (0,0,0), (0,row*self.cellSize), (self.width*self.cellSize,row*self.cellSize))
        
        for col in range(self.dimensions[0]):
            pygame.draw.line(self.screen, (0,0,0), (col*self.cellSize, 0), (col*self.cellSize,self.height*self.cellSize))
    
    def start(self, ca):
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            ca.update()
            self.screen.fill((255, 255, 255))
            self.paintGrid(ca.grid)
            pygame.display.flip()
            time.sleep(0.5)
        