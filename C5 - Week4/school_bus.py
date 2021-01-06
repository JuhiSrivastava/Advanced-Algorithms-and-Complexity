# python3
from itertools import permutations
from itertools import combinations
import numpy as np

INF = 10 ** 9

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph

def print_answer( weight_of_path, path ):
    print(weight_of_path)
    if weight_of_path == -1:
        return
    print(' '.join(map(str, path)))

def optimal_path( graph ):
    n = len(graph)
    C = [[INF for _ in range(n)] for __ in range(1 << n)]
    path = [[(-1, -1) for _ in range(n)] for __ in range(1 << n)]
    C[1][0] = 0
    for s in range(1, n):
        subsetS = combinations([_ for _ in range(n)],s)
        for S in list(subsetS):
            S = (0,) + S
            #print("Subset" , S)
            k = sum([1 << i for i in S])
            #print("k" , k)
            for i in S:
                if i != 0:
                    for j in S:
                        if j != i:
                            temp = C[k ^ (1 << i)][j] + graph[i][j]
                            if temp < C[k][i]:
                                C[k][i] = temp
                                path[k][i] = (k ^ (1 << i), j)

            #print(np.array(C))
    #print(path)
            #print("----------------")
    #find mini
    result, tempInd2 = min([(C[-1][i] + graph[i][0], i) for i in range(n)])
    
    if result >= INF:
        return (-1, [])

    newPath = []
    tempInd1 = (1 << n) - 1
    while -1 != tempInd1:
        newPath.insert(0, tempInd2 + 1)
        tempInd1, tempInd2 = path[tempInd1][tempInd2]
    return (result, newPath)

if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))