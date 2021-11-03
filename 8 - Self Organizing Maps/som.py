# som.py
# Definition of the class to build a self organizing map
# Ayala Segoviano Donaldo Horacio

from random import *
from math import *


class Node:

    def __init__(self, FV_size=10, PV_size=10, Y=0, X=0):
        self.FV_size = FV_size
        self.PV_size = PV_size
        self.FV = [0.0]*FV_size  # Feature Vector
        self.PV = [0.0]*PV_size  # Prediction Vector
        self.X = X  # X location
        self.Y = Y  # Y location

        for i in range(FV_size):
            self.FV[i] = random()  # Assign a random number from 0 to 1

        for i in range(PV_size):
            self.PV[i] = random()  # Assign a random number from 0 to 1


class SOM:

    #Let radius=False if you want to autocalculate the radis
    def __init__(self, height=10, width=10, FV_size=10, PV_size=10, radius=False, learning_rate=0.005):
        self.height = height
        self.width = width
        self.radius = radius if radius else (height+width)/2
        self.total = height*width
        self.learning_rate = learning_rate
        self.nodes = [0]*(self.total)
        self.FV_size = FV_size
        self.PV_size = PV_size
        for i in range(self.height):
            for j in range(self.width):
                self.nodes[(i)*(self.width)+j] = Node(FV_size, PV_size, i, j)

    # Train_vector format: [ [FV[0], PV[0]],
    #                        [FV[1], PV[1]], so on..

    def train(self, iterations=1000, train_vector=[[[0.0], [0.0]]]):
        
        time_constant = iterations/log(self.radius)
        radius_decaying = 0.0
        learning_rate_decaying = 0.0
        influence = 0.0
        stack = []  # Stack for storing best matching unit's index and updated FV and PV
        temp_FV = [0.0]*self.FV_size
        temp_PV = [0.0]*self.PV_size
        for i in range(1, iterations+1):
            #print "Iteration number:",i
            radius_decaying = self.radius*exp(-1.0*i/time_constant)
            learning_rate_decaying = self.learning_rate * \
                exp(-1.0*i/time_constant)
            
            
            for j in range(len(train_vector)):
                input_FV = train_vector[j][0]
                input_PV = train_vector[j][1]
                best = self.best_match(input_FV)
                stack = []
                for k in range(self.total):
                    dist = self.distance(self.nodes[best], self.nodes[k])
                    if dist < radius_decaying:
                        temp_FV = [0.0]*self.FV_size
                        temp_PV = [0.0]*self.PV_size
                        influence = exp((-1.0*(dist**2))/(2*radius_decaying*i))

                        for l in range(self.FV_size):
                            #Learning
                            temp_FV[l] = self.nodes[k].FV[l]+influence * \
                                learning_rate_decaying * \
                                (input_FV[l]-self.nodes[k].FV[l])

                        for l in range(self.PV_size):
                            #Learning
                            temp_PV[l] = self.nodes[k].PV[l]+influence * \
                                learning_rate_decaying * \
                                (input_PV[l]-self.nodes[k].PV[l])

                        #Push the unit onto stack to update in next interval
                        stack[0:0] = [[[k], temp_FV, temp_PV]]

                for l in range(len(stack)):

                    self.nodes[stack[l][0][0]].FV[:] = stack[l][1][:]
                    self.nodes[stack[l][0][0]].PV[:] = stack[l][2][:]

    #Returns prediction vector
    def predict(self, FV=[0.0], get_ij=False):
        best = self.best_match(FV)
        if get_ij:
          return self.nodes[best].PV, self.nodes[best].X, self.nodes[best].Y
        return self.nodes[best].PV

    #Returns best matching unit's index
    def best_match(self, target_FV=[0.0]):

        minimum = sqrt(self.FV_size)  # Minimum distance
        minimum_index = 1  # Minimum distance unit
        temp = 0.0
        for i in range(self.total):
            temp = 0.0
            temp = self.FV_distance(self.nodes[i].FV, target_FV)
            if temp < minimum:
                minimum = temp
                minimum_index = i

        return minimum_index

    def FV_distance(self, FV_1=[0.0], FV_2=[0.0]):
        temp = 0.0
        for j in range(self.FV_size):
            temp = temp+(FV_1[j]-FV_2[j])**2

        temp = sqrt(temp)
        return temp

    def distance(self, node1, node2):
        return sqrt((node1.X-node2.X)**2+(node1.Y-node2.Y)**2)


# Training the SOM
# (height=10, width=10, FV_size=10, PV_size=10, radius=False, learning_rate=0.005):
height, width = 20,20
country_dev_som = SOM(height, width, 12, 1, False, 0.5)

# Now you have the countries and variables to use
data = []
training_set = []
testing_set = []
country_id = {}
country_tag = {0:"--"}
id = 1

with open('out.txt', 'r') as file:
    for line in file:
        fields = line.split(',')
        if len(fields) < 10:
            continue
        for i in range(2,len(fields)):
            fields[i] = float(fields[i])
        country_id[fields[1]] = id
        country_tag[id] = fields[1]
        id = id + 1
        data.append([fields[2:], [country_id[fields[1]]]])

# Get the max per vector
max_per_vector = [0]*12
for vector in data:
    for i in range(len(vector[0])):
        if max_per_vector[i] < vector[0][i]:
            max_per_vector[i] = vector[0][i]

# Divide each field by the maximum
for vector in data:
    for i in range(len(vector[0])):
        vector[0][i] /= max_per_vector[i]

training_set = data[0:45]
testing_set = data[45:]

country_dev_som.train(300, training_set)

#for row in range(height):
#    for col in range(width):
#        print(country_tag[round(country_dev_som.nodes[row*height + col].PV[0])], end = "\t")
#        #print(round(country_dev_som.nodes[row*height + col].PV[0], 2), end = "\t")
#    print()

bmu_som = [[[] for i in range(width)] for i in range(height)]

for country in data:
    country_bmu, x, y = country_dev_som.predict(country[0], True)
    bmu_som[y][x].append(country_tag[country[1][0]])

max_elements = 0

for arr in bmu_som:
    for c in arr:
        max_elements = max(max_elements, len(c) + 2)

print(max_elements)

for arr in bmu_som:
    for c in arr:
        for s in c:
            print(s,end = ",")
        print(end = "\t"*(max_elements - len(c)))
    print()

    