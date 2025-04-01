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

print(f"P{root.playerWhoWins} wins on an atoll of size {len(root.value.board)}")

targetNode = root
response = ""
parents = []  # Stack
while response != "quit":
    print("*"*500)
    response = input("Type the index of a child, 'display', 'back', or 'quit': ")
    if response.isnumeric():
        targetIndex = int(response)
        if targetIndex >= len(targetNode.children):
            print(f"Failed, this node only has {len(targetNode.children)} children.")
            continue
        print("Swapping nodes...")
        parents.append(targetNode)
        targetNode = targetNode.children[targetIndex]
        displayChildrenInformation(targetNode)

    elif 'display'.startswith(response):
        print("Showing information for the current board...")
        displayChildrenInformation(targetNode)

    elif 'back'.startswith(response):
        if not parents:
            print("You're already looking at the root node.")
            continue
        targetNode = parents.pop()
        #displayChildrenInformation(targetNode)







