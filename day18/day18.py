import numpy as np


inp_map = {'.':0, '|':1, '#':2}
data_map = {0:'.', 1:'|', 2:'#'}

with open('input.txt') as f:

    inp = f.read().split("\n")

    data = []
    for line in inp:
        data.append([inp_map[s] for s in line])

data = np.array(data, dtype=int)

y_max, x_max = data.shape

def print_data(data):
    for row in data:
        print(''.join([data_map[num] for num in row]))

def get_adjacent(i,j, data):
              # y, x
    indices = [[],[]]

    # not on an edge
    if i > 0 and i < y_max-1 and j>0 and j<x_max-1:
        # print('test?')
        idx =  [(i-1,j-1),(i-1,j),(i-1,j+1),
                 (i,j-1),          (i,j+1),
                (i+1,j-1),(i+1,j),(i+1,j+1),]
    elif i == 0: # top edge:
        if j == 0: # left corner
            idx = [          (i,j+1),
                   (i+1,j), (i+1,j+1)]
        elif j<x_max-1: # middle
            idx = [(i,j-1),            (i,j+1),
                   (i+1,j-1), (i+1,j), (i+1,j+1)]
        else: # right corner
            idx = [(i,j-1),
                   (i+1,j-1), (i+1,j)]
    elif i<y_max-1: # middle
        if j == 0: # left side
            idx = [(i-1,j),(i-1,j+1),
                           (i,j+1),
                   (i+1,j),(i+1,j+1)]
        else: #right side
            idx = [(i-1,j-1),(i-1,j),
                   (i,j-1),
                   (i+1,j-1),(i+1,j)]
    else: # bottom edge
        if j == 0: # left corner
            idx = [ (i-1,j), (i-1,j+1),
                              (i,j+1)]
        elif j<x_max-1: # middle
            idx = [(i-1,j-1), (i-1,j), (i-1,j+1),
                   (i,j-1),            (i,j+1)]
        else: # right corner
            idx = [(i-1,j-1), (i-1,j),
                   (i,j-1)]

    neighbors = []
    # print(idx)
    for loc in idx:
        neighbors.append(data[loc])
    # print(neighbors)
    return neighbors

def minute(data):

    new_data = data.copy()

    for i in range(y_max):
        for j in range(x_max):
            current = data[i,j]
            neighbors = get_adjacent(i,j, data)

            if current == 0: # open
                if len([n for n in neighbors if n==1]) >= 3:
                    new_data[i,j] = 1

            elif current == 1: # trees
                if len([n for n in neighbors if n==2]) >= 3:
                        new_data[i,j] = 2

            elif current == 2: # lumber yard

                new_data[i,j] = 0
                check_lumber_yard = len([n for n in neighbors if n==2]) >= 1
                check_trees       = len([n for n in neighbors if n==1]) >= 1

                if check_lumber_yard and check_trees:
                    new_data[i,j] = 2

    return new_data




for i in range(600):
    data = minute(data)
    n_wooded = len(np.where(data==1)[0])
    n_lumber = len(np.where(data==2)[0])
    if i == 9:
        print('part 1')
        print(n_wooded*n_lumber)
        print()

# sequence repeats after a while with a period of 28
final_time = (1000000000 - 600)%28
for i in range(final_time):
    data = minute(data)

print('part 2')
n_wooded = len(np.where(data==1)[0])
n_lumber = len(np.where(data==2)[0])
print(n_wooded*n_lumber)
print()


# print_data(data)
