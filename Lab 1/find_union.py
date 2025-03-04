from Lab3.tester import *

class Node:
    def __init__(self, id_):
        self.id = id_
        self.parent = self
        self.rank = 0 

def find(x):
    if x != x.parent:
        x.parent = find(x.parent)
    return x.parent


def union(x, y):
    x = find(x)
    y = find(y)
    if x == y: return
    if x.rank < y.rank:
        x.parent = y
    else:
        y.parent = x
        if x.rank == y.rank: x.rank += 1
            
            
def make_set(x: 'id'):
    return Node(x)


def connected(x: 'id', y: 'id'):
    return find(x) == find(y)


def kruskal(G):
    G.sort(key=lambda e: e[2], reverse = True)
    max_V_number = max(G, key=lambda e: e[1])[1]
    vert = [make_set(v) for v in range(max_V_number + 1)]
    result = None
    for edge in G:
        u, v, weight = edge
        if not connected(vert[1], vert[2]):
            union(vert[u], vert[v])
            result = weight
    return result

test(kruskal)