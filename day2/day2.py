import numpy as np

with open('input.txt') as f:
    data = f.read().split()

def counter(string):

    data = {}
    for s in string:
        if s not in data:
            data[s] = 1
        else:
            data[s] += 1

    has_two = 0
    has_three = 0

    for letter,count in data.items():
        if count == 2:
            has_two = 1
        elif count == 3:
            has_three = 1

    # print(string, has_two, has_three)
    return has_two, has_three


print('part 1')
has_two = 0
has_three = 0

for line in data:
    two, three = counter(line)

    has_two += two
    has_three += three

print(has_two, has_three, has_two*has_three)


print('part 2')
with open('input2.txt') as f:
    data = f.read().split()


num_data = []
for row in data:
    num_data.append(np.array([ord(s) for s in row]))

n_data = len(data)
for i in range(n_data):
    lhs = num_data[i]
    for j in range(i+1, n_data):
        diff = lhs - num_data[j]
        total = np.sum(np.array(diff, dtype=bool))
        # print('diff', i,j, total)

        if total == 1:
            idx = np.where(diff==0)[0]
            common = []
            for k in idx:
                common.append(data[i][k])
            print(''.join(common))
            exit()




