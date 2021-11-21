import random

class CelullarAutomata2D:
    def __init__(self, dimensions, rules):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]
        self.rules = rules
        self.b = rules[0:2]
        self.s = rules[2:4]
        self.u = rules[4:6]
        self.r = rules[6:8]
        print(self.b, self.s, self.u, self.r)
        self.movements = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]

    def isPositionValid(self, row, col):
        return 0 <= row <= self.height - 1 and 0 <= col <= self.width - 1

    def countNeighbors(self, row, col, state):
        count = 0
        for mov in self.movements:
            if self.isPositionValid(row + mov[0], col + mov[1]):
                if self.grid[row + mov[0]][col + mov[1]] == state:
                    count += 1
        return count

    def update(self):
        nextGrid = [row[:] for row in self.grid]
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 0:
                    if self.b[0] <= self.countNeighbors(row, col, 1) <= self.b[1]:
                        nextGrid[row][col] = 1
                elif self.grid[row][col] == 1:
                    if self.s[0] <= self.countNeighbors(row, col, 1) <= self.s[1]:
                        continue
                    elif self.u[0] <= self.countNeighbors(row, col, 2) <= self.u[1]:
                        nextGrid[row][col] = 2
                else:
                    if self.r[0] <= self.countNeighbors(row, col, 2) <= self.r[1]:
                        continue
                    else:
                        nextGrid[row][col] = 0

        self.grid = nextGrid

class CelullarAutomata1D:
    def __init__(self, dimensions, initialState, rules = [0,0,0,0,0,0,0,0]):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]
        self.grid[0] = initialState
        self.rules = rules[::-1]
        self.neighbor = 1
        self.row = 1
    
    def applyRule(self, row, col):
        rule = 0
        shift = 0
        for i in range(col - 2, col + 2):
            rule += self.grid[row][i] << shift
            shift += 1
        return int(self.rules[rule])


    def update(self):
        if self.row >= self.height:
            return 
        newRow = [0]*self.width
        for i in range(2, self.width - 2):
            newRow[i] = self.applyRule(self.row - 1, i)
        self.grid[self.row] = newRow

        self.row += 1

class CelullarAutomata1DSecondOrder:
    def __init__(self, dimensions, initialState, rules = [0,0,0,0,0,0,0,0]):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]
        self.grid[0] = initialState
        self.rules = rules[::-1]
        self.neighbor = 1
        self.row = 1
    
    def applyRule(self, row, col):
        rule = 0
        shift = 0
        for i in range(col - 2, col + 2):
            rule += self.grid[row][i] << shift
            shift += 1
        return int(self.rules[rule])


    def update(self):
        if self.row >= self.height:
            return

        twoBehind = self.grid[self.row - 2] if self.row >= 2 else [0]*self.width
        newRow = [0]*self.width
        for i in range(1, self.width - 1):
            newRow[i] = self.applyRule(self.row - 1, i)
            newRow[i] = 0 if twoBehind[i] == newRow[i] else 1
        self.grid[self.row] = newRow

        self.row += 1
