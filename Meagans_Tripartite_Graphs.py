import math

import numpy as np
import oapackage
import pickle


def getTripartiteEdges(vertexCount, firstCount, secondCount, thirdCount):
    if firstCount + secondCount + thirdCount != vertexCount:
        print(f"Unfortunately, {firstCount} + {secondCount} + {thirdCount} is not equal to {vertexCount}. Try again! ○|￣|_")
        raise RuntimeError("Inconsistent number of verticies given to tripartite edges.")

    first = list(range(firstCount))
    second = list(range(firstCount, firstCount + secondCount))
    third = list(range(firstCount + secondCount, firstCount + secondCount + thirdCount))
    edges = []
    # Connect first verticies to all in the second and third partitions
    for startVertex in first:
        for endVertex in second:
            edges.append((startVertex, endVertex))
        for endVertex in third:
            edges.append((startVertex, endVertex))
    # Connect second vertices to all in the third partition
    for startVertex in second:
        for endVertex in third:
            edges.append((startVertex, endVertex))

    return edges


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
    newgraph = original.copy()
    newgraph[edge[0], edge[1]] = 0
    newgraph[edge[1], edge[0]] = 0
    return newgraph


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
    global graphs
    reduced = reduce(original)
    graphKey = str(reduced)
    nimValue = graphs.get(graphKey, None)

    if nimValue is not None:
        return nimValue



    childGraphs = []

    for vertex in getVertexMoves(reduced):
        childGraphs.append(removeVertex(reduced, vertex))

    for edgeMove in getEdgeMoves(reduced):
        childGraphs.append(removeEdge(reduced, edgeMove))

    childNimValues = set()

    for graph in childGraphs:
        childNimValues.add(getNimValue(graph))

    childNimValues = list(childNimValues)
    childNimValues.sort()

    for i in range(len(childNimValues)):
        if i != childNimValues[i]:
            graphs[graphKey] = i
            return i

    # add the next highest Nim Value in childNimValue
    graphs[graphKey] = len(childNimValues)
    return len(childNimValues)

"""
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
# graph2_reduced = reduce(graph2)

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
"""

def main():
    global graphs
    while True:
        size = int(input("How many vertices does the graph have: "))
        if size < 0:
            quit()
        edges = input("What are the edges? (e.x. 1,2;3,4;5,6; or 'complete'): ")

        if edges == "complete":
            print("Ahhh, I see you're looking for a complete tripartite graph (ง •_•)ง")
            first = int(input("How many verticies in the first partition: "))
            second = int(input("How many verticies in the second partition: "))
            third = int(input("How many verticies in the third partition: "))
            ordered_edges = getTripartiteEdges(size, first, second, third)
            break


        num_edges = math.ceil(len(edges) / 4)
        ordered_edges = []

        edgeError = None
        for edge_number in range(num_edges):
            first_num = int(edges[4 * edge_number])
            second_num = int(edges[4 * edge_number + 2])
            if first_num >= size:
                edgeError = f"User error, {first_num} is not in the acceptable range of labels from 0 to {size - 1}. Try again!"
            if second_num >= size:
                edgeError = f"User error, {second_num} is not in the acceptable range of labels from 0 to {size - 1}. Try again!"
            ordered_edges.append((first_num, second_num))
        if edgeError is None:
            break
        print(edgeError)

    graph = np.zeros((size, size), dtype=int)
    graph = attachEdges(graph, ordered_edges)

    refreshFile = False
    if refreshFile:
        graphs = {}
    else:
        with open("graphs.dict", "rb") as file:
            graphs = pickle.load(file)

    print(f"The nim value of \n{graph} \nis {getNimValue(graph)}")

    # graph2 : 7  2,4,4,5,4,6,5,0,6,0,0,1,1,3

    with open("graphs.dict", "wb") as file:
        pickle.dump(graphs, file)

if __name__ == '__main__':
    graphs = None
    while True:
        try:
            main()
        except RuntimeError:
            print("You probably entered a letter where you wanted a number or you didn't type in the edges right. Try again!")


