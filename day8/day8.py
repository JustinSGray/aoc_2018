import string

import numpy as np

import networkx as nx

with open('input.txt') as f:
    data = [int(n) for n in f.read().split()]


class Node(object):

    def __init__(self, n_children, metadata=None):

        self.metadata = metadata
        self.n_children = n_children
        self.children = []
        self.value = 0



def pop_spec(data):

    n_children = data.pop(0)
    n_meta = data.pop(0)

    return n_children, n_meta, data

# get the spec
# make a node
#recurse down the data
# after recursion pull in the metadata

G = nx.DiGraph()

# letters = string.ascii_uppercase

def parse_data(data):
    n_children, n_meta, data = pop_spec(data)
    node = Node(n_children=n_children)

    if n_children == 0:
        node.metadata = [data.pop(0) for i in range(n_meta)]

        node.value = sum(node.metadata)

    else:
        for i in range(n_children):
            data, child_node = parse_data(data)
            node.children.append(child_node)
            G.add_edge(node, child_node)

        node.metadata = [data.pop(0)-1 for i in range(n_meta)]

        for idx in node.metadata:
            if idx < n_children:
                node.value += node.children[idx].value
    G.add_node(node)

    return data, node

print('part 1')
parse_data(data)

meta_total = 0
for node in G.nodes():
    meta_total += sum(node.metadata)
print(meta_total)


print('part 2')

# find root
for node in G:
    if G.in_degree(node) == 0:
        break
print(node.value)



