from collections import namedtuple
Sample = namedtuple('Sample', ['before', 'command', 'after'])

with open('input.txt') as f: 
    data = [l.strip() for l in f.readlines()]

samples = []

i = 0
while i < len(data):
    if 'Before' in data[i]: 
        #gah, this is a dirty hack. Use a regex! 
        exec('b='+data[i].split(':')[1])
        c = [int(n) for n in data[i+1].split()]
        exec('a='+data[i+2].split(':')[1])
        samples.append(Sample(b,c,a))
        i += 3
    else: 
        i += 1

def addr(command, regs): 
    regs[command[3]] = regs[command[1]] + regs[command[2]]

def addi(command, regs): 
    regs[command[3]] = regs[command[1]] + command[2]

def mulr(command, regs): 
    regs[command[3]] = regs[command[1]] * regs[command[2]]

def muli(command, regs): 
    regs[command[3]] = regs[command[1]] * command[2]

def banr(command, regs): 
    regs[command[3]] = regs[command[1]] & regs[command[2]]

def bani(command, regs): 
    regs[command[3]] = regs[command[1]] & command[2]

def borr(command, regs): 
    regs[command[3]] = regs[command[1]] | regs[command[2]]

def bori(command, regs): 
    regs[command[3]] = regs[command[1]] | command[2]

def setr(command, regs): 
    regs[command[3]] = regs[command[1]]

def seti(command, regs): 
    regs[command[3]] = command[1]

def gtir(command, regs): 
    regs[command[3]] = int(command[1] > regs[command[2]])

def gtri(command, regs): 
    regs[command[3]] = int(regs[command[1]] > command[2])

def gtrr(command, regs): 
    regs[command[3]] = int(regs[command[1]] > regs[command[2]])

def eqir(command, regs): 
    regs[command[3]] = int(command[1] == regs[command[2]])

def eqri(command, regs): 
    regs[command[3]] = int(regs[command[1]] == command[2])

def eqrr(command, regs): 
    regs[command[3]] = int(regs[command[1]] == regs[command[2]])

commands = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
command_names = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
N_commands = len(commands)

def find_posibles(sample): 
    b = sample.before # copy to we don't change the source data
    c = sample.command
    a = sample.after

    possible = []
    for i,command in enumerate(commands): 
        b_copy = list(b)
        command(c, b_copy)
        if a == b_copy: 
            possible.append((i,c[0])) # need to track the possible command, and the op_code it could be

    # p_names = [command_names[i] for i in possible]

    return possible


print('Part 1')
sample_tests = []
num = 0
for s in samples: 
    p = find_posibles(s)
    if len(p) > 2: 
        num += 1
    sample_tests.append(p)
print(num)
print('Part 2')

op_code_sets = [set() for i in range(N_commands)]
for possibles in sample_tests: 
    for p in possibles: 
        command_idx = p[0]
        op_code = p[1]
        op_code_sets[op_code].add(command_idx)


op_code_map = [None for i in range(N_commands)]

def decode(): 
    for i in range(N_commands): 
        # print(i, op_code_sets[i])
        if op_code_map[i] is not None: 
            continue

        if len(op_code_sets[i]) == 1: 
            op_code_map[i] = op_code_sets[i].pop()
            for s in op_code_sets: 
                try: 
                    s.remove(op_code_map[i])
                except KeyError: 
                    pass
                  
            continue

        for j in range(i, N_commands): 
            diff = op_code_sets[i].difference(op_code_sets[j])
            if len(diff) == 1: 
                op_code_map[i] = diff.pop()
        
                for s in op_code_sets: 
                    try: 
                        s.remove(op_code_map[i])
                    except KeyError: 
                        pass
                break  
        
        
decode()
decode() # needs a second pass through to get the last one

registers = [0,0,0,0]

with open('sample.txt') as f: 
    lines = f.read().split('\n')
program = [[int(s) for s in line.split()] for line in lines]

for line in program: 
    op_idx = op_code_map[line[0]]
    op = commands[op_idx]

    op(line, registers)

print('reg 0: ', registers[0])
    


    







