import time

import numpy as np

from numba import jit

SIZE = 300

ar = np.arange(SIZE)+1
Y,X = np.meshgrid(ar, ar)


SERIAL_NUMBER = 5177

rack_id = X + 10
starting_power = rack_id * Y
step3 = starting_power + SERIAL_NUMBER
step4 = step3*rack_id
step5 = np.floor(step4/100)%10
power = step5 - 5


def find_powers(span=3):
    powers = np.zeros((SIZE-span+1,SIZE-span+1), dtype='int')

    for i in np.arange(SIZE-span, dtype='int'):
        for j in np.arange(SIZE-span, dtype='int'):
            powers[i,j] = np.sum(power[i:i+span,j:j+span])

    # print(powers.shape)
    idx_max = np.argmax(powers)
    max_power = powers.flatten()[idx_max]
    max_x, max_y = np.unravel_index(idx_max, (SIZE,SIZE))
    return max_power, (max_x+1, max_y+1), powers


def find_next_powers(prev_powers, span):
    '''find the powers for a span 1 larger than the given powers'''

    next_powers = np.zeros((SIZE-span+1,SIZE-span+1), dtype='int')


    for i in np.arange(SIZE-span, dtype='int'):
        for j in np.arange(SIZE-span, dtype='int'):
            next_powers[i,j] = powers[i,j] + np.sum(power[i:i+span,j+span-1]) + np.sum(power[i+span-1,j:j+span-1])

    idx_max = np.argmax(next_powers)
    max_power = next_powers.flatten()[idx_max]
    max_x, max_y = np.unravel_index(idx_max, (SIZE,SIZE))

    return max_power, (max_x+1, max_y+1), next_powers



print('part 1')
mp, mp_loc, powers = find_powers(3)
print(mp_loc)

print('part 2')

largest = 0
largest_loc = (0,0)
largest_span = 0

st = time.time()

mp, mp_loc, powers = find_powers(1)

for i in range(2,21):

    mp, mp_loc, powers = find_next_powers(powers, i)
    if mp > largest:
        largest = mp
        largest_loc = mp_loc
        largest_span = i

    print(i, mp, mp_loc)

print('largest!!')
print(largest_loc, largest_span)
print('time ', time.time()-st)



