from heapq import heappush, heappop
from Lab3.tester import *
from graph_func import convert_edgelist_to_adjlist

def dijkstra(G):
    
    G = convert_edgelist_to_adjlist(G)

    n = len(G)
    pq = []
    max_min_edge = [0] * n
    max_min_edge[1] = float('inf')
    
    heappush(pq, (-float('inf'), 1))
    
    while pq:
        w, u = heappop(pq)
        w = -w

        if u == 2:
            return w

        for v, weight in G[u]:

            min_edge_path = min(w, weight)

            if min_edge_path > max_min_edge[v]:
                max_min_edge[v] = min_edge_path
                heappush(pq, (-min_edge_path, v))

test(dijkstra)