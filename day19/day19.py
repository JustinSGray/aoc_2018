
def addr(command, regs):
    regs[command[2]] = regs[command[0]] + regs[command[1]]

def addi(command, regs):
    regs[command[2]] = regs[command[0]] + command[1]

def mulr(command, regs):
    regs[command[2]] = regs[command[0]] * regs[command[1]]

def muli(command, regs):
    regs[command[2]] = regs[command[0]] * command[1]

def banr(command, regs):
    regs[command[2]] = regs[command[0]] & regs[command[1]]

def bani(command, regs):
    regs[command[2]] = regs[command[0]] & command[1]

def borr(command, regs):
    regs[command[2]] = regs[command[0]] | regs[command[1]]

def bori(command, regs):
    regs[command[2]] = regs[command[0]] | command[1]

def setr(command, regs):
    regs[command[2]] = regs[command[0]]

def seti(command, regs):
    regs[command[2]] = command[0]

def gtir(command, regs):
    regs[command[2]] = int(command[0] > regs[command[1]])

def gtri(command, regs):
    regs[command[2]] = int(regs[command[0]] > command[1])

def gtrr(command, regs):
    regs[command[2]] = int(regs[command[0]] > regs[command[1]])

def eqir(command, regs):
    regs[command[2]] = int(command[0] == regs[command[1]])

def eqri(command, regs):
    regs[command[2]] = int(regs[command[0]] == command[1])

def eqrr(command, regs):
    regs[command[2]] = int(regs[command[0]] == regs[command[1]])




with open('input.txt') as f:
    bound_reg = int(f.readline().split()[1])

    global_stuff = globals()

    commands = []
    data = []
    for line in f:
        com = line.split()
        op = global_stuff[com[0]]
        commands.append((op, (int(com[1]), int(com[2]), int(com[3]))))
        data.append(line.strip())

def run_program(registers):
    ip = 0
    while True:

        try:
            op, com = commands[ip]
            registers[bound_reg] = ip
            print('ip={} {} {}'.format(ip, registers, data[ip]))
            op(com, registers)
            # print('      {}'.format(registers))
            ip = registers[bound_reg]
            ip += 1
            if ip == 1:
                print([x for x in range(1, registers[4]+1) if registers[4] % x == 0])
                return sum([x for x in range(1, registers[4]+1) if registers[4] % x == 0])
        except IndexError:
            break
    return registers[0]



print('bound_reg ', bound_reg)


# print('part 1: ', run_program([0,0,0,0,0,0]))
print('part 2: ', run_program([1,0,0,0,0,0]))



