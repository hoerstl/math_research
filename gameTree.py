import os
import pickle

"""
This file is a WIP. The idea was to generalize the logic used in Meagans_Tripartite_Graphs.py for all sorts of games.

"""



def getNimValue(board):
    global previousData
    reducedValue = board.reduce()
    dataKey = str(reducedValue)

    # Check if this board has a nim value that has already been calculated
    nimValue = previousData.get(dataKey, None)
    if nimValue is not None:
        return nimValue

    childBoards = []

    for move in board.getAvailableMoves():
        childGraphs.append(removeVertex(reducedValue, vertex))

    for edgeMove in getEdgeMoves(reducedValue):
        childGraphs.append(removeEdge(reducedValue, edgeMove))

    childNimValues = set()

    for graph in childGraphs:
        childNimValues.add(getNimValue(graph))

    childNimValues = list(childNimValues)
    childNimValues.sort()

    for i in range(len(childNimValues)):
        if i != childNimValues[i]:
            previousData[dataKey] = i
            return i

    # add the next highest Nim Value in childNimValue
    previousData[dataKey] = len(childNimValues)
    return len(childNimValues)


def generateTree(board):
    global previousData
    if os.path.exists(board.__class__.saveFile):
        with open(board.__class__.saveFile, "rb") as file:
            previousData = pickle.load(file)
    else:
        previousData = {}

    return getNimValue(board)



if __name__ == '__main__':
    previousData = None










