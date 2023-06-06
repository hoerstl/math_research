import math
import pickle
import turtle
from AtollBoard import *
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
    global currentBoard, islandNumber
    if currentBoard.generateCode(currentBoard.currentPlayer).find("T") == -1:
        currentBoard.flipTurn()
        drawCurrentBoard()
        return True
    return False

def clicked(x, y):
    if currentBoard is None:
        return
    if skipTurn():
        return
    angle = getAngle(x, y)
    indexToRemove = getClickedIndex(angle)
    removeFromBoard(indexToRemove)


def getAngle(x, y):
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
            drawCurrentBoard()
    else:
        createNewBoard()



def createNewBoard():
    global islandNumber, t, root, releaseMode, logicinprogress, currentBoard, initiallyGeneratedCode
    interestingCode = r"T[^|]D[^⬇]|[^⬇]D[^|]T"
    currentBoard = AtollBoard(islandNumber)
    currentBoardCode = currentBoard.generateCode("L")
    while not re.match(interestingCode, currentBoardCode):
        currentBoard = AtollBoard(islandNumber)
        currentBoardCode = currentBoard.generateCode("L")
    initiallyGeneratedCode = currentBoardCode
    drawCurrentBoard()

def drawCurrentBoard():
    global islandNumber, t, root, releaseMode, logicinprogress, currentBoard, p1mode
    if islandNumber == 0 or logicinprogress:
        return
    logicinprogress = True
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

    logicinprogress = False



def deemLeftWin():
    global initiallyGeneratedCode
    filename = "leftwins.save"
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
    filename = "rightwins.save"
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
    filename = "ties.save"
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
    if os.path.exists("leftwins.save"):
        with open("leftwins.save", "rb") as file:
            leftwins = pickle.load(file)
    else:
        leftwins = []

    print("Here are the boards where left wins:")
    for winningCode in leftwins:
        print(winningCode)

    if os.path.exists("rightwins.save"):
        with open("rightwins.save", "rb") as file:
            rightwins = pickle.load(file)
    else:
        rightwins = []

    print("Here are the boards where right wins:")
    for winningCode in rightwins:
        print(winningCode)

    if os.path.exists("ties.save"):
        with open("ties.save", "rb") as file:
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
        with open("rightwins.save", "wb") as file:
            pickle.dump([], file)
        with open("leftwins.save", "wb") as file:
            pickle.dump([], file)


if __name__ == '__main__':
    """Please note that all codes in the leftwins.save and rightwins.save are generated from left's perspective"""
    releaseMode = True
    p1mode = True
    logicinprogress = False
    currentBoard = None
    initiallyGeneratedCode = None
    root = turtle.Screen()
    t = turtle.Turtle()
    if releaseMode:
        t.hideturtle()
    t.speed(0)
    islandNumber = 10
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










