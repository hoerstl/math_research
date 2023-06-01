import math

import numpy as np
import oapackage
import pickle




def inverse_permutation(perm):
    inverse = [0] * len(perm)
    for i, p in enumerate(perm):
        inverse[p] = i
    return inverse


def reduce(graph):
    tr = oapackage.reduceGraphNauty(graph, verbose=0)
    tri = inverse_permutation(tr)

    graph_reduced = oapackage.transformGraphMatrix(graph, tri)
    return graph_reduced


def attachEdges(graph, edges: []):
    for edge in edges:
        first = edge[0]
        second = edge[1]
        graph[first, second] = 1
    return np.maximum(graph, graph.T)  # make array symmetric


def removeVertex(original, vertex):
    return np.delete(np.delete(original, vertex, 0), vertex, 1)


def removeEdge(original, edge: (int, int)):
    original[edge[0], edge[1]] = 0
    original[edge[1], edge[0]] = 0
    return original


def getVertexMoves(original):
    return list(range(len(original)))


def getEdgeMoves(original):
    height, width = original.shape
    edges = []
    for row in range(height):
        for col in range(row, width):
            if original[row, col] == 1:
                edges.append((row, col))
    return edges


def getNimValue(original):
    reduced = reduce(original)
    graphKey = str(reduced)
    nimValue = graphs.get(graphKey, None)

    if nimValue is not None:
        return nimValue

    # TODO: Remove this if statement after one run
    if reduced.size == 0:
        graphs[graphKey] = 0
        return 0

    childGraphs = []
    childNimValues = []

    for vertex in getVertexMoves(reduced):
        childGraphs.append(removeVertex(reduced, vertex))

    for edgeMove in getEdgeMoves(reduced):
        childGraphs.append(removeEdge(reduced, edgeMove))

    for graph in childGraphs:
        childNimValues.append(getNimValue(graph))

    childNimValues.sort()

    for i in range(len(childNimValues)):
        if i != childNimValues[i]:
            graphs[graphKey] = i
            return i

    # add the next highest Nim Value in childNimValue
    graphs[graphKey] = len(childNimValues)
    return len(childNimValues)



size = 7
graph1 = np.zeros((size, size), dtype=int)
edges1 = [(0, 1), (1, 2), (1, 4), (2, 3), (4, 3), (3, 5), (5, 6)]
graph1 = attachEdges(graph1, edges1)

graph1_reduced = reduce(graph1).tolist()

print("input graph: ")
print(graph1)

print("reduced graph: ")
print(graph1_reduced)


graph2 = np.zeros((size, size), dtype=int)
edges2 = [(2, 4), (4, 5), (4, 6), (5, 0), (6, 0), (0, 1), (1, 3)]
graph2 = attachEdges(graph2, edges2)

# graph2_reduced = str(reduce(graph2))
graph2_reduced = reduce(graph2)

# 2023-06-01: Testing np.delete()
# graph2_chomp = np.delete(graph2_reduced, 6, 1)
# print(f"CHOMPED GRAPH2 {graph2_chomp}")


print("input graph2: ")
print(graph2)

print("reduced graph2: ")
print(graph2_reduced)

# print(getVertexMoves(graph2_reduced))
# print(getEdgeMoves(graph2_reduced))

# print(f"Removed vertex 2 {removeVertex(graph2_reduced, 2)}")
# print(f"Removed edge (1,4) {removeEdge(graph2_reduced, (1,4))}")


graph2_reduced = str(graph2_reduced)

if len(edges1) != len(edges2):
    print("There was a keying error")

if graph1_reduced == graph2_reduced:
    print("The graphs are isomorphic!")
else:
    print("These graphs are not isomorphic.")

graphs = {graph2_reduced: 10}

if __name__ == '__main__':
    size = int(input("How many vertices does the graph have: "))
    edges = input("What are the edges? (e.x. 1,2;3,4;5,6;): ")

    num_edges = math.ceil(len(edges)/4)
    ordered_edges = []

    for edge_number in range(num_edges):
        first_num = int(edges[4*edge_number])
        second_num = int(edges[4*edge_number+2])

        ordered_edges.append((first_num, second_num))

    graph = np.zeros((size, size), dtype=int)
    graph = attachEdges(graph, ordered_edges)
    graph = str(reduce(graph))

    if graphs.get(graph, False):
        print(graphs[graph])
    else:
        print("Sorry bro!")

    print(graph)

    # vertex = int(input("What vertex to we remove: "))
    # edge = input("What edge do we remove: ")



    # graph2 : 7  2,4,4,5,4,6,5,0,6,0,0,1,1,3






