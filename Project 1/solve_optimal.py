from data import runtests
from collections import deque

class Node:
    def __init__(self, id_):
        self.id = id_
        self.parent = self
        self.rank = 0

def find(node):
    if node != node.parent:
        node.parent = find(node.parent)
    return node.parent

def union(node1, node2):
    root1 = find(node1)
    root2 = find(node2)
    
    if root1 == root2:
        return
    
    if root1.rank < root2.rank:
        root1.parent = root2
    
    else:
        root2.parent = root1
        if root1.rank == root2.rank:
            root1.rank += 1

def make_set(node_id):
    return Node(node_id)

def connected(node1, node2):
    return find(node1) == find(node2)

def kruskal(edges, node_count):
    
    edges.sort(key=lambda e: e[2])
    nodes = [make_set(i) for i in range(1, node_count + 1)]
    nodes = [None] + nodes
    mst = []
    
    for u, v, weight in edges:
        if not connected(nodes[u], nodes[v]):
            union(nodes[u], nodes[v])
            mst.append((u, v, weight))
    
    return mst

def bfs_find_path(node_count, adjacency_list, targets):
    if not targets:
        return set()
    
    path_nodes = set()
    visited = [False] * (node_count + 1)
    parent = [None] * (node_count + 1)
    start = next(iter(targets))
    remaining = targets
    remaining.remove(start)
    queue = deque([start])
    visited[start] = True
    path_nodes.add(start)
    
    while queue and remaining:
        node = queue.popleft()
        
        for neighbor in adjacency_list[node]:
            
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = node
                queue.append(neighbor)
                
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    current = neighbor
                   
                    while current is not None and current not in path_nodes:
                        path_nodes.add(current)
                        current = parent[current]
    return path_nodes

def build_conflict_graph(paths):
    num_paths = len(paths)
    conflicts = [set() for _ in range(num_paths)]
    path_sets = [set(path) for path in paths]
    edge_sets = []
    
    for path in paths:
        edges = set()
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edges.add((min(u, v), max(u, v)))
        
        edge_sets.append(edges)
    
    for i in range(num_paths):
        
        for j in range(i + 1, num_paths):
            
            if not path_sets[i].isdisjoint(path_sets[j]):
                conflicts[i].add(j)
                conflicts[j].add(i)
            
            elif not edge_sets[i].isdisjoint(edge_sets[j]):
                conflicts[i].add(j)
                conflicts[j].add(i)
    
    return [list(c) for c in conflicts]

def calculate_subgraph_weight(edges, vertices):
    vertices = set(vertices)
    return sum(weight for u, v, weight in edges if u in vertices and v in vertices)

def lexbfs(graph):
    
    all_nodes = set(range(len(graph)))
    start = next(iter(all_nodes))
    partition = [all_nodes - {start}, {start}]
    order = []
    
    while partition:
        current_set = partition.pop()
        current_node = current_set.pop()
        order.append(current_node)
        
        if current_set:
            partition.append(current_set)
        
        new_partition = []
       
        for subset in partition:
            neighbors = {node for node in subset if node in graph[current_node]}
            non_neighbors = subset - neighbors
            
            if non_neighbors:
                new_partition.append(non_neighbors)
            
            if neighbors:
                new_partition.append(neighbors)
        
        partition = new_partition
    
    return order

def solve_problem(node_count, edges, groups):
    
    mst = kruskal(edges, node_count)
    adjacency_list = [[] for _ in range(node_count + 1)]
    
    for u, v, _ in mst:
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)
    
    group_sets = [set(group) for group in groups]
    paths = [list(bfs_find_path(node_count, adjacency_list, group)) for group in group_sets]
    conflict_graph = build_conflict_graph(paths)
    path_weights = [calculate_subgraph_weight(mst, path) for path in paths]
    lex_order = lexbfs(conflict_graph)
    lex_order.reverse()
    remaining_weights = path_weights.copy()
    colors = ['white'] * (len(groups) + 1)
    
    for idx in range(1, len(lex_order) + 1):
        
        if remaining_weights[lex_order[idx - 1]] > 0:
            colors[lex_order[idx - 1]] = 'red'
            
            for neighbor in conflict_graph[lex_order[idx - 1]]:
                
                if neighbor in lex_order[idx:]:
                    new_weight = remaining_weights[neighbor] - remaining_weights[lex_order[idx - 1]]
                    remaining_weights[neighbor] = max(new_weight, 0)
    
    for idx in range(len(lex_order), 0, -1):
       
        if colors[lex_order[idx - 1]] == 'red':
            
            if all(colors[neighbor] != 'blue' for neighbor in conflict_graph[lex_order[idx - 1]]):
                colors[lex_order[idx - 1]] = 'blue'
   
    return sum(path_weights[i] for i in range(len(colors)) if colors[i] == 'blue')

runtests(solve_problem)