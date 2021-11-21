from Painter import Painter
from CellularAutomata import CelullarAutomata2D, CelullarAutomata1D, CelullarAutomata1DSecondOrder
import random

dimensions = (250,250)
cellSize = 2
rules = [0]*8

initialState = [0]*dimensions[0]
initialState[int(dimensions[0]/2)] = 1
initialState = [(1 if random.random() < 0.01 else 0) for i in range(dimensions[0])]
print(initialState)
#initialState[int(dimensions[0]/2) + 1] = 1
#rules = [0,1,1,1,1,0,1,0]

rules = [int(x) for x in list('{0:0b}'.format(2019630414))]
rules.insert(0,0)
print(rules)
print(len(rules))

#ca = CelullarAutomata2D(dimensions, rules)
#ca = CelullarAutomata1D(dimensions, initialState, rules)
#ca = CelullarAutomata1DSecondOrder(dimensions, initialState, rules)

#(2,5,1,2,  0,1,4,8)) Spreading fungus


painter = Painter(dimensions, cellSize)

painter.start(ca)
