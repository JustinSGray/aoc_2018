import numpy as np

INIT_F = 0


data = open('input.txt').read().split()

data = [int(s) for s in data]

print("part 1")
final_freq = np.sum(data)
print(final_freq)



print('part 2')

n_data = len(data)

i = 0
last = 0
seen = set()

print(data)
while True:
    # print('f', i, data[i])

    if last in seen:
        print('first repeat', last)
        break

    seen.add(last)

    last += data[i]

    i += 1
    i = i%n_data








