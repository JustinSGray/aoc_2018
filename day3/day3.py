import numpy as np

with open('input.txt') as f:
    data = f.read().split("\n")

claims = []

max_right = 0
max_bottom = 0

for row in data:

    s0 = row.split("@")
    id = s0[0].strip()
    data = s0[1].strip()

    s1 = data.split(':')
    corner = s1[0].strip().split(',')
    left = int(corner[0]) # 0 based indexing
    top = int(corner[1])

    size = s1[1].strip().split('x')
    width = int(size[0])
    height = int(size[1])

    claims.append((id, left, top, width, height))

    max_bottom = max(max_bottom, top+height)
    max_right = max(max_right, left+width)

print(max_right)
print(max_bottom)

cloth = np.zeros((max_bottom,max_right), dtype=int)

for id, left, top, width, height in claims:
    # print(id, left, top, width, height)
    cloth[top:top+height, left:left+width] += 1

print('part 1')

# print(cloth)

print(np.sum(cloth>1))


print('part2')
for id, left, top, width, height in claims:

    claim_check = cloth[top:top+height, left:left+width]
    if(np.all(claim_check == 1)):
        print(id)


