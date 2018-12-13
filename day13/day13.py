import numpy as np

tiles = {
    '-' : 0,
    '|' : 1,
    '/' : 2, 
    '\\': 3, 
    '+' : 4,
    '>' : 5,
    'v' : 6,
    '<' : 7,
    '^' : 8,
    ' ' : -1
}


#   right down left up 
#     5    6     7   8
turn_map = {
    
    2: {
        5: 'left',
        6: 'right',
        7: 'left',
        8: 'right',
    },
    3: {
        5: 'right',
        6: 'left',
        7: 'right',
        8: 'left',
    }
}

directions = {
    # dir     y,x
    5 : (0,1), # right
    6 : (1,0), # down
    7 : (0,-1), # left
    8 : (-1,0), # up
}

class Cart(): 

    def __init__(self): 
        self.loc = np.array([-1,-1])
        self.dir = -1
        self.last_turn = 'right'
        self.dead = False

    def tick(self): 
        # print('foo', self.loc, self.dir)
        dy,dx = directions[self.dir]
        self.loc[0] += dy
        self.loc[1] += dx

        tile = course[self.loc[0], self.loc[1]]
        if tile == -1: 
            raise ValueError("Ya done messed up!")
        # if turn, update our direction
        if tile == 2 or tile == 3: 
            self._turn(turn_map[tile][self.dir])
        elif tile == 4: # intersection
            if self.last_turn == 'right': 
                self.last_turn = self._turn('left')

            elif self.last_turn == 'left': 
                self.last_turn = self._turn('strait')

            elif self.last_turn == 'strait': 
                self.last_turn = self._turn('right')


    def _turn(self, direction): 
        if direction == 'right': 
            self.dir = (self.dir-4)%4 +5 
        elif direction == 'left': 
            self.dir = (self.dir+6)%4 + 5 

        return direction


with open('input.txt') as f:
    data = f.readlines()
    height = len(data)
    width = len(data[0])-1

    course = np.ones((height, width), dtype=int)*-1

    for i,row in enumerate(data):
        course[i] = [tiles[s] for s in row[:-1]]


# find all the carts and make a data structure with their location and direction
carts = []
cart_locs = np.where(course>4)

for (y,x) in zip(cart_locs[0],cart_locs[1]): 
    c = Cart()
    c.loc = np.array([y,x])
    d = c.dir = course[c.loc[0], c.loc[1]]
    carts.append(c)

    # replace their locations with the correct track piece
    # this ignores the possibility that any cart started on a curve or an intersection
    if d in (4,5): 
        course[c.loc[0],c.loc[1]] = 0
    else: 
        course[c.loc[0],c.loc[1]] = 1

N_carts = len(carts)



# print('part 1')
# i = 0 
# green = True
# while green: 
#     # print(i, [c.loc for c in carts])
#     # print(i, [complex(c.loc[1],c.loc[0]) for c in carts])
#     for j,c in enumerate(carts):
#         # print('tick ', j) 
#         c.tick()
#         for j in range(N_carts): 
#             for k in range(j+1, N_carts): 
#                 if np.all(carts[j].loc == carts[k].loc): 
#                     c_loc = carts[j].loc
#                     print(i, 'collision at', c_loc[1], c_loc[0])
#                     green = False
#                     break 
#     i += 1

print()
print('part 2')

i = 0 
green = True
while len(carts) > 1:
    carts.sort(key=lambda c: (c.loc[1], c.loc[0]))
    for ci, cart in enumerate(carts):
        if cart.dead:
            continue
        cart.tick()
        for ci2, cart2 in enumerate(carts):
            if ci != ci2 and (cart.loc[0] == cart2.loc[0]) and (cart.loc[1] == cart2.loc[1]) and not cart2.dead:
                cart.dead = True
                cart2.dead = True
                break
        if cart.dead:
            continue
        part = course[cart.loc]

    carts = [c for c in carts if not c.dead]
    i += 1
print(carts[0].loc[1], ",", carts[0].loc[0])

    




