import string

from numba import jit, int64

alphabet = string.ascii_lowercase


with open('input.txt') as f:
    data = [ord(letter) for letter in f.read()]


@jit
def react(data, remove=None):
    i = 1
    N_P = len(data)

    ord_remove_lower = 0
    ord_remove_upper = 0

    if remove is not None:
        ord_remove_lower = ord(remove.lower())
        ord_remove_upper = ord(remove.upper())

    while i<N_P-1:

        pm1 = data[i-1]
        p = data[i]
        pp1 = data[i+1]

        if remove is not None and (p == ord_remove_upper or p == ord_remove_lower):
            data.pop(i)
            N_P -= 1
            if i > 0:
                i -= 1
            continue

        sub = pm1 - p
        if sub == -32 or sub == 32:
            data.pop(i-1)
            data.pop(1)
            N_P -= 2
            if i > 0:
                i -= 1
            continue

        sub = p - pp1
        if sub == -32 or sub == 32:
            data.pop(i+1)
            data.pop(i)
            N_P -= 2
            if i > 0:
                i -= 1
            continue

        i += 1

    return N_P


print('part 1')
size = react(data)
print(size)

import time
print('part 2')


st = time.time()
smallest_letter = None
smallest_len = 1e100

for letter in alphabet:
    # ord_code = ord(letter)
    size = react(list(data), letter)

    # print(letter, size)

    if size < smallest_len:
        smallest_letter = letter
        smallest_len = size


print('smallest: {}, {}'.format(smallest_letter, smallest_len))
print('time ', time.time()-st)


