import math
import pickle
import turtle
from atoll.ResearchAtollBoard import *
import re
import os



def getNewSize():
    global islandNumber, root
    num = root.textinput("Islands?", "How many islands do you want to play on?")
    backup = islandNumber
    try:
        islandNumber = max(2, int(num))

    except ValueError as e:
        islandNumber = backup
    root.listen()


def skipTurn():
    """
    This method skips the current player's turn if they have no moves and the other player does. Draws the board
    on a successful skip.
    :return: True if the current player has no moves and their opponent does
    """
    global currentBoard, islandNumber, finalDrawComplete
    currentBoardCode = currentBoard.generateCode(currentBoard.currentPlayer)  # Get the code for the current board

    if currentBoardCode.find("T") == -1 and currentBoardCode.find("D") != -1:  # If you have no moves and the other player does
        currentBoard.flipTurn()  # Swap the turn
        drawCurrentBoard()
        return True
    if currentBoardCode.find("T") == -1 and currentBoardCode.find("D") == -1:
        if not finalDrawComplete:
            drawCurrentBoard()
            displayWinner()
            finalDrawComplete = True
        return True
    # If the other player has no moves either, we don't bother swapping the turn.
    return False

def clicked(x, y):
    global logicinprogress
    if logicinprogress:
        return
    logicinprogress = True
    if currentBoard is None:
        logicinprogress = False
        return
    if skipTurn():
        logicinprogress = False
        return
    angle = getAngle(x, y)
    indexToRemove = getClickedIndex(angle)
    removeFromBoard(indexToRemove)
    logicinprogress = False


def getAngle(x, y):
    if x == 0:
        x = .000001
    angle = math.degrees(math.atan(y/x))
    if x <= 0:
        angle += 180
    angle = angle % 360
    return angle


