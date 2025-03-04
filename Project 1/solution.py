from data import runtests
from collections import deque

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


def kruskal(G, N):
    
    G.sort(key=lambda e: e[2])

    vert = [make_set(i) for i in range(1, N+1)]
    vert = [None] + vert

    result = []
    for edge in G:
        u, v, _ = edge
        if not connected(vert[u], vert[v]):
            union(vert[u], vert[v])
            result.append(edge)

    return result

def optimized_bfs(N, G, needed):
    if not needed:
        return set()
    
    path_vertices = set()
    visited = [False] * (N + 1)
    parent = [None] * (N + 1)
    
    start = next(iter(needed))
    remaining_targets = needed
    remaining_targets.remove(start)
    
    Q = deque([start])
    visited[start] = True
    path_vertices.add(start)
    
    while Q and remaining_targets:
        x = Q.popleft()
        
        for v in G[x]:
            if not visited[v]:
                visited[v] = True
                parent[v] = x
                Q.append(v)
                
                if v in remaining_targets:
                    remaining_targets.remove(v)
                    curr = v
                    while curr is not None and curr not in path_vertices:
                        path_vertices.add(curr)
                        curr = parent[curr]
                        
    return path_vertices

def BFS(N, G, needed):
    if not needed:
        return set()
    
    path_vertices = set()
    start = next(iter(needed))
    
    all_targets = needed | {start}
    path_vertices.add(start)
    
    for target in all_targets:
        visited = [False] * (N+1)
        parent = [None] * (N+1)
        Q = deque([target])
        
        visited[target] = True
        found_targets = set()
        
        while Q and len(found_targets) < len(all_targets):
            x = Q.popleft()
            for v in G[x]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = x
                    Q.append(v)
                    if v in all_targets:
                        found_targets.add(v)
                        curr = v
                        while curr is not None:
                            path_vertices.add(curr)
                            curr = parent[curr]
    return path_vertices

def create_conflict_graph(K, trakt, lords):
    num_lords = len(lords)
    conflicts = [[] for _ in range(num_lords)]
    
    K_sets = [set(path) for path in K]
    
    edge_dict = {}
    for u, v, _ in trakt:
        u, v = u if u < v else v, u if u > v else v
        if u not in edge_dict:
            edge_dict[u] = set()
        edge_dict[u].add(v)
    
    for i in range(num_lords):
        for j in range(i + 1, num_lords):
            # Check set intersection first
            if K_sets[i] & K_sets[j]:
                conflicts[i].append(j)
                conflicts[j].append(i)
                continue
            
            has_conflict = False
            for u in K_sets[i]:
                if u in edge_dict:
                    for v in edge_dict[u]:
                        if v in K_sets[i] and u in K_sets[j] and v in K_sets[j]:
                            has_conflict = True
                            break
                if has_conflict:
                    break
            
            if has_conflict:
                conflicts[i].append(j)
                conflicts[j].append(i)
    
    return conflicts

def suma_wag_podgrafu(G, V_H):
    V_H = set(V_H)
    return sum(w for u, v, w in G if u in V_H and v in V_H)


def lexbfs(graph, start_vertex=None):
    all_vertices = set(range(len(graph)))
    if start_vertex is None:
        start_vertex = next(iter(all_vertices))

    partition = [all_vertices - {start_vertex}, {start_vertex}]
    visited_order = []

    while partition:
        current_set = partition.pop()
        current_vertex = current_set.pop()
        visited_order.append(current_vertex)
        if current_set:
            partition.append(current_set)
        
        new_partition = []
        for subset in partition:
            neighbors = {v for v in subset if v in graph[current_vertex]}
            non_neighbors = subset - neighbors
            if non_neighbors:
                new_partition.append(non_neighbors)
            if neighbors:
                new_partition.append(neighbors)

        partition = new_partition

    return visited_order

def my_solve(N, roads, lords):

    trakt = kruskal(roads, N)
    
    L = [[] for _ in range(N+1)]
    for v, u, _ in trakt:
        L[v].append(u)
        L[u].append(v)
    
    points = [set(lord) for lord in lords]
    
    K = [list(optimized_bfs(N, L, points[i])) for i in range(len(lords))]
    
    P = create_conflict_graph(K, trakt, lords)
    
    W = [suma_wag_podgrafu(trakt, path) for path in K]

    B = lexbfs(P)
    B.reverse()
    weights = W.copy()
    color = ['white'] * (len(lords) + 1)
    
    for i in range(1, len(B) + 1):
        if weights[B[i - 1]] > 0:
            color[B[i - 1]] = 'red'
            for neighbor in P[B[i-1]]:
                if neighbor in B[i:]:
                    a = weights[neighbor] - weights[B[i - 1]]
                    weights[neighbor] = a if a > 0 else 0
    
    for i in range(len(B), 0, -1):
        if color[B[i - 1]] == 'red':
            if all(color[neighbor] != 'blue' for neighbor in P[B[i-1]]):
                color[B[i - 1]] = 'blue'
    
    return sum(W[i] for i in range(len(color)) if color[i] == 'blue')
    
runtests(my_solve)