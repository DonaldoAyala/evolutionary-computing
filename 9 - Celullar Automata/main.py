from Painter import Painter
from CelullarAutomata import CelullarAutomata

dimensions = (50,50)
cellSize = 10

ca = CelullarAutomata(dimensions, (1,2,3,4,5,6))
painter = Painter(dimensions, cellSize)

painter.start(ca)
