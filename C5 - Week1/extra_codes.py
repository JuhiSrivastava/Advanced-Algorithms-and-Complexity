# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph

def findAPath(graph, from_, to,flw,ids):
    paths =[]
    flows = []
    Idss = []
    queue = [[from_]]
    visits = [[0]*(to+1)]
    tempFlw = []
    tempIds = []
    while len(queue) >0:
        tempPath = queue[0]
        currentVertex = tempPath[-1]
        del queue[0]
        tempVisit = visits[0]
        tempVisit[currentVertex] = 1
        del visits[0]
        if len(flw) > 0:
            tempFlw = flw[0]
            del flw[0]
            tempIds = ids[0]
            del ids[0]
            
        #print("tempPath",tempPath)
        #print("tempVisit",tempVisit)
        #print("queue",queue)
        #print("visits",visits)
        #print("flw",flw)
        if currentVertex == to:
            paths.append(tempPath)
            flows.append(tempFlw)
            Idss.append(tempIds)
        else:
            lis = []
            for i in graph.graph[currentVertex]:
                if (i%2 == 0 and graph.edges[i].capacity - graph.edges[i].flow > 0) or (i%2 != 0 and graph.edges[i].capacity + graph.edges[i].flow > 0):
                    lis.append(i)
            for i in lis:
                if tempVisit[graph.edges[i].v] == 0:
                    newPath = tempPath + [graph.edges[i].v]
                    if i%2 == 0:
                        newFlw = tempFlw + [graph.edges[i].capacity - graph.edges[i].flow]
                    else:
                        newFlw = tempFlw + [graph.edges[i].capacity + graph.edges[i].flow]
                    newIds = tempIds + [i]
                    newVisit = tempVisit.copy()
                    queue.append(newPath)
                    visits.append(newVisit)
                    flw.append(newFlw)
                    ids.append(newIds)
        #print("queue",queue)
        #print("flw",flw)
        #print("Aftr-----------------")
    #print("Juhi",paths,flows,Idss)
    if len(paths) > 0:
        return paths[0],flows[0],Idss[0]
    else:
        return paths,flows,Idss

def max_flow(graph, from_, to):
    flow = 0
    pathsl = []
    idsl =[]
    while(True):
        path,flw,ids = findAPath(graph, from_, to,[],[])
        print(path,flw)
        for i in ids:
            graph.add_flow(i,1)
        if from_ in path: 
            del ids[0]
            del path[0]
        if to in path:
            del ids[-1]
            del path[-1]
        if len(path) == 2:
            pathsl.append(path)
            idsl.append(ids)
        if len(flw) == 0:
            break
        flow = flow + 1
        #for i in graph.edges:
            #print("i: ",i.u,"to",i.v,"capacity",i.capacity,"flow",i.flow)
    print("=====",pathsl,idsl)    
    return pathsl,idsl


class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        vertex_count = m+n+2
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        graph = FlowGraph(vertex_count)
        count = 1;
        for i in range(n):
            graph.add_edge(0,i+1,1)
            for j in range(m):
                if adj_matrix[i][j] == 1:
                    graph.add_edge(i+1,n+j+1,1)
                    graph.add_edge(n+j+1,m+n+1,1)
        return graph,n

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, paths, n):
        matching = [-1] * n
        for i,j in paths:
            matching[j-1] = i-n-1
        return matching

    def solve(self):
        graph,n = self.read_data()
        paths,ids = max_flow(graph, 0, graph.size() - 1)
        matching = self.find_matching(paths,n)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()


'''
# python3
class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):
        countL = [0]*len(adj_matrix)
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        matching = [-1] * n
        for i in range(n):
            countL[i] = adj_matrix[i].count(1)
            if countL[i] == 0:
                countL[i] = m+1
        #print(countL)
            
        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.
        
        #for i in range(m):
        while sum(countL) != (m+1)*n:
            #print("countL", countL)
            i = min(countL)
            #print("i", i)
            ind = countL.index(i)
            #print("ind", ind,adj_matrix)
            newind = adj_matrix[ind].index(1)
            adj_matrix[ind] = [0]*m
            matching[ind] = newind
            #busy_right[newind] = True
            #print("hi",matching)
            
            for j in range(n):
                adj_matrix[j][newind] = 0
                countL[j] = adj_matrix[j].count(1)
                if countL[j] == 0:
                    countL[j] = m+1
            #print(adj_matrix,countL)
        return matching

    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()

'''



'''
# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph

def findAPath(graph, from_, to,flw,ids):
    paths =[]
    flows = []
    Idss = []
    queue = [[from_]]
    visits = [[0]*(to+1)]
    tempFlw = []
    tempIds = []
    while len(queue) >0:
        tempPath = queue[0]
        currentVertex = tempPath[-1]
        del queue[0]
        tempVisit = visits[0]
        tempVisit[currentVertex] = 1
        del visits[0]
        if len(flw) > 0:
            tempFlw = flw[0]
            del flw[0]
            tempIds = ids[0]
            del ids[0]
            
        #print("tempPath",tempPath)
        #print("tempVisit",tempVisit)
        #print("queue",queue)
        #print("visits",visits)
        #print("flw",flw)
        if currentVertex == to:
            paths.append(tempPath)
            flows.append(tempFlw)
            Idss.append(tempIds)
        else:
            lis = []
            for i in graph.graph[currentVertex]:
                if (i%2 == 0 and graph.edges[i].capacity - graph.edges[i].flow > 0) or (i%2 != 0 and graph.edges[i].capacity + graph.edges[i].flow > 0):
                    lis.append(i)
            for i in lis:
                if tempVisit[graph.edges[i].v] == 0:
                    newPath = tempPath + [graph.edges[i].v]
                    if i%2 == 0:
                        newFlw = tempFlw + [graph.edges[i].capacity - graph.edges[i].flow]
                    else:
                        newFlw = tempFlw + [graph.edges[i].capacity + graph.edges[i].flow]
                    newIds = tempIds + [i]
                    newVisit = tempVisit.copy()
                    queue.append(newPath)
                    visits.append(newVisit)
                    flw.append(newFlw)
                    ids.append(newIds)
        #print("queue",queue)
        #print("flw",flw)
        #print("Aftr-----------------")
    #print("Juhi",paths,flows,Idss)
    if len(paths) > 0:
        return paths[0],flows[0],Idss[0]
    else:
        return paths,flows,Idss

def max_flow(graph, from_, to):
    flow = 0
    pathsl = []
    idsl =[]
    while(True):
        path,flw,ids = findAPath(graph, from_, to,[],[])
        print(path,flw)
        for i in ids:
            graph.add_flow(i,1)
        if from_ in path: 
            del ids[0]
            del path[0]
        if to in path:
            del ids[-1]
            del path[-1]
        if len(path) == 2:
            pathsl.append(path)
            idsl.append(ids)
        if len(flw) == 0:
            break
        flow = flow + 1
        for i in graph.edges:
            print("i: ",i.u,"to",i.v,"capacity",i.capacity,"flow",i.flow)
    print("=====",pathsl,idsl)    
    return pathsl,idsl


class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        vertex_count = m+n+2
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        graph = FlowGraph(vertex_count)
        count = 1;
        for i in range(n):
            graph.add_edge(0,i+1,1)
            for j in range(m):
                if adj_matrix[i][j] == 1:
                    graph.add_edge(i+1,n+j+1,1)
                    graph.add_edge(n+j+1,m+n+1,1)
        return graph,n

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, paths, n):
        matching = [-1] * n
        for i,j in paths:
            matching[i-1] = j-n-1
        return matching

    def solve(self):
        graph,n = self.read_data()
        paths,ids = max_flow(graph, 0, graph.size() - 1)
        matching = self.find_matching(paths,n)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()




'''


'''
# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow

def findAPath(graph, from_, to,ids):
    queue = [[from_]]
    visits = [[0]*(to+1)]
    tempIds = []
    while len(queue) >0:
        tempPath = queue[0]
        currentVertex = tempPath[-1]
        del queue[0]
        tempVisit = visits[0]
        tempVisit[currentVertex] = 1
        del visits[0]
        if len(ids) > 0:
            tempIds = ids[0]
            del ids[0]
        if currentVertex == to:
            return tempPath,tempIds
        else:
            for i in graph.graph[currentVertex]:
                if graph.edges[i].capacity - graph.edges[i].flow > 0:
                    if tempVisit[graph.edges[i].v] == 0:
                        #newVisit = tempVisit.copy()
                        queue.append(tempPath + [graph.edges[i].v])
                        visits.append(tempVisit)
                        ids.append(tempIds + [i])
    return [],[]

def max_flow(graph, from_, to,matching,n):
    while(True):
        path,ids = findAPath(graph, from_, to,[])
        if len(path) == 0:
            break
        for i in range(1,len(path)-1):
            if ids[i]%2 == 0:
                flw = graph.edges[ids[i]].capacity - graph.edges[ids[i]].flow
            else:
                flw = graph.edges[ids[i]].capacity + graph.edges[ids[i]].flow 
            if flw > 0 and i+2 <= len(path)-1:
                matching[path[i]-1] = path[i+1]-n-1
        for i in ids:
            graph.add_flow(i,1)     
    return matching


class MaxMatching:
    def read_data(self):
        unassign = []
        n, m = map(int, input().split())
        graph = FlowGraph(m+n+2)
        flag = True
        for i in range(n):
            li = list(map(int, input().split()))
            if len(li) == li.count(1):
                unassign.append(i)
                continue
            graph.add_edge(0,i+1,1)
            for j in range(m):
                if li[j] == 1:
                    graph.add_edge(i+1,n+j+1,1)
                if flag:
                    graph.add_edge(n+j+1,m+n+1,1)
            if flag:
                flag =False
        return graph,n,m,unassign

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def solve(self):
        graph,n,m,unassign = self.read_data()
        matching = [-1] * n
        matching = max_flow(graph, 0, graph.size() - 1,matching,n)
        for i in range(len(unassign)-1,-1,-1):
            for j in range(m):
                if j not in matching:
                    matching[unassign[i]] = j
                    break
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
'''