from AtollBoard import AtollBoard
from copy import deepcopy
import pickle


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.nimValue = None


root = Node(AtollBoard(2))
leafNodes = [root]
while len(leafNodes) != 0:
    parent = leafNodes.pop(0)
    parentBoard = parent.value
    availableMoves = parentBoard.getAvaialbleMoves()

    for move in availableMoves:
        newBoard = deepcopy(parentBoard)

        if parentBoard.inDeploymentPhase:
            newBoard.deploy(*move)
        else:
            newBoard.attack(move)

        newNode = Node(newBoard)
        parent.children.append(newNode)
        leafNodes.append(newNode)

with open('atollTree.pickle', 'wb') as file:
    pickle.dump(root, file)

print("Possible first Moves:")
for child in root.children[0].children:
    print(child.value)


