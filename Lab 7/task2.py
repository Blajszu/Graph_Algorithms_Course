import networkx as nx
from dimacs import loadCNFFormula, readSolution
from os import listdir
import time

def build_implication_graph(clauses, num_vars):
    G = nx.DiGraph()
    
    for i in range(1, num_vars + 1):
        G.add_node(i)
        G.add_node(-i)
    
    for clause in clauses:
        x, y = clause
        G.add_edge(-x, y)
        G.add_edge(-y, x)
    
    return G

def is_satisfiable(clauses, num_vars):
    G = build_implication_graph(clauses, num_vars)
    
    sccs = list(nx.strongly_connected_components(G))
    
    scc_map = {}
    for i, component in enumerate(sccs):
        for node in component:
            scc_map[node] = i
    
    for var in range(1, num_vars + 1):
        if scc_map[var] == scc_map[-var]:
            return False
    
    dag = nx.DiGraph()
    for u, v in G.edges():
        if scc_map[u] != scc_map[v]:
            dag.add_edge(scc_map[u], scc_map[v])
    
    topological_order = list(nx.topological_sort(dag))
    assignment = {}
    
    for scc_idx in reversed(topological_order):
        for node in sccs[scc_idx]:
            if abs(node) not in assignment:
                if node > 0:
                    assignment[abs(node)] = True
                else:
                    assignment[abs(node)] = False
    
    return True


def test(alg_sol, directory):
    graph_files = list(filter(lambda x: x[0] != ".", listdir(f'Lab7/{directory}/')))
    test_number = len(graph_files)
    cnt_true = 0
    cnt_false = 0
    sum_time = 0
    
    for idx, name in enumerate(graph_files):
        num_vars, edges = loadCNFFormula(f'Lab7/{directory}/{name}')
        expected_result = int(readSolution(f'Lab7/{directory}/{name}').replace("solution=", ""))
        
        start_time = time.time()
        is_sat = alg_sol(edges, num_vars)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        sum_time += elapsed_time
        res = (is_sat and expected_result == 1) or (not is_sat and expected_result == 0)
        
        if res:
            cnt_true += 1
        else:
            cnt_false += 1
        
        print("===========")
        print(f"TEST {idx} DLA GRAFU: {name}")
        print("Wynik algorytmu:", is_sat)
        print("Oczekiwane rozwiązanie:", bool(expected_result))
        print("ZALICZONY" if res else "NIEZALICZONY")
        print(f"Czas wykonania testu: {elapsed_time:.4f} sekund")
        print("===========")
    
    print("===PODSUMOWANIE===")
    print(f"Testy zaliczone: {cnt_true}/{test_number}")
    print(f"Testy niezaliczone: {cnt_false}/{test_number}")
    print(f"Łączny czas wykonania: {round(sum_time, 4)} sekund")

if __name__ == "__main__":
    test(is_satisfiable, "sat")