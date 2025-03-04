import networkx as nx
from tester import test

def max_flow(L, V):
    G = nx.DiGraph()

    for (u, v, w) in L:
        G.add_edge(u, v, capacity=w)

    source, sink = 1, V

    flow_value = nx.maximum_flow_value(G, source, sink)
    return flow_value

def check_planarity(L, V):
    G = nx.DiGraph()

    for (u, v, w) in L:
        G.add_edge(u, v, capacity=w)

    flow_value = nx.check_planarity(G)
    return flow_value[0]


# test(max_flow, "flow")
test(check_planarity, "graphs-lab7")