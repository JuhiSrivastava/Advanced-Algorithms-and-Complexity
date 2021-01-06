# python3
import sys
import resource
from time import perf_counter
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

   
class Graph: 
   
    def __init__(self,vertices): 
        self.V= vertices  
        self.graph = [[] for _ in range(self.V)]
        self.graphT = [[] for _ in range(self.V)]
 
    def addEdge(self,u,v): 
        self.graph[u].append(v)
        self.graphT[v].append(u)
        
def DFS(graph,stack,visited,vertex):
    visited[vertex] = 1
    for i in graph[vertex]:
        if visited[i] == 0:
            DFS(graph,stack,visited,i)
    stack.append(vertex)
    return stack,visited
                
        
def StonglyConnectedComponents(graph1):
    t1_start = perf_counter()
    visited = [0]*graph1.V
    start = visited.index(0)
    newstack = []*graph1.V
    while 0 in visited:
        newstack,visited  = DFS(graph1.graph,newstack ,visited, start)
        if 0 in visited:
            start = visited.index(0)
    #print(newstack)
    graph2 = graph1.graphT
    components = []
    while len(newstack) > 0:
        start = newstack[-1]
        del newstack[-1]
        tempstack,visited  = DFS(graph2,[]*graph1.V ,[0]*graph1.V, start)
        final = []
        for i in tempstack:
            if i in newstack:
                final = [i] + final
                newstack.remove(i)
            if i == start:
                final = [i] + final
        if len(final) > 0:
            components.append(final)
    return components
    

def ImplicationGraph():
    graph1 = Graph(2*n) 
    for clause in clauses:
        if clause[0] > 0 and clause[1] > 0:
            graph1.addEdge(clause[0]*2 -1,clause[1]*2 -2)
            graph1.addEdge(clause[1]*2 -1,clause[0]*2 -2)
        elif clause[0] < 0 and clause[1] > 0:
            graph1.addEdge(clause[0]*-2 -2,clause[1]*2 -2)
            graph1.addEdge(clause[1]*2 -1,clause[0]*-2 -1)
        elif clause[0] > 0 and clause[1] < 0:
            graph1.addEdge(clause[0]*2 -1,clause[1]*-2 -1)
            graph1.addEdge(clause[1]*-2 -2,clause[0]*2 -2)
        elif clause[0] < 0 and clause[1] < 0:
            graph1.addEdge(clause[0]*-2 -2,clause[1]*-2 -1)
            graph1.addEdge(clause[1]*-2 -2,clause[0]*-2 -1)
    #print(graph1.graph)
    return graph1

# This solution tries all possible 2^n variable assignments.
# It is too slow to pass the problem.
# Implement a more efficient algorithm here.
def isSatisfiable(): 
    graph = ImplicationGraph()
    components = StonglyConnectedComponents(graph)
    #print(components)
    assignments = [-1]*n
    for i in components:
        if -1 not in assignments:
            break
        for j in range(len(i)-1,-1,-1):
            if assignments[int(i[j]/2)] == -1:
                if i[j]%2 == 0:
                    if i[j] + 1 in i:
                        return None
                    assignments[int(i[j]/2)] = 1
                else:
                    if i[j] -1 in i or (0 in i and 1 in i):
                        return None
                    assignments[int((i[j]-1)/2)] = 0
    return assignments


n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]

result = isSatisfiable()
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE");
    print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
