from AtollBoard import AtollBoard
from copy import deepcopy
from simpleNode import Node
import pickle
import time

startTime = time.time()
atollSize = 5
root = Node(AtollBoard(atollSize))
incompleteNodes = [root]
while len(incompleteNodes) != 0:
    parent = incompleteNodes.pop(0)
    parentBoard = parent.value
    availableMoves = parentBoard.getAvaialbleMoves()

    if not availableMoves:
        if parentBoard.tryToSkipTurn():
            incompleteNodes.append(parent)
        continue

    for move in availableMoves:
        newBoard = deepcopy(parentBoard)

        if parentBoard.inDeploymentPhase:
            newBoard.deploy(*move)
        else:
            newBoard.attack(move)

        newNode = Node(newBoard)
        parent.children.append(newNode)
        incompleteNodes.append(newNode)


with open('atollTree.pickle', 'wb') as file:
    pickle.dump(root, file)

endTime = time.time()
print(f"Finished in {endTime - startTime} seconds.")

print(f"Player {root.playerWhoWins} wins on an atoll of size {atollSize}.")
print('\n\n')

print("Possible first Moves:")
for i, child in enumerate(root.children):
    print(child.value)
    print(child.children)
    print(child.playerWhoWins)



