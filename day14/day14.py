import numpy as np

from numba import jit

def digits(n): 
    return([int(s) for s in str(n)])

# class Node(): 

#     def __init__(self, score=0): 

#         self.score = score
#         self.next = None

# N0 = Node(3)
# N1 = Node(7)


# N0.next = N1
# N1.next = N0

# last_node = N1


def mix_recipies(elves, score_board): 
    scores = [score_board[e] for e in elves]

    # mix recipes and add the new ones to the end of the scoreboard
    score_board.extend(digits(np.sum(scores)))
    BOARD_SIZE = len(score_board)

    #move the elves
    for i in range(len(elves)): 
        elves[i] = (elves[i]+scores[i]+1)%BOARD_SIZE


def print_score_board(i=0): 

    scores = [str(s) for s in score_board]

    bracket_start = ['(','[']
    bracket_end = [')',']']
    for e, bs, be in zip(elves, bracket_start, bracket_end): 
        scores[e] = '{}{}{}'.format(bs, score_board[e], be)
    print(' '.join(scores))


def part1(N_recipies=939601):

    score_board = [3,7]

    elves = [0,1]


    # go until len(score board) = 2+9+10

    while len(score_board) < N_recipies+11:
        # print_score_board()
        mix_recipies(elves, score_board)

    return score_board[N_recipies:N_recipies+10]    

print('part 1')
final_score = part1(5)
print(''.join([str(s) for s in final_score]))


def part2(goal=939601): 

    goal = digits(goal)

    N_goal = len(goal)

    score_board = [3,7]

    elves = [0,1]

    # make sure score board is long enough
    while len(score_board) < N_goal: 
        mix_recipies(elves, score_board)


    # iterate until you find your goal
    i = len(score_board)
    while (score_board[-N_goal:] != goal):
        # print_score_board()

        prev_len_score_board = len(score_board)
        
        mix_recipies(elves, score_board)
        
        new_len_score_board = len(score_board)
        if i%10000 == 0: 
            print(i, len(score_board))

        N_new = new_len_score_board - prev_len_score_board
        for j in range(N_new): 
            check = score_board[-N_goal-j:-j]
            if check == goal: 
                return len(score_board) - j - N_goal
 
        i += 1


print('part 2')
answer = part2()
print(answer)




