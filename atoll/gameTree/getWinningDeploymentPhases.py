import pickle
from simpleNode import Node


def displayChildrenInformation(node):
    print(f"Here are options for P{node.value.playerToMove} to move on {node.value.board}:")
    for i, child in enumerate(node.children):
        print("*" * (node.isBiological[i] == "0"), end="")
        print(f"{i}.\t", child.value, end="  " if child.playerWhoWins == 1 else "  \t")
        print(f"P{child.playerWhoWins} will win")


with open('atollTree.pickle', 'rb') as file:
    root = pickle.load(file)

playerWhoWins = root.playerWhoWins
print(f"P{playerWhoWins} wins on an atoll of size {len(root.value.board)}")


def getAllWinningDeploymentPhases(node):
    if not node.value.inDeploymentPhase and node.playerWhoWins == playerWhoWins:
        return (node.value.canonicalForm,)
    
    if node.playerWhoWins != playerWhoWins:
        return tuple()
    
    res = []
    for i, child in enumerate(node.children):
        if node.isBiological[i]:
            res += [*getAllWinningDeploymentPhases(child)]
    return tuple(res)
    
allWinningDeploymentPhases = getAllWinningDeploymentPhases(root)
uniqueWinningDeploymentPhases = list(set(allWinningDeploymentPhases))
uniqueWinningDeploymentPhases.sort()
uniqueWinningDeploymentPhases.sort(key=lambda e: e[-2:])
print(len(uniqueWinningDeploymentPhases))
print(uniqueWinningDeploymentPhases)

P1MoveFirstCount = 0
P2MoveFirstCount = 0
OtherCount = 0
for board in uniqueWinningDeploymentPhases:
    if board[-2:] == "11":
        P1MoveFirstCount += 1
    elif board[-2:] == "22":
        P2MoveFirstCount += 1
    else:
        OtherCount += 1

print(f"{P1MoveFirstCount=}\n{P2MoveFirstCount=}\n{OtherCount=}\n")
        







