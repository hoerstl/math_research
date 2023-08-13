import pickle
from simpleNode import Node


with open('atollTree.pickle', 'rb') as file:
    root = pickle.load(file)

print(f"P{root.playerWhoWins} wins on an atoll of size {len(root.value.board)}")
print("Possible first Moves:")
for i, child in enumerate(root.children): # 3
    print(child.value)
    print(child.children)
    print(child.playerWhoWins)




