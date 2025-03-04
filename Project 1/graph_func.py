import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def print_graph_master(graph_matrix, edge_weights = False, vertex_weights_array = [], directed = False, font_size = 12):
    
    vertex_weights = vertex_weights_array != []
    
    graph_matrix = np.array(graph_matrix)
    G = None
    if directed:
        G = nx.from_numpy_array(graph_matrix, create_using=nx.DiGraph)
    else:
        G = nx.from_numpy_array(graph_matrix)
    pos = nx.spring_layout(G)
    if directed:
        nx.draw(G, pos, with_labels=(not vertex_weights), node_color='skyblue', node_size=font_size*50, font_size=font_size, font_color='black', arrowsize=20)
    else:
        nx.draw(G, pos, with_labels=(not vertex_weights), node_color='skyblue', node_size=font_size*50, font_size=font_size, font_color='black')
    
    if vertex_weights:
        vertex_weights_dict = {index: value for index, value in enumerate(vertex_weights_array)}
        nx.set_node_attributes(G, vertex_weights_dict, 'weight')
        node_labels = nx.get_node_attributes(G, 'weight')
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_size)

    if edge_weights and not directed:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        for k, v in edge_labels.items():
            if v == 1.12321:
                edge_labels[k] = 0
            if edge_labels[k] == int(edge_labels[k]):
                edge_labels[k] = int(edge_labels[k])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=font_size)

    if edge_weights and directed:
        edge_weights = {}
        for i in range(len(graph_matrix)):
            for j in range(len(graph_matrix)):
                weight = graph_matrix[i][j]
                if weight != 0:
                    if (i, j) in edge_weights:
                        edge_weights[(i, j)].append(weight)
                    else:
                        edge_weights[(i, j)] = [weight]

        for edge, _ in list(edge_weights.items()):
            if edge[::-1] in edge_weights and edge_weights[edge] is not None:
                weight = edge_weights[edge[::-1]]
                edge_weights[edge[::-1]] = None
                edge_weights[edge] += weight

        edge_weights = { k:set(v) for k,v in edge_weights.items() if v != None }

        for edge, weights in edge_weights.items():
            G.edges[edge]['weight'] = weights

        edge_labels = {(i, j): ', '.join(map(str, weights)) for (i, j), weights in edge_weights.items()}
        for k, v in edge_labels.items():
            v = float(v)
            if v == 1.12321:
                edge_labels[k] = 0
            if v == int(v):
                edge_labels[k] = int(v)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=font_size)
    
    plt.show()

def generate_graph_matrix(num_vertices, num_edges):
    if num_edges > num_vertices * (num_vertices - 1) // 2:
        raise ValueError("Number of edges cannot exceed the maximum possible for a complete graph.")

    adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
    edges_added = 0

    while edges_added < num_edges:
        i, j = np.random.randint(0, num_vertices, size=2)
        if i != j and adj_matrix[i][j] == 0:
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
            edges_added += 1
    
    return adj_matrix.tolist()

def generate_directed_graph_matrix(num_vertices, num_edges):

    if num_edges > num_vertices * (num_vertices - 1):
        raise ValueError("Number of edges cannot exceed the maximum possible for a complete graph.")

    adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)

    for _ in range(num_edges):
        i, j = np.random.randint(0, num_vertices, size=2)
        adj_matrix[i, j] = 1

    np.fill_diagonal(adj_matrix, 0)
    return adj_matrix.tolist()

def generate_edge_weighted_directed_graph_matrix(num_vertices, num_edges, max_weight):

    if num_edges > num_vertices * (num_vertices - 1):
        raise ValueError("Number of edges cannot exceed the maximum possible for a complete graph.")

    adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)

    for _ in range(num_edges):
        i, j = np.random.randint(0, num_vertices, size=2)
        weight = np.random.randint(1, max_weight + 1)
        adj_matrix[i, j] = weight

    np.fill_diagonal(adj_matrix, 0)
    return adj_matrix.tolist()

def generate_edge_weighted_graph_matrix(num_vertices, num_edges, max_weight):

    if num_edges > num_vertices * (num_vertices - 1) // 2:
        raise ValueError("Number of edges cannot exceed the maximum possible for a complete graph.")

    adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
    edges_added = 0

    while edges_added < num_edges:
        i, j = np.random.randint(0, num_vertices, size=2)
        if i != j and adj_matrix[i][j] == 0:
            weight = np.random.randint(1, max_weight + 1)
            adj_matrix[i][j] = weight
            adj_matrix[j][i] = weight
            edges_added += 1
    
    return adj_matrix.tolist()

def generate_weights_for_verticles(G, max_weight):
    n = len(G)
    weights = [np.random.randint(1, max_weight + 1) for _ in range(n)]

    return weights

def convert_adjlist_to_matrix(G, for_printing = False):
    n = len(G)
    adj_matrix = [[0] * n for _ in range(n)]

    el = None
    for g in G:
        if g != []:
            el = g[0]
            break

    if type(el) == int:
        for i in range(n):
            for j in G[i]:
                adj_matrix[i][j] = 1
    elif type(el) == list or type(el) == tuple:
        for i in range(n):
            for j in G[i]:
                adj_matrix[i][j[0]] = 1.12321 if for_printing and j[1] == 0 else j[1]
    else:
        raise ValueError("Incorrect data format in the adjacency list.")
        
    return adj_matrix

