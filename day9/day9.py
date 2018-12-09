
from collections import deque
import time

# my input
# 435 players; last marble is worth 71184 points

def play(N_PLAYERS, LAST_MARBLE):
    # N_PLAYERS = 435
    # LAST_MARBLE = 71184

    circle = deque([0])

    player = 0

    scores = [0,]*N_PLAYERS

    marble_counter = 1

    while marble_counter <= LAST_MARBLE:
        player = (player+1)%(N_PLAYERS)

        if marble_counter % 23 == 0: # multiple of 23
            circle.rotate(7)
            bonus = circle.pop()
            circle.rotate(-1)

            scores[player] += marble_counter + bonus

            # print('special rule', marble_counter, bonus)
        else:
            circle.rotate(-1)
            circle.append(marble_counter)

        marble_counter+=1

    return max(scores)


print('part 1')
winner = play(435, 71184)
print(winner)

print('part 2')
winner = play(435, 71184*100)
print(winner)






