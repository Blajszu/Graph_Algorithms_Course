from tester import test

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = set()

    def add_edge(self, neighbor):
        self.adjacent.add(neighbor)

def lexBFS(graph, num_vertices):
    partitions = [set(range(num_vertices))]
    traversal_order = []

    while partitions:
        current_vertex = partitions[-1].pop()
        traversal_order.append(current_vertex)

        new_partitions = []
        for group in partitions:
            connected = group & graph[current_vertex].adjacent
            disconnected = group - connected
            if disconnected:
                new_partitions.append(disconnected)
            if connected:
                new_partitions.append(connected)
        partitions = new_partitions

    return traversal_order

def construct_graph(num_vertices, edges):
    graph = [Vertex(i) for i in range(num_vertices)]
    for x, y, _ in edges:
        graph[x - 1].add_edge(y - 1)
        graph[y - 1].add_edge(x - 1)
    return graph

def verify_chordal(edges, num_vertices):
    graph = construct_graph(num_vertices, edges)
    bfs_order = lexBFS(graph, num_vertices)
    position = {bfs_order[i]: i for i in range(num_vertices)}

    for idx in range(num_vertices):
        node = bfs_order[idx]
        prev_neighbors = [neighbor for neighbor in graph[node].adjacent if position[neighbor] < position[node]]
        for j in range(len(prev_neighbors)):
            for k in range(j + 1, len(prev_neighbors)):
                if prev_neighbors[k] not in graph[prev_neighbors[j]].adjacent:
                    return False
    return True

def compute_largest_clique(edges, num_vertices):
    graph = construct_graph(num_vertices, edges)
    bfs_order = lexBFS(graph, num_vertices)
    position = {bfs_order[i]: i for i in range(num_vertices)}
    max_clique = 0

    for node in bfs_order:
        earlier_neighbors = {neighbor for neighbor in graph[node].adjacent if position[neighbor] < position[node]}
        clique_size = len(earlier_neighbors) + 1
        max_clique = max(max_clique, clique_size)

    return max_clique

def calculate_chromatic_number(edges, num_vertices):
    graph = construct_graph(num_vertices, edges)
    bfs_order = lexBFS(graph, num_vertices)
    colors = [0] * num_vertices

    for node in bfs_order:
        used_colors = {colors[neighbor] for neighbor in graph[node].adjacent if colors[neighbor] > 0}
        color_choice = 1
        while color_choice in used_colors:
            color_choice += 1
        colors[node] = color_choice

    return max(colors)

def find_min_vertex_cover(edges, num_vertices):
    graph = construct_graph(num_vertices, edges)
    bfs_order = lexBFS(graph, num_vertices)
    bfs_order.reverse()
    independent_set = set()

    for node in bfs_order:
        if all(neigh not in independent_set for neigh in graph[node].adjacent):
            independent_set.add(node)

    vertex_cover_size = num_vertices - len(independent_set)
    return vertex_cover_size

# test(verify_chordal, "chordal")
# test(compute_largest_clique, "maxclique")
# test(calculate_chromatic_number, "coloring")
# test(find_min_vertex_cover, "vcover")
