from tester import test

class Node:
    def __init__(self):
        self.edges = {}  
        self.active = True  
        self.merged_vertices = {self}  #
    
    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight
    
    def delEdge(self, to):
        if to in self.edges:
            del self.edges[to]

class Graph:
    def __init__(self, V, edges):
        self.nodes = [Node() for _ in range(V)]
        self.active_count = V
        for x, y, c in edges:
            x -= 1
            y -= 1
            self.nodes[x].addEdge(y, c)
            self.nodes[y].addEdge(x, c)
    
    def mergeVertices(self, x, y):
        self.nodes[x].merged_vertices.update(self.nodes[y].merged_vertices)
        
      
        for neighbor, weight in self.nodes[y].edges.items():
            if neighbor != x: 
                self.nodes[x].addEdge(neighbor, weight)
                self.nodes[neighbor].delEdge(y)  
                self.nodes[neighbor].addEdge(x, weight)  
        
        
        self.nodes[y].active = False
        self.nodes[y].edges.clear()
        self.active_count -= 1
    
    def getActiveNodes(self):
        
        return [i for i, node in enumerate(self.nodes) if node.active]

def minimumCutPhase(G):
    active = G.getActiveNodes()
    if len(active) < 2:
        return float('inf')
    a = active[0]
    A = {a}  
    weights = {v: 0 for v in active}  
    
    for neighbor, weight in G.nodes[a].edges.items():
        if G.nodes[neighbor].active:
            weights[neighbor] = weight
    
    cut_sequence = [a]  
    last_cut_weight = 0 
    while len(A) < len(active):
        
        max_weight = float('-inf')
        next_vertex = None
        
        for v in active:
            if v not in A and weights[v] > max_weight:
                max_weight = weights[v]
                next_vertex = v
        
        if next_vertex is None:
            break

        A.add(next_vertex)
        cut_sequence.append(next_vertex)
        last_cut_weight = max_weight
   
        for neighbor, weight in G.nodes[next_vertex].edges.items():
            if G.nodes[neighbor].active and neighbor not in A:
                weights[neighbor] += weight
    
    if len(cut_sequence) < 2:
        return float('inf')

    t = cut_sequence[-1]  
    s = cut_sequence[-2]  
    G.mergeVertices(s, t)
    
    return last_cut_weight

def stoerWagner(V, L):
    G = Graph(V, L)
    min_cut = float('inf')
    
    while G.active_count > 1:
        current_cut = minimumCutPhase(G)
        min_cut = min(min_cut, current_cut)
    
    return min_cut

test(stoerWagner)