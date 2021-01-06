#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree

def funParty(vertex1,parent,maxWeight,tree):
    if maxWeight[vertex1] == -1:
        if len(tree[vertex1].children) == 1 and 0!=vertex1:
            maxWeight[vertex1] = tree[vertex1].weight 
        else:
            m = tree[vertex1].weight
            for i in tree[vertex1].children:
                if i!= parent:
                    for j in tree[i].children:
                        if j!=vertex1:
                            m = m + funParty(j,i,maxWeight,tree)
            newm = 0
            for i in tree[vertex1].children:
                if i != parent:
                    newm = newm + funParty(i,vertex1,maxWeight,tree)
            maxWeight[vertex1] = max(m,newm)
    return maxWeight[vertex1]

def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    if size == 0:
        return 0
    maxWeight = [-1]*len(tree)
    #dfs(tree, 0, -1,maxWeight,[0]*len(tree))
    funParty(0,-1,maxWeight,tree)
    #print(maxWeight)
    # You must decide what to return.
    return max(maxWeight)


def main():
    tree = ReadTree();
    weight = MaxWeightIndependentTreeSubset(tree);
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
