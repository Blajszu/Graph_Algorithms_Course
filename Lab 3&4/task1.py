from tester import test
from graph_func import *
from collections import deque
from copy import deepcopy

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

def ford_furkerson(V, G):
    G_mtx_main = convert_edgelist_to_matrix(G, directed=False)
    n = len(G_mtx_main)

    res_cnt = float('inf')

    for i in range(2, n-1):
        
        G_mtx = deepcopy(G_mtx_main)
        cnt = 0

        while True:
            
            # alg_result = DFS_matrix(G_mtx, 1, i)
            alg_result = BFS_matrix(G_mtx, 1, i)

            if alg_result == None:
                break

            path = reconstruct_path(alg_result, 1, i)

            for j in range(len(path) - 1):
                G_mtx[path[j]][path[j + 1]] = 0
                G_mtx[path[j + 1]][path[j]] = 0
            
            cnt += 1

        res_cnt = min(res_cnt, cnt)

    return res_cnt

test(ford_furkerson)