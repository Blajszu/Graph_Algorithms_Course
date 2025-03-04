import time
from dimacs import *

def test(alg_sol):

    graph_names = ["clique5", "clique20", "clique100", "clique1000", "g1", "grid5x5", "grid100x100", "path10", "path1000", "pp10", "pp100", "pp1000", "rand20_100", "rand100_500", "rand1000_100000"]
    test_numer = len(graph_names)
    cnt_true = 0
    cnt_false = 0
    sum_time = 0
    cnt = 0

    for name in graph_names:
        
        V, L = loadWeightedGraph("Lab1/grafy/" + name)
        sol = readSolution("Lab1/grafy/" + name)

        # Pomiar czasu start
        start_time = time.time()
        res_value = int(alg_sol(L))
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Pomiar czasu koniec

        sum_time += elapsed_time

        res = res_value == int(sol)
        if res: 
            cnt_true += 1
        else: 
            cnt_false += 1
        
        print("===========")
        print("TEST " + str(cnt) + " DLA GRAFU:", name)
        print("Wynik algorytmu:", res_value)
        print("Oczekiwane rozwiązanie:", sol)
        print("ZALICZONY") if res else print("NIEZALICZONY")
        print("Czas wykonania testu: {:.4f} sekund".format(elapsed_time))
        print("===========")
        cnt += 1
    
    print("===PODSUMOWANIE===")
    print("Testy zaliczone: {}/{}".format(cnt_true, test_numer))
    print("Testy niezaliczone: {}/{}".format(cnt_false, test_numer))
    print("Łączny czas wykonania: {} sekund".format(round(sum_time, 4)))
