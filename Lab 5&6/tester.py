import time
from dimacs import *
from os import listdir

def test(alg_sol, directory):

    graph_names = list(filter(lambda x: x[0] != ".", listdir(f'Lab4/{directory}/')))
    test_numer = len(graph_names)
    cnt_true = 0
    cnt_false = 0
    sum_time = 0
    cnt = 0

    for name in graph_names:
        
        V, L = loadDirectedWeightedGraph(f'Lab4/{directory}/{name}')
        sol = readSolution(f'Lab4/{directory}/{name}')

        # Pomiar czasu start
        start_time = time.time()
        res_value = int(alg_sol(L, V))
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


def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[vs[i]].out
      Nj = G[vs[j]].out

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True