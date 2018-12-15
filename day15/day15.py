import time

from collections import deque

import numpy as np

class Unit:
    def __init__(self, unit_type, x, y, d):
        self.unit_type = unit_type
        self.x = x
        self.y = y
        self.is_alive = True
        self.hp = 200
        self.attack_damage = d

    def pos(self):
        return self.x, self.y

    def get_attacked(self, damage):
        if self.is_alive:
            self.hp -= damage
            if self.hp <= 0:
                self.is_alive = False

def reading_order(pos):
    return pos[1], pos[0]

class Board: 

    def __init__(self, data):
        self.data = data

        self.max_y = len(data)
        self.max_x = len(data[0])

    # finds nodes in targets that have the same shortest path distance from start
    # without visiting a node in excluded_nodes

    def find_closest(self, excluded_nodes, start, targets):
        data = self.data
        if data[start[1]][start[0]] == '#':
            return [], None

        seen = set()
        q = deque([(start, 0)])
        found_dist = None
        closest = []
        while q:
            cell, dist = q.popleft()
            if found_dist is not None and dist > found_dist:
                return closest, found_dist
            if cell in seen or cell in excluded_nodes:
                continue
            seen.add(cell)
            if cell in targets:
                found_dist = dist
                closest.append(cell)
            for n in self.neighbors(*cell):
                if n not in seen:
                    q.append((n, dist + 1))
        return closest, found_dist


    def neighbors(self, x, y):

        neighbors = []
      
        if x > 0 and data[y][x-1] != '#': 
            neighbors.append((x-1,y))

        if x < (self.max_x-1) and data[y][x+1] != '#': 
            neighbors.append((x+1,y))

        if y > 0 and data[y-1][x] != '#': 
            neighbors.append((x,y-1))

        if y < (self.max_y-1) and data[y+1][x] != '#': 
            neighbors.append((x,y+1))


        return neighbors



    def solve(self, e_damage, no_elves_die):
        data = self.data
        # extract characters/units from the grid and replace with dots
        units = []
        for y in range(len(data)):
            for x in range(len(data[0])):
                t = data[y][x]
                if t in "GE":
                    units.append(Unit(t, x, y, 3 if t == "G" else e_damage))
                    # data[y][x] = "."


        round = 0
        while True:
            order = sorted(units, key=lambda c: reading_order(c.pos()))

            for idx, c in enumerate(order):
                if not c.is_alive:
                    continue

                # get all opposing units and their positions
                enemies = [e for e in units if e.unit_type != c.unit_type and e.is_alive]
                enemy_positions = [e.pos() for e in enemies]

                # get all cells immediately next to the current unit
                nearby_cells = self.neighbors(*c.pos())

                # get enemies in range
                enemy_positions_in_range = [p for p in nearby_cells if p in enemy_positions]

                # if no enemies in range, take a step towards
                if not enemy_positions_in_range:
                    # get all open positions in grid next to an enemy
                    surrounding = []
                    for e in enemies:
                        surrounding.extend(self.neighbors(*e.pos()))
                    surrounding = [s for s in surrounding]

                    # get all units positions except for the current one
                    excluded_nodes = [e.pos() for e in units if e.is_alive and e != c]
                    closest_targets, dist = self.find_closest(excluded_nodes, c.pos(), surrounding)

                    if closest_targets:
                        # choose the closest by reading order
                        choice = min(closest_targets, key=reading_order)

                        # find next cell which has a shortest path of the same distance
                        for s in sorted(nearby_cells, key=reading_order):
                            _, d = self.find_closest(excluded_nodes, s, [choice])
                            if d == dist - 1:
                                c.x, c.y = s
                                break

                    # update enemies in range if it has changed
                    enemy_positions_in_range = [p for p in self.neighbors(*c.pos()) if p in enemy_positions]

                if enemy_positions_in_range:
                    # get the enemy objects at those positions
                    enemies = [e for e in enemies if e.pos() in enemy_positions_in_range]

                    # find the lowest health and attack
                    lowest_health = min(enemies, key=lambda e: (e.hp, reading_order(e.pos())))
                    lowest_health.get_attacked(c.attack_damage)

                    # if part 2, return early if an elf dies
                    if no_elves_die and lowest_health.unit_type == "E" and not lowest_health.is_alive:
                        return False, 0

                    # check to see if there is only one unit type left
                    alive = set(e.unit_type for e in units if e.is_alive)
                    if len(alive) == 1:
                        # handle edge case when last enemy dies at end of turn
                        if idx == len(order) - 1:
                            round += 1
                        return True, round * sum(e.hp for e in units if e.is_alive)
            round += 1


st = time.time()

with open("input.txt") as f:
    input_data = f.read()
data = [list(line) for line in input_data.split("\n")]

b = Board(data)
_, score = b.solve(3, False)
print("Part 1", score)


i = 4
while True:
    no_elves_died, score = b.solve(i, True)
    if no_elves_died:
        print("Part 2", score)
        break
    i += 1

print('time ', time.time()-st)