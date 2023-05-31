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



size = 7
graph1 = np.zeros((size, size), dtype=int)
edges1 = [(0, 1), (1, 2), (1, 4), (2, 3), (4, 3), (3, 5), (5, 6), (2, 6)]
graph1 = attachEdges(graph1, edges1)

graph1_reduced = reduce(graph1)

print("input graph: ")
print(graph1)

print("reduced graph: ")
print(graph1_reduced)



graph2 = np.zeros((size, size), dtype=int)
edges2 = [(2, 4), (4, 5), (4, 6), (5, 0), (6, 0), (0, 1), (1, 3), (2, 6)]
graph2 = attachEdges(graph2, edges2)

graph2_reduced = reduce(graph2)

print("input graph: ")
print(graph2)

print("reduced graph: ")
print(graph2_reduced)


if len(edges1) != len(edges2):
    print("There was a keying error")

if np.all(graph1_reduced == graph2_reduced):
    print("The graphs are isomorphic!")
else:
    print("These graphs are not isomorphic.")