def getClickedIndex(angle):
    global islandNumber, t, root, releaseMode, logicinprogress, currentBoard
    rotationDelta = 360 / islandNumber
    angle -= 90
    angle = angle % 360
    angle = 360 - angle
    return int(angle // rotationDelta)


def removeFromBoard(index):
    global currentBoard
    if currentBoard != None:
        if currentBoard.takeable(index):
            currentBoard.aggress(index)
            if not skipTurn():  # Try to skip the new player's move
                # if you can't, draw the board for the player to move
                drawCurrentBoard()

    else:
        createNewBoard()



def createNewBoard():
    global islandNumber, t, root, releaseMode, logicinprogress, currentBoard, initiallyGeneratedCode, finalDrawComplete, forceInterestingBoard
    finalDrawComplete = False
    interestingCode = r"T[^|]D[^⬇]|[^⬇]D[^|]T" if forceInterestingBoard else ""
    currentBoard = AtollBoard(islandNumber)
    currentBoardCode = currentBoard.generateCode("L")
    while not re.match(interestingCode, currentBoardCode):
        currentBoard = AtollBoard(islandNumber)
        currentBoardCode = currentBoard.generateCode("L")
    initiallyGeneratedCode = currentBoardCode
    drawCurrentBoard()


def displayWinner():
    global t, currentBoard
    currentCode = currentBoard.generateCode("L")
    p1Spaces = 0
    p2Spaces = 0
    for digit in currentCode:
        if digit == "S":
            p1Spaces += 1
        elif digit == "P":
            p2Spaces += 1

    if p1Spaces > p2Spaces:
        text = "P1 win"
        t.color("blue")
    elif p1Spaces == p2Spaces:
        text = "Tie"
        t.color("grey")
    else:
        text = "P2 win"
        t.color("red")

    t.penup()
    t.goto(0, -350)
    t.write(text, align="center", font=('Arial', 30, 'normal'))


def drawCurrentBoard():
    global islandNumber, t, root, releaseMode, logicinprogress, currentBoard, p1mode
    if islandNumber == 0:
        return
    #print(islandNumber)


    if p1mode:
        code = currentBoard.generateCode("L")
    else:
        code = currentBoard.generateCode(currentBoard.currentPlayer)

    if not releaseMode:
        print(currentBoard.board)

    t.reset()
    t.speed(0)
    t.seth(90)
    if releaseMode:
        t.hideturtle()

    rotationDelta = 360 / islandNumber

    r1 = 200
    r2 = 300
    rmid = (r1 + r2) // 2
    for i in range(islandNumber):
        if i == 0:
            t.pensize(2)
        else:
            t.pensize(1)
        t.forward(r2)
        t.backward(r2)
        t.right(rotationDelta)

    t.forward(r2)
    t.seth(0)
    t.circle(-r2)
    t.seth(-90)
    t.forward(r2-r1)
    t.seth(0)
    t.fillcolor("white")
    t.begin_fill()
    t.circle(-r1)
    t.end_fill()
    t.penup()

    t.goto(0, rmid - 20)
    t.circle(-rmid, extent=rotationDelta/2)
    for i in range(islandNumber):
        if currentBoard.board[i][1] == "L":
            t.color("blue")
        elif currentBoard.board[i][1] == "R":
            t.color("red")
        else:
            t.color("white")
        t.write(currentBoard.board[i][0], align="center", font=('Arial', 30, 'normal'))
        t.circle(-rmid, extent=rotationDelta)


    t.penup()
    t.goto(500, -100)
    if currentBoard.currentPlayer == "L":
        t.color("blue")
    elif currentBoard.currentPlayer == "R":
        t.color("red")
    else:
        raise RuntimeError("Weird starting Player")
    t.write(currentBoard.currentPlayer + " to Move", align="center", font=('Arial', 40, 'normal'))
    t.goto(0, 0)
    if p1mode:
        t.color("blue")
    t.write(code, align="center", font=('Arial', 20, 'normal'))




# Functions used to gather data, not useful for game function.
def deemLeftWin():
    global initiallyGeneratedCode
    filename = "../leftwins.save"
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            list = pickle.load(file)
    else:
        list = []
    list.append(initiallyGeneratedCode)
    with open(filename, "wb") as file:
        pickle.dump(list, file)

    createNewBoard()


def deemRightWin():
    global initiallyGeneratedCode
    filename = "../rightwins.save"
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            list = pickle.load(file)
    else:
        list = []
    list.append(initiallyGeneratedCode)
    with open(filename, "wb") as file:
        pickle.dump(list, file)

    createNewBoard()


def deemTie():
    global initiallyGeneratedCode
    filename = "../ties.save"
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            list = pickle.load(file)
    else:
        list = []
    list.append(initiallyGeneratedCode)
    with open(filename, "wb") as file:
        pickle.dump(list, file)

    createNewBoard()


def listData():
    if os.path.exists("../leftwins.save"):
        with open("../leftwins.save", "rb") as file:
            leftwins = pickle.load(file)
    else:
        leftwins = []

    print("Here are the boards where left wins:")
    for winningCode in leftwins:
        print(winningCode)

    if os.path.exists("../rightwins.save"):
        with open("../rightwins.save", "rb") as file:
            rightwins = pickle.load(file)
    else:
        rightwins = []

    print("Here are the boards where right wins:")
    for winningCode in rightwins:
        print(winningCode)

    if os.path.exists("../ties.save"):
        with open("../ties.save", "rb") as file:
            ties = pickle.load(file)
    else:
        ties = []

    print("Here are the boards where both players tie:")
    for winningCode in ties:
        print(winningCode)


def clearData():
    global root
    response = root.textinput("Deletion confirmation", "Are you sure you want to delete all gathered data?")
    root.listen()
    if not len(response) > 0:
        return
    if response.lower()[0] == "y":
        with open("../rightwins.save", "wb") as file:
            pickle.dump([], file)
        with open("../leftwins.save", "wb") as file:
            pickle.dump([], file)
        with open("../ties.save", "wb") as file:
            pickle.dump([], file)


if __name__ == '__main__':
    """Please note that all codes in the leftwins.save and rightwins.save are generated from left's perspective"""
    releaseMode = True
    p1mode = True
    logicinprogress = False
    finalDrawComplete = False
    currentBoard = None
    forceInterestingBoard = False
    initiallyGeneratedCode = None
    root = turtle.Screen()
    t = turtle.Turtle()
    if releaseMode:
        t.hideturtle()
    t.speed(0)
    islandNumber = 15
    root.onkeypress(createNewBoard, "space")
    root.onkeypress(drawCurrentBoard, "d")
    root.onkeypress(getNewSize, "s")
    root.onkeypress(skipTurn, "p")
    root.onkeypress(deemLeftWin, "l")
    root.onkeypress(deemRightWin, "r")
    root.onkeypress(deemTie, "t")
    root.onkeypress(listData, ".")
    root.onkeypress(clearData, "c")
    root.onscreenclick(clicked)
    root.listen()
    root.mainloop()










