import turtle
from AtollBoard import *



def getNewSize():
    global islandNumber, root
    num = root.textinput("Islands?", "How many islands do you want to play on?")
    backup = islandNumber
    try:
        islandNumber = max(2, int(num))

    except ValueError as e:
        islandNumber = backup
    root.listen()

def drawNewBoard():
    global islandNumber, t, root, releaseMode
    if islandNumber == 0:
        return
    #print(islandNumber)
    newboard = AtollBoard(islandNumber)
    code = newboard.generateCode(newboard.startingPlayer)

    if not releaseMode:
        print(newboard.board)

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
        if newboard.board[i][1] == "L":
            t.color("blue")
        elif newboard.board[i][1] == "R":
            t.color("red")
        else:
            t.color("white")
        t.write(newboard.board[i][0], align="center", font=('Arial', 30, 'normal'))
        t.circle(-rmid, extent=rotationDelta)


    t.penup()
    t.goto(500, -100)
    if newboard.startingPlayer == "L":
        t.color("blue")
    elif newboard.startingPlayer == "R":
        t.color("red")
    else:
        raise RuntimeError("Weird starting Player")
    t.write(newboard.startingPlayer + " to Start", align="center", font=('Arial', 40, 'normal'))
    t.goto(0, 0)
    t.write(code, align="center", font=('Arial', 20, 'normal'))










if __name__ == '__main__':
    releaseMode = True
    root = turtle.Screen()
    t = turtle.Turtle()
    if releaseMode:
        t.hideturtle()
    t.speed(0)
    islandNumber = 2
    root.onkeypress(drawNewBoard, "space")
    root.onkeypress(getNewSize, "s")
    root.listen()
    root.mainloop()










