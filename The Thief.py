from Meagans_Tripartite_Graphs import *

def getNimValue(original):
    global graphs
    reduced = reduce(original)
    graphKey = str(reduced)
    nimValue = graphs.get(graphKey, None)

    if nimValue is not None:
        return nimValue

    #
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


def getNextGraph(original):
    global graphs
    #reduced = reduce(original)
    childGraphs = []

    for vertex in getVertexMoves(original):
        childGraphs.append(removeVertex(original, vertex))

    for edgeMove in getEdgeMoves(original):
        childGraphs.append(removeEdge(original, edgeMove))

    childNimValues = []

    for graph in childGraphs:
        childNimValues.append(getNimValue(graph))

    for index, nimValue in enumerate(childNimValues):
        if nimValue == 0:
            return childGraphs[index]
    return "You're screwed"


if __name__ == '__main__':
    global graphs
    while True:
        size = int(input("How many vertices does the graph have: "))
        if size < 0:
            quit()
        edges = input("What are the edges? (e.x. 1,2;3,4;5,6;): ")

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

    print(f"Move from \n{graph}")
    print(f"Play to \n{getNextGraph(graph)}")


