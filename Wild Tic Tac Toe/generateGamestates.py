import pickle
import copy
import queue




def getAvailablePositions(board):
    availablePositions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "":
                availablePositions.append((i, j))
    return availablePositions


def expand(node):
    emptyPositions = getAvailablePositions(node.value)

    newchildren = []
    for position in emptyPositions:
        row = position[0]
        col = position[1]
        # Make O move in that position
        newboardO = copy.deepcopy(node.value)  # copy the board
        newboardO[row][col] = 'O'  # place an O there
        OChild = Node(newboardO, node, (row, col))  # Make a node for the new board
        newchildren.append(OChild)  # Append it to the list of children

        # Make X move in that position
        newboardX = copy.deepcopy(node.value)  # copy the board
        newboardX[row][col] = 'X'  # place an X there
        XChild = Node(newboardX, node, (row, col))  # Make a node for the new board
        newchildren.append(XChild)  # Append it to the list of children
    node.children = copy.copy(newchildren)
    return newchildren

def checkWinning(node):
    global boardwidth, boardheight
    board = node.value
    ir = node.recentChange[0]  # initial row
    ic = node.recentChange[1]  # initial column
    initialShape = board[ir][ic]
    if initialShape == "":
        if node.parent is not None:
            raise RuntimeError(f"Most recently placed piece on board at {node.recentChange} has not been placed:\n{node.value} ")
        return False

    # Check for horizontal wins
    count = 0
    for col in range(boardwidth):
        count += 1 if board[ir][col] == initialShape else 0
    if count == boardwidth:
        return True

    # Check for vertical wins
    count = 0
    for row in range(boardheight):
        count += 1 if board[row][ic] == initialShape else 0
    if count == boardheight:
        return True


    # Check main diagonal wins
    if ir == ic and boardwidth == boardheight:
        count = 0
        for i in range(boardwidth):
            count += 1 if board[i][i] == initialShape else 0
        if count == boardwidth:
            return True


    # Check anti diagonal wins
    if ir == boardheight-1-ic and boardwidth == boardheight:
        count = 0
        for i in range(boardwidth):
            count += 1 if board[boardheight-1-i][i] == initialShape else 0
        if count == boardwidth:
            return True

    # There have been no wins so return False
    return False




def checkFull(node):
    full = True
    for i in range(len(node.value)):
        for j in range(len(node.value[i])):
            if node.value[i][j] == "":
                full = False

    return full




class Node:

    def __init__(self, gamestate, parent, newPos):
        self.children = []
        self.parent = parent
        self.value = gamestate
        if parent is None:
            self.movesMade = 0
            self.previousPlayer = 2
        else:
            self.movesMade = parent.movesMade + 1
            self.previousPlayer = 1 if self.movesMade % 2 == 1 else 2
        self.ending = None
        self.recentChange = newPos

    def __str__(self):
        string = ""
        for row in self.value:
            string += str(row) + "\n"
        return string


boardsize = 3
boardwidth = boardsize
boardheight = boardsize
if __name__ == '__main__':
    # An 'X' is an X and an 'O' is an O. An empty string is used to mark an empty space
    startingBoard = [["" for j in range(boardsize)] for i in range(boardsize)]
    root = Node(startingBoard, None, (0, 0))

    startingNode = root
    winningNodes = []
    tiedNodes = []
    nodesToExpand = queue.Queue()
    nodesToExpand.put(root)
    while nodesToExpand.qsize() != 0:
        nextNode = nodesToExpand.get()
        if checkWinning(nextNode):
            nextNode.ending = "Win"
            winningNodes.append(nextNode)
        elif checkFull(nextNode):
            nextNode.ending = "Tie"
            tiedNodes.append(nextNode)
        else:
            newToExpand = expand(nextNode)
            for node in newToExpand:
                nodesToExpand.put(node)


    # n = 1
    # for child in root.children:
    #     print(f"Starting move {n}")
    #     print(child)
    #     n += 1

    for node in winningNodes:
        print(f"Winning Board for P{node.previousPlayer}:")
        print(node)

