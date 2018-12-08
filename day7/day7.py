import re
import networkx as nx
import numpy as np

pattern = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')

data = []
with open('input.txt') as f:
    for line in f:
        m = pattern.match(line)
        parent = m.group(1)
        child = m.group(2)
        data.append((parent,child))

# graph making problem

print("part 1")

G = nx.DiGraph()
G.add_edges_from(data)
steps = list(nx.lexicographical_topological_sort(G))
print('order:', "".join(steps))

print('part 2')

task_times = []
tasks = []
time = 0
while task_times or G:
    available = []
    for node in G:
        if G.in_degree(node) == 0 and node not in tasks:
            available.append(node)

    if available and len(task_times) < 5:
        task = min(available)  # min gets smallest task alphabetically
        task_times.append(ord(task) - 4)
        tasks.append(task)
    else:
        # just advance time to the next one to complete
        min_time = min(task_times)
        completed = [] # there could be more than one that completes at the same time
        for i, v in enumerate(task_times):
            if v == min_time:
                completed.append(tasks[i])

        # now just decrement any remaining tasks and remove any completed ones
        task_times = [v - min_time for v in task_times if v > min_time]
        tasks = [t for t in tasks if t not in completed]
        G.remove_nodes_from(completed)

        time += min_time

print(time)










