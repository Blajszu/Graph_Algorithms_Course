from tester import test
from graph_func import *
from collections import deque

def DFS_matrix(G, start, t):
    n = len(G)
    
    visited = [False] * n
    parent = [None] * n

    def DFSvisit(G, u, t):
        visited[u] = True
        for v in range(n):
            if G[u][v] != 0:
                if not visited[v]:
                    parent[v] = u
                    DFSvisit(G, v, t)

    DFSvisit(G, start, t)
    
    if visited[t]:
        return parent

def BFS_matrix(G, start, t):
    Q = deque()

    n = len(G)
    d = [-1] * n
    visited = [False] * n
    parent = [None] * n

    d[start] = 0
    visited[start] = True
    
    Q.append(start)

    while len(Q) != 0:
        u = Q.popleft()

        if u == t:
            return parent

        for v in range(n):
            if G[u][v] != 0:
                if not visited[v]:
                    visited[v] = True
                    d[v] = d[u] + 1
                    parent[v] = u
                    Q.append(v)

    return None

def reconstruct_path(alg_result, s, t):
    result = [t]
    current = alg_result[t]

    while current != s:
        result.append(current)
        current = alg_result[current]
    
    result.append(s)
    return result

def ford_furkerson(G):
    G_mtx = convert_edgelist_to_matrix(G, directed=True)
    n = len(G_mtx)

    while True:
        
        # alg_result = DFS_matrix(G_mtx, 1, n-1)
        alg_result = BFS_matrix(G_mtx, 1, n-1)

        if alg_result == None:
            break

        path = reconstruct_path(alg_result, 1, n-1)
        mini = float('inf')

        for i in range(len(path) - 1):
            mini = min(mini, G_mtx[path[i + 1]][path[i]])

        for i in range(len(path) - 1):
            G_mtx[path[i]][path[i + 1]] += mini
            G_mtx[path[i + 1]][path[i]] -= mini

    return sum(G_mtx[-1])

test(ford_furkerson)