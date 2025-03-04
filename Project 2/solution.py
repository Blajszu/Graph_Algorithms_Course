from data import runtests
from collections import deque

def solve(N, M, holes, pieces):
    holes_set = set(holes) 

    init_state = tuple(sorted(pieces))

    state_to_id = {}
    id_to_state = []
    graph = []

    from collections import deque
    queue = deque()

    def add_state(state):

        if state not in state_to_id:
            state_id = len(id_to_state)
            state_to_id[state] = state_id
            id_to_state.append(state)
            graph.append([])
            queue.append(state_id)
        
        return state_to_id[state]

    add_state(init_state)

    def occupied_positions(state):
        return {(i, j) for (_, i, j) in state}

    def get_moves(ptype, i, j, state):
        occ = occupied_positions(state)
        moves = []
        if ptype == "k": 
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 1 <= ni <= N and 1 <= nj <= M and (ni, nj) not in holes_set and (ni, nj) not in occ:
                        moves.append((ni, nj))
        elif ptype == "n":
            for di, dj in ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)):
                ni, nj = i+di, j+dj
                if 1 <= ni <= N and 1 <= nj <= M and (ni, nj) not in holes_set and (ni, nj) not in occ:
                    moves.append((ni, nj))
        else:
            if ptype == "r": 
                directions = [(1,0), (-1,0), (0,1), (0,-1)]
            elif ptype == "b":
                directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
            elif ptype == "q": 
                directions = [(1,0), (-1,0), (0,1), (0,-1),
                              (1,1), (1,-1), (-1,1), (-1,-1)]
            else:
                directions = []
            for di, dj in directions:
                ni, nj = i, j
                while True:
                    ni += di
                    nj += dj
                    if not (1 <= ni <= N and 1 <= nj <= M):
                        break
                    if (ni, nj) in holes_set:
                        break
                    if (ni, nj) in occ:
                        break
                    moves.append((ni, nj))
        return moves

    while queue:

        cur_id = queue.popleft()
        cur_state = id_to_state[cur_id]

        for idx, (ptype, i, j) in enumerate(cur_state):
            for (ni, nj) in get_moves(ptype, i, j, cur_state):

                new_state_list = list(cur_state)
                new_state_list[idx] = (ptype, ni, nj)
                new_state = tuple(sorted(new_state_list))
                new_id = add_state(new_state)
                
                if new_id not in graph[cur_id]:
                    graph[cur_id].append(new_id)
                
                if cur_id not in graph[new_id]:
                    graph[new_id].append(cur_id)

    matching = edmonds_maximum_matching(graph)
    M_size = len(matching) // 2

    start_id = state_to_id[init_state]
    
    if start_id not in matching:
        return False

    graph_removed, _ = remove_vertex_from_graph(graph, start_id)
    matching_removed = edmonds_maximum_matching(graph_removed)
    M_size_removed = len(matching_removed) // 2

    if M_size_removed == M_size:
        return False
    else:
        return True

def remove_vertex_from_graph(graph, rem):
    n = len(graph)
    mapping = {}
    new_graph = []
    new_id_to_old = []
    
    for old_id in range(n):
        if old_id == rem:
            continue
        new_id = len(new_graph)
        mapping[old_id] = new_id
        new_id_to_old.append(old_id)
        new_graph.append([])
    
    for old_id in range(n):
        if old_id == rem:
            continue
        
        new_u = mapping[old_id]
        
        for v in graph[old_id]:
            if v == rem:
                continue
            
            new_v = mapping[v]
            new_graph[new_u].append(new_v)
    
    return new_graph, mapping

def edmonds_maximum_matching(graph):
    
    n = len(graph)
    match = [-1] * n
    p = [-1] * n
    base = list(range(n))
    used = [False] * n
    blossom = [False] * n

    def lca(a, b):
       
        used2 = [False] * n
        
        while True:
            a = base[a]
            used2[a] = True
            
            if match[a] == -1:
                break
            
            a = p[match[a]]
       
        while True:
            b = base[b]
            
            if used2[b]:
                return b
            
            b = p[match[b]]

    def markPath(v, b, x):
        
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = x
            x = match[v]
            v = p[match[v]]

    def findPath(start):

        nonlocal used, p, base, blossom
       
        used[:] = [False] * n
        p[:] = [-1] * n
        
        for i in range(n):
            base[i] = i
        
        q = deque()
        q.append(start)
        used[start] = True
        
        while q:
            v = q.popleft()

            for u in graph[v]:
                if base[v] == base[u] or match[v] == u:
                    continue
                
                if u == start or (match[u] != -1 and p[match[u]] != -1):
                    curbase = lca(v, u)
                    blossom[:] = [False] * n
                    markPath(v, curbase, u)
                    markPath(u, curbase, v)
                    
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                q.append(i)

                elif p[u] == -1:
                    p[u] = v
                    
                    if match[u] == -1:
                        cur = u
                        
                        while cur != -1:
                            prev = p[cur]
                            nxt = match[prev] if prev != -1 else -1
                            match[cur] = prev
                            match[prev] = cur
                            cur = nxt
                        
                        return True
                    else:
                        used[match[u]] = True
                        q.append(match[u])
        
        return False

    for v in range(n):
        if match[v] == -1:
            if findPath(v):
                pass
    
    matching = {}
    
    for i in range(n):
        if match[i] != -1 and i < match[i]:
            matching[i] = match[i]
            matching[match[i]] = i
    
    return matching

runtests(solve)