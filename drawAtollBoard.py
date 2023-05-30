import math
import turtle
from AtollBoard import *
import re



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
    global islandNumber, t, root, releaseMode, logicinp, currentBoard
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
    global islandNumber, t, root, releaseMode, logicinp, currentBoard
    interestingCode = r"T[^|]D[^⬇]|[^⬇]D[^|]T"
    currentBoard = AtollBoard(islandNumber)
    while not re.match(interestingCode, currentBoard.generateCode(currentBoard.currentPlayer)):
        currentBoard = AtollBoard(islandNumber)
    drawCurrentBoard()

def drawCurrentBoard():
    global islandNumber, t, root, releaseMode, logicinp, currentBoard
    if islandNumber == 0 or logicinp:
        return
    logicinp = True
    #print(islandNumber)
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
    t.write(code, align="center", font=('Arial', 20, 'normal'))

    logicinp = False










if __name__ == '__main__':
    releaseMode = True
    logicinp = False
    currentBoard = None
    root = turtle.Screen()
    t = turtle.Turtle()
    if releaseMode:
        t.hideturtle()
    t.speed(0)
    islandNumber = 10
    root.onkeypress(createNewBoard, "space")
    root.onkeypress(drawCurrentBoard, "r")
    root.onkeypress(getNewSize, "s")
    root.onkeypress(skipTurn, "p")
    root.onscreenclick(clicked)
    root.listen()
    root.mainloop()










