from AtollBoard import AtollBoard
from copy import deepcopy
from simpleNode import Node
import pickle
import time

seenBoards = {} # "canonicalBoardForm": Node
startTime = time.time()
atollSize = 9
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

        # Convert the newBoard to its canonical form and check if we've seen it yet. If we have, use that node instead
        canonicalForm = newBoard.canonicalForm
        cachedNode = seenBoards.get(canonicalForm)
        if cachedNode:
            node = cachedNode
            parent.isBiological += "0"
        else:
            node = Node(newBoard)
            incompleteNodes.append(node)
            parent.isBiological += "1"
        
        parent.children.append(node)
        seenBoards[canonicalForm] = node


with open('atollTree.pickle', 'wb') as file:
    pickle.dump(root, file)

endTime = time.time()
print(f"Finished in {endTime - startTime} seconds.")

print(f"Player {root.playerWhoWins} wins on an atoll of size {atollSize}.")
print('\n\n')