def convert_matrix_to_adjlist(G):
    n = len(G)
    adj_list = [[] for _ in range(n)]
    
    if is_weighted_graph(G):
        for i in range(n):
            for j in range(n):
                if G[i][j] != 0:
                    adj_list[i].append([j, G[i][j]])
    else:
        for i in range(n):
            for j in range(n):
                if G[i][j] != 0:
                    adj_list[i].append(j)
    
    return adj_list

def convert_edgelist_to_matrix(G, directed = False, for_printing = False):
    if directed:
        maks = 0
        for el in G:
            maks = max(maks, el[0], el[1])
        
        adj_matrix = [[0] * (maks + 1) for _ in range(maks + 1)]

        if len(G[0]) == 2:
            for el in G:
                adj_matrix[el[0]][el[1]] = 1
        
        elif len(G[0]) == 3:
            for el in G:
                adj_matrix[el[0]][el[1]] = 1.12321 if for_printing and el[2] == 0 else el[2]
        else:
            raise ValueError("Incorrect data format.")

        return adj_matrix
    
    else:
        maks = 0
        for el in G:
            maks = max(maks, el[0], el[1])
        
        adj_matrix = [[0] * (maks + 1) for _ in range(maks + 1)]

        if len(G[0]) == 2:
            for el in G:
                adj_matrix[el[0]][el[1]] = 1
                adj_matrix[el[1]][el[0]] = 1
        
        elif len(G[0]) == 3:
            for el in G:
                adj_matrix[el[0]][el[1]] = el[2]
                adj_matrix[el[1]][el[0]] = el[2]
        
        else:
            raise ValueError("Incorrect data format.")

        return adj_matrix

def convert_edgelist_to_adjlist(G, directed = False):
    maks = 0
    for i in G:
        maks = max(maks, i[0], i[1])

    adj_list = [[] for _ in range(maks+1)]
    is_weighted_graph = (len(G[0]) == 3)

    if directed:
        if is_weighted_graph:
            for i in G:
                adj_list[i[0]].append((i[1], i[2]))
        else:
            for i in G:
                adj_list[i[0]].append(i[1])
    else:
        if is_weighted_graph:
            for i in G:
                adj_list[i[0]].append((i[1], i[2]))
                adj_list[i[1]].append((i[0], i[2]))
        else:
            for i in G:
                adj_list[i[0]].append(i[1])
                adj_list[i[1]].append(i[0])
    
    return adj_list
    
# Nie mam pojęcia po co mi te dwie funkcje
def convert_matrix_to_edgelist(G, directed = False):
    edgelist = []
    n = len(G)

    if directed:
        if is_weighted_graph(G):
            for i in range(n):
                for j in range(n):
                    if G[i][j] != 0:
                        edgelist.append([i, j, G[i][j]])
        else:
            for i in range(n):
                for j in range(n):
                    if G[i][j] != 0:
                        edgelist.append([i, j])
    
    else:
        if is_weighted_graph(G):
            for i in range(n):
                for j in range(i, n):
                    if G[i][j] != 0:
                        edgelist.append([i, j, G[i][j]])
        else:
            for i in range(n):
                for j in range(i, n):
                    if G[i][j] != 0:
                        edgelist.append([i, j])

    return edgelist

def convert_adjlist_to_edgelist(G, directed = False):
    edgelist = []
    n = len(G)

    if directed:
        if type(G[0][0]) == int:
            for i in range(n):
                for j in G[i]:
                    edgelist.append([i, j])
        elif type(G[0][0]) == list or type(G[0][0]) == tuple:
            for i in range(n):
                for j in G[i]:
                    edgelist.append([i, j[0], j[1]])
        else:
            raise ValueError("Incorrect data format in the adjacency list.")
    else:
        if type(G[0][0]) == int:
            for i in range(n):
                for j in G[i]:
                    if [j, i] not in edgelist:
                        edgelist.append([i, j])
        elif type(G[0][0]) == list or type(G[0][0]) == tuple:
            for i in range(n):
                for j in G[i]:
                    if [j[0], i, j[1]] not in edgelist:
                        edgelist.append([i, j[0], j[1]])
        else:
            raise ValueError("Incorrect data format in the adjacency list.")
    
    return edgelist

def is_weighted_graph(matrix):
    for row in matrix:
        for element in row:
            if element != 0 and element != 1:
                return True
    return False

def is_directed_graph(matrix):
    n = len(matrix)
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i] or (i == j and matrix[i][j] != 0):
                return True
    
    return False

def draw_graph_matrix(G, vertex_weights_array = [], font_size = 12, force_edge_weighted = False):
    edge_weighted = is_weighted_graph(G) or force_edge_weighted
    directed = is_directed_graph(G)

    print_graph_master(G, edge_weighted, vertex_weights_array, directed, font_size)

def draw_graph_adjlist(G, vertex_weights_array = [], font_size = 12, force_edge_weighted = False):
    G = convert_adjlist_to_matrix(G, for_printing = True)
    draw_graph_matrix(G, vertex_weights_array, font_size, force_edge_weighted)

def draw_graph_edgelist(G, directed = False, vertex_weights_array = [], font_size = 12, force_edge_weighted = False): #Nie wiem po chuj
    G = convert_edgelist_to_matrix(G, directed, for_printing = True)
    draw_graph_matrix(G, vertex_weights_array, font_size, force_edge_weighted)