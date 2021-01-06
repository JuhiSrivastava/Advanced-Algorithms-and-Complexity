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
        self.edges[id].capacity -= flow
        self.edges[id ^ 1].capacity += flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph

def findAPath(graph, from_, to,visited, path,flw,ids):
    start = from_
    if visited[start] == 1 and start != to:
        return False
    if start == to:
        return True
    visited[start] = 1
    lis = []
    #print("start", graph.graph[start])
    for i in graph.graph[start]:
        if graph.edges[i].capacity > 0:
            lis.append(i)
    #print("after",lis)
    for i in lis:
        #print("i",graph.edges[i].u,"to",graph.edges[i].v)
        if findAPath(graph, graph.edges[i].v, to,visited, path,flw,ids):
            flw.append(graph.edges[i].capacity)
            path.append(start)
            #print("i",graph.edges[i].u,"to",graph.edges[i].v,"path",path)
            #print("flow", flw)
            ids.append(i)
            #print("ids", ids)
            return True

def max_flow(graph, from_, to):
    
    flow = 0
    while(True):
        visited = [0]*(to+1)
        path = [to]
        flw = []
        ids = []
        #for i in graph.edges:
            #print("i: ",i.u,"to",i.v,"capacity",i.capacity)
        findAPath(graph, from_, to,visited, path,flw,ids)
        #print("hi",path)
        #print("hi",flw)
        if len(flw) == 0:
            break
        mini = min(flw)
        flow = flow + mini
        for i in ids:
            graph.add_flow(i,mini)
        #for i in graph.edges:
            #print("i: ",i.u,"to",i.v,"capacity",i.capacity)
        #print("---------------",flow)
    # your code goes here
    return flow


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))

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
                if graph.edges[i].capacity - graph.edges[i].flow > 0:
                    lis.append(i)
            for i in lis:
                if tempVisit[graph.edges[i].v] == 0:
                    newPath = tempPath + [graph.edges[i].v]
                    newFlw = tempFlw + [graph.edges[i].capacity - graph.edges[i].flow]
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
    while(True):
        #for i in graph.edges:
            #print("i: ",i.u,"to",i.v,"capacity",i.capacity)
        path,flw,ids = findAPath(graph, from_, to,[],[])
        #print("hi",path,flw,ids)
        if len(flw) == 0:
            break
        mini = min(flw)
        flow = flow + mini
        for i in ids:
            graph.add_flow(i,mini)
        #for i in graph.edges:
            #print("i: ",i.u,"to",i.v,"capacity",i.capacity)
        #print("---------------",flow)
    # your code goes here
    return flow


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))

'''