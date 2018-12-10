from re import findall
import numpy as np
import matplotlib.pylab as plt


data = []
with open('input.txt') as f:
    for line in f.readlines():
        # x, y, vx, vy
        data.append(list(map(int,findall(r'-?\d+', line))))

data = np.array(data)

msg_area = 1e100
bbox = [0,0]

msg_time = 0

areas = []
for sec in range(20000):

    X = data[:,0] + sec*data[:,2]
    Y = data[:,1] + sec*data[:,3]
    max_x = np.max(X)
    min_x = np.min(X)
    delta_x = abs(max_x-min_x)

    max_y = np.max(Y)
    min_y = np.min(Y)
    delta_y = abs(max_y-min_y)

    curr_area = delta_x*delta_y
    if curr_area < msg_area:
        msg_time = sec
        bbox = (delta_y+1, delta_x+1)
        msg_area = curr_area

    # based on a plot of the areas, you can stop when it starts increasing again
    else:
        break

    areas.append(curr_area)


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


fig, ax = plt.subplots()
ax.plot(areas)
# fig.savefig('day10_area_variation.png')
plt.show()
