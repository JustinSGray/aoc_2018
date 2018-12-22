import numpy as np

import networkx as nx

# My Input
DEPTH = 5913
TARGET = (8,701)

# Test Input
# DEPTH = 510
# TARGET = (10,10)



def print_map():
    TYPE_MAP[0,0] = 3
    TYPE_MAP[TARGET] = 4

    char_map = {0:'.', 1:'=', 2:'|', 3:'M', 4:'T'}
    for row in TYPE_MAP:
        print(''.join([char_map[t] for t in row]))

    TYPE_MAP[0,0] = 0
    TYPE_MAP[TARGET] = 0

def geologic_index(pos):

    y,x = pos
    if pos == (0,0) or pos == TARGET:
        return 0
    if y == 0:
        return x*16807
    if x == 0:
        return y*48271

    # its not an edge case
    left = EROSION_MAP[y,x-1]
    up = EROSION_MAP[y-1,x]
    return left*up


print('part 1')
EROSION_MAP = np.empty((TARGET[1]+1,TARGET[0]+1), dtype=int)
TYPE_MAP = np.empty((TARGET[1]+1,TARGET[0]+1), dtype=int)
for i in range(TARGET[1]+1): # y
    for j in range(TARGET[0]+1): # x
        pos = (i,j)

        gi = geologic_index(pos)

        erosion = (gi + DEPTH)%20183
        EROSION_MAP[pos] = erosion
        TYPE_MAP[pos] = erosion % 3

print(np.sum(TYPE_MAP))


print('part 2')

PADDING = 100

EROSION_MAP = np.empty((TARGET[1]+PADDING,TARGET[0]+PADDING), dtype=int)
TYPE_MAP = np.empty((TARGET[1]+PADDING,TARGET[0]+PADDING), dtype=int)
for i in range(TARGET[1]+PADDING): # y
    for j in range(TARGET[0]+PADDING): # x
        pos = (i,j)

        gi = geologic_index(pos)

        erosion = (gi + DEPTH)%20183
        EROSION_MAP[pos] = erosion
        TYPE_MAP[pos] = erosion % 3


rocky, wet, narrow = 0, 1, 2
torch, gear, neither = 0, 1, 2
valid_items = {rocky: (torch, gear), wet: (gear, neither), neither: (torch, neither)}

def dijkstra():
    graph = nx.Graph()
    for y in range(0, corner[1] + 1):
        for x in range(0, corner[0] + 1):
            items = valid_items[TYPE_MAP[y,x]] # valid_items[grid[(x, y)]]

            graph.add_edge((y, x, items[0]), (y, x, items[1]), weight=7)
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x, new_y = x+dx, y+dy
                if 0 <= new_x <= corner[0] and 0 <= new_y <= corner[1]:
                    new_items = valid_items[TYPE_MAP[new_y, new_x]]
                    for item in set(items).intersection(set(new_items)):
                        graph.add_edge((y, x, item), (new_y, new_x, item), weight=1)

    return nx.dijkstra_path_length(graph, (0, 0, torch), (TARGET[1], TARGET[0], torch))


corner = (TARGET[0] + 99, TARGET[1] + 99)
# grid = {c: v[2] for c, v in zip()}
print(dijkstra())




