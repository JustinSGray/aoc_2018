import numpy as np

def parse_line(line):
    s0 = line.split(']')
    date,time = s0[0][1:].split()

    s1 = date.split('-')
    month = int(s1[1])
    day = int(s1[2])
    minute = int(time.split(':')[1])

    return month, day, minute

# first re-sort the data
with open('input.txt') as f:
    data = f.readlines()

data.sort(key=parse_line)

schedule =[]
day_map = {}

guards = set()

i = 0

for row in data:

    month,day,time = parse_line(row)


    action_str = row.split(']')[1].strip()
    if "Guard" in action_str: # id the guard
        s1 = action_str.split()
        id = s1[1][1:]
        schedule.append((month, day, id, np.zeros(60, dtype=bool)))

        day_map[(month,day)] = i
        i += 1

        guards.add(id)

    if "falls" in action_str:
        schedule[-1][3][time:] = True
    elif "wakes" in action_str:
        schedule[-1][3][time:] = False

print('part 1')

guards = {}
time_cards = {}
sleepiest = -1
most_asleep = -1

for month, day, id, asleep in schedule:
    guards.setdefault(id, 0)
    time_cards.setdefault(id, [])

    time_cards[id].append((month, day))

    guards[id] += np.sum(asleep)


    if guards[id] > most_asleep:
        sleepiest = id
        most_asleep = guards[id]

print('sleepiest', sleepiest)


new_data = []
for month,day in time_cards[sleepiest]:
    idx = day_map[(month,day)]
    new_data.append(schedule[idx][3])

new_data = np.array(new_data, dtype=bool)
day_counts = np.sum(new_data,axis=0)
worst_minute = np.argmax(day_counts)
print('worst minute', worst_minute)

print('answer', int(sleepiest)*worst_minute)
print()

print('part 2')

def get_guard_data(id):
    new_data = []
    for month,day in time_cards[id]:
        idx = day_map[(month,day)]
        new_data.append(schedule[idx][3])

    new_data = np.array(new_data, dtype=int)
    return new_data

max_sleep = -1
max_minute = -1
max_sleeper = -1

for guard in guards:
    g_data = get_guard_data(guard)
    sleep = np.sum(g_data,axis=0)
    this_max = np.max(sleep)
    if this_max > max_sleep:
        max_sleep = this_max
        max_minute = np.argmax(sleep)
        max_sleeper = int(guard)

print(max_sleep, max_minute, max_sleeper)
print(max_sleeper*max_minute)



