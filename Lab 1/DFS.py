from graph_func import convert_edgelist_to_adjlist
from Lab3.tester import *

def path_exists(adj, n, min_weight):
    
    def dfs(adj, visited, current, target, min_weight):
        if current == target:
            return True
        visited[current] = True
        for neighbor, weight in adj[current]:
            if not visited[neighbor] and weight >= min_weight:
                if dfs(adj, visited, neighbor, target, min_weight):
                    return True
        return False

    visited = [False] * n
    return dfs(adj, visited, 1, 2, min_weight)

def DFS_main(G):
    
    G_adj = convert_edgelist_to_adjlist(G)
    n = len(G_adj)

    left, right = 0, max(weight for _, _, weight in G)
    result = 0

    while left <= right:
        mid = (left + right) // 2
        if path_exists(G_adj, n, mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result

test(DFS_main)