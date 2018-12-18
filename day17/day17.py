from collections import namedtuple

import numpy as np
import re

import networkx as nx

x_first_pattern = re.compile("x=([0-9]+), y=([0-9]+)..([0-9]+)")
y_first_pattern = re.compile("y=([0-9]+), x=([0-9]+)..([0-9]+)")

with open('test.txt') as f:
    x_left = 1e10
    x_right = 0
    y_bottom = 0
    data = []
    for line in f:
        x_first = x_first_pattern.match(line)
        if x_first:
            # print('x first: ', x_first[1], x_first[2], x_first[3])
            x = int(x_first[1])
            y_min = int(x_first[2])
            y_max = int(x_first[3])

            if y_max > y_bottom:
                y_bottom = y_max
            if x > x_right:
                x_right = x
            elif x < x_left:
                x_left = x

            data.append(((y_min, y_max), x))

        else:
            y_first = y_first_pattern.match(line)
            # print('y first: ', y_first[1], y_first[2], y_first[3])
            y = int(y_first[1])
            x_min = int(y_first[2])
            x_max = int(y_first[3])

            if y > y_bottom:
                y_bottom = y
            if x_min < x_left:
                x_left = x_min
            if x_max > x_right:
                x_right = x_max

            data.append((y, (x_min, x_max)))


    x_left -= 1 # making the board one larger to left, so we alway have an all sand column
# four possible states:
ground = {0: '.',
          1: '#',
          2: '~' ,
          3: '|' ,# flowing
          4: '|' # spilling over
         }

ground_map = np.zeros((y_bottom+2, x_right-x_left+3), dtype=int)


for entry in data:
    if isinstance(entry[0], tuple):
        y_min, y_max = entry[0]
        x = entry[1]-x_left
        ground_map[y_min:y_max+1,x] = 1

    else:
        y = entry[0]
        x_min = entry[1][0] - x_left
        x_max = entry[1][1] - x_left
        ground_map[y,x_min:x_max+1] = 1

def print_ground():
    for row in ground_map:
        print(''.join([ground[j] for j in row]))

class Level:
    def __init__(self, y, x, width, state, parent=None):

        self.y = y
        self.x = x
        self.width = width
        self.state = state
        self.parent = parent


    def __repr__(self):
        return 'Level({},{},{},{})'.format(self.y, self.x, self.width, self.state)

    def set_to_map(self):
        ground_map[self.y, self.x:self.x+self.width] = self.state

    def get_state(self):
        return ''.join([ground[s] for s in ground_map[self.y, self.x:self.x+self.width]])

    def in_bucket(self):

        # left, right = ground_map[level.y, level.x-1], ground_map[level.y, level.x+level.width]
        for j in range(1,50): # big enough to find the edge of any bucket i saw in the input
            left = ground_map[self.y, self.x-j]
            left_down =  ground_map[self.y+1, self.x-j]
            # print('left? ', j, ground[left], ground[left_down])
            if left!=1 and (left_down!=0): # not a wall, and below it is not sand. just keep going
                continue
            if left!=1 and left_down==0: # fell off the cliff
                return False, 0, 0
            if left==1 and (left_down==1 or left_down==2):
                left_idx = self.x - j + 1
                break

        for j in range(50):
            right = ground_map[self.y, self.x+self.width+j]
            right_down = ground_map[self.y+1, self.x+self.width+j]
            # print('right? ', j, ground[right], ground[right_down])
            if right!=1 and (right_down!=0): # not a wall, and below it is not sand. just keep going
                continue
            if right!=1 and right_down==0: # fell off the cliff
                return False, 0, 0
            if right==1 and (right_down==1 or right_down==2):
                right_idx = self.x+self.width+j-1
                break

        return True, left_idx, right_idx

    def settle(self):
        # print('testing', self)
        in_bucket, left, right = self.in_bucket()
        # print("settling",left, right)
        # print()
        if in_bucket:
            self.x = left
            self.width = right-left+1
            self.state = 2
            self.set_to_map()
            return True
        return False

    def find_cliffs(self):
        for j in range(1,50): # big enough to find the edge of any bucket i saw in the input
            left = ground_map[self.y, self.x-j]
            left_down =  ground_map[self.y+1, self.x-j]
            if left == 1:
                left_idx = False
                break
            if left==0 and left_down==0: # spill
                print('spill left', self, j)
                left_idx = self.x-j
                break

        for k in range(0,50):
            right = ground_map[self.y, self.x+self.width+j]
            right_down = ground_map[self.y+1, self.x+self.width+j]
            if right == 1: # hit a wall
                right_idx = False
                break
            if right==0 and right_down==0: # spill
                print('spill right', self, k)
                right_idx = self.x+self.width+k
                break

        print(j,k)
        self.x -= j-1
        self.width = self.width+j+k

        return left_idx , right_idx

    def spill(self):
        print('pre_cliffs', self)
        left_idx, right_idx = self.find_cliffs()
        print('post_cliffs', self)
        self.state = 3
        # self.set_to_map()
        return left_idx, right_idx


def analyze_level(level):
    new_active_levels = []
    settled = level.settle()
    print('foo', level, settled)
    if settled and level.parent is not None:
        # level.set_to_map()
        new_active_levels.append(current_level.parent)
        print("settled", level)
    elif level.y < y_bottom:
        # should only ever have width 1

        below = ground_map[level.y+1, level.x:level.x+level.width][0]
        level.state = 3
        if below == 0: # flow down
            # print(level)
            level.set_to_map()
            print('flowing down', level)
            new_active_levels.append(Level(level.y+1, level.x, 1, 3, parent=level))
        else: # spill sideways
            left, right = level.spill()
            print('spilling', level, left, right)
            level.set_to_map()
            below = ground_map[level.y+1, level.x:level.x+level.width]
            print('below', below[0], below[-1])
            # if below[0]==0: # left down on left side
            #     new_active_levels.append(Level(level.y+1, level.x, 1, 3, parent=level))
            if below[-1]==0:
                new_active_levels.append(Level(level.y+1, level.x+level.width, 1, 3, parent=level))
    print()
    return new_active_levels

spring = Level(0,500-x_left,1,3,None)

# active levels are ones that still need operating on to determine their final state
active_levels = [spring]

all_levels = set()

# print_ground()
# print("*********************")
i = 0
while active_levels:
    current_level = active_levels.pop(-1)

    active_levels.extend(analyze_level(current_level))

test = Level(10,8,1,3)
# print(test.in_bucket())
# print(test)
print_ground()

# TODO: check if any levels need to be merged