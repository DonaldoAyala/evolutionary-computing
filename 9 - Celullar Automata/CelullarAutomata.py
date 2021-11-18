import random

class CelullarAutomata:
    def __init__(self, dimensions, rules):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]


    def update(self):
        change_row = random.randint(0,self.height - 1)
        change_col = random.randint(0,self.width - 1)
        self.grid[change_row][change_col] ^= 1

