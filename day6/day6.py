import numpy as np

data = np.loadtxt('input.txt', delimiter=',', dtype=int)

max_x = np.max(data[:,0])+1
max_y = np.max(data[:,1])+1





y_position = np.tile(np.arange(max_x), max_y).reshape((max_y,max_x))

x_position = np.tile(np.arange(max_y), max_x).reshape((max_x, max_y)).T

x_dist = np.zeros((max_y, max_x), dtype=int)
y_dist = np.zeros((max_y, max_x), dtype=int)

all_dist = np.ones((max_y, max_x), dtype=int)*1e10
grid = np.zeros((max_y, max_x), dtype=int)

for i,(y,x) in enumerate(data):
    x_dist = np.abs(x_position-x)
    y_dist = np.abs(y_position-y)

    m_dist = x_dist + y_dist

    blank = np.where(m_dist == all_dist)

    island = np.where(m_dist < all_dist)


    all_dist[island] = m_dist[island]
    grid[island] = i+1
    grid[blank] = 0

print('part 1')

non_infinite = []
areas = []

print(max_x, max_y)

print(grid)

for i in range(len(data)):
    id = i+1
    locs = np.where(grid==id)
    # locs 0 is y, locs 1 is x
    if np.any(np.logical_or(locs[0] == 0, locs[0]==max_y-1)):
        continue
    if np.any(np.logical_or(locs[1] == 0, locs[1]==max_x-1)):
        continue

    non_infinite.append(i+1)
    areas.append(len(locs[0]))

    # print('id', id)
    # print('size', len(locs[0]))

largest = np.argmax(areas)
print('id', non_infinite[largest])
print('area', areas[largest])


print('part 2')


all_dist = np.zeros((max_y, max_x), dtype=int)
grid = np.zeros((max_y, max_x), dtype=int)

for i,(y,x) in enumerate(data):
    x_dist = np.abs(x_position-x)
    y_dist = np.abs(y_position-y)

    m_dist = x_dist + y_dist

    all_dist += m_dist

safe = np.where(all_dist<10000)

print(len(safe[0]))
