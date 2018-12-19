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

def get_adjacent(i,j,data):

    idx = ((i-1,j-1),(i-1,j),(i-1,j+1),
           (i,j-1),          (i,j+1),
           (i+1,j-1),(i+1,j),(i+1,j+1),)

    for ni,nj in idx:
        if ni < 0 or nj < 0:
            continue
        try:
            yield(data[ni,nj])
        except IndexError:
            pass

def minute(data):

    new_data = data.copy()

    for i in range(y_max):
        for j in range(x_max):
            current = data[i,j]
            neighbors = get_adjacent(i,j, data)

            if current == 0: # open
                n_trees = 0
                for n in neighbors:
                    if n==1:
                        n_trees += 1
                    if n_trees == 3:
                        new_data[i,j] = 1
                        break

            elif current == 1: # trees
                n_lumber = 0
                for n in neighbors:
                    if n==2:
                        n_lumber+=1
                    if n_lumber == 3:
                        new_data[i,j] = 2
                        break

            elif current == 2: # lumber yard

                new_data[i,j] = 0
                # check_lumber_yard = len([n for n in neighbors if n==2]) >= 1
                # check_trees       = len([n for n in neighbors if n==1]) >= 1

                check_lumber_yard = check_trees = False

                for n in neighbors:
                    if n==2:
                        check_lumber_yard = True
                    if n==1:
                        check_trees = True
                    if check_trees and check_lumber_yard:
                        new_data[i,j] = 2
                        break

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
