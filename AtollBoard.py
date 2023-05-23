import random


# https://py2.codeskulptor.org/#user50_bK7Eg8ebJv_1.py

def randompartition(n, k):
    result = [1 for i in range(k)]
    choose = n - k
    j = 0
    while choose != 0 and j < k:
        p = random.choice(range(choose + 1))
        choose -= p
        result[j] += p
        j += 1
    result[k - 1] += choose
    return result


def getfirstindex(object):
    return object[0]


def createBoard(size):
    n = size
    board = [i for i in range(n)]
    finalBoard = []

    remainingSpaces = board[:]
    p1SpaceCount = random.choice(range(len(remainingSpaces) - 2)) + 1
    p1Spaces = random.sample(remainingSpaces, p1SpaceCount)
    p1Distribution = randompartition(n, p1SpaceCount)
    for i in range(len(p1Spaces)):
        finalBoard.append((p1Spaces[i], p1Distribution[i], "L"))
        remainingSpaces.remove(p1Spaces[i])

    if len(remainingSpaces) == 1:
        p2SpaceCount = 1
    else:
        p2SpaceCount = random.choice(range(len(remainingSpaces) - 1)) + 1
    p2Spaces = random.sample(remainingSpaces, p2SpaceCount)
    p2Distribution = randompartition(n, p2SpaceCount)
    for i in range(len(p2Spaces)):
        finalBoard.append((p2Spaces[i], p2Distribution[i], "R"))
        remainingSpaces.remove(p2Spaces[i])

    for i in range(len(remainingSpaces)):
        finalBoard.append((remainingSpaces[i], 0, "N/A"))

    finalBoard.sort(key=getfirstindex)
    for i in range(len(finalBoard)):
        finalBoard[i] = finalBoard[i][1:]

    #print(finalBoard)
    if p1SpaceCount > p2SpaceCount:
        #print("Right Starts")
        startingPlayer = "R"
    elif p1SpaceCount == p2SpaceCount:
        #print("Left Starts")
        startingPlayer = "L"
    elif p1SpaceCount < p2SpaceCount:
        #print("Left Starts")
        startingPlayer = "L"
    else:
        raise RuntimeError("Somehow there are more than 3 comparisons between two fixed integers!")

    return startingPlayer, finalBoard


if __name__ == '__main__':
    n = int(input("Please enter the size of the atoll: "))
    for i in range(10):
        startingPlayer, board = createBoard(n)

        print(startingPlayer + " Starts")
        print(board)




