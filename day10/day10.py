
import numpy as np

from re import findall

data = []
with open('input.txt') as f:
    for line in f.readlines():
        # x, y, vx, vy
        data.append(list(map(int,findall(r'-?\d+', line))))

data = np.array(data)

msg_area = 1e100
bbox = [0,0]

msg_time = 0
for sec in range(20000):

    X = data[:,0] + sec*data[:,2]
    Y = data[:,1] + sec*data[:,3]
    max_x = np.max(X)
    min_x = np.min(X)
    delta_x = abs(max_x-min_x)

    max_y = np.max(Y)
    min_y = np.min(Y)
    delta_y = abs(max_y-min_y)

    if (delta_x*delta_y) < msg_area:
        msg_time = sec
        bbox = (delta_y+1, delta_x+1)
        msg_area = delta_x*delta_y

grid = np.chararray(bbox, unicode=True)
grid[:] = '-'

X = data[:,0] + msg_time*data[:,2]
Y = data[:,1] + msg_time*data[:,3]
X = X - np.min(X)
Y = Y - np.min(Y)
grid[(Y,X)] = '#'

print('time: ', msg_time)
for row in grid:
    print(''.join(row))
