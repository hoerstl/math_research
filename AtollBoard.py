import random


# https://py2.codeskulptor.org/#user50_bK7Eg8ebJv_1.py


class AtollBoard:
    def __init__(self, size):
        n = size
        board = [i for i in range(n)]
        self.board = []

        remainingSpaces = board[:]
        if len(remainingSpaces) == 2:
            p1SpaceCount = 1
        else:
            p1SpaceCount = random.choice(range(len(remainingSpaces) - 2)) + 1
        p1Spaces = random.sample(remainingSpaces, p1SpaceCount)
        p1Distribution = self.randompartition(n, p1SpaceCount)
        for i in range(len(p1Spaces)):
            self.board.append((p1Spaces[i], p1Distribution[i], "L"))
            remainingSpaces.remove(p1Spaces[i])

        if len(remainingSpaces) == 1:
            p2SpaceCount = 1
        else:
            p2SpaceCount = random.choice(range(len(remainingSpaces) - 1)) + 1
        p2Spaces = random.sample(remainingSpaces, p2SpaceCount)
        p2Distribution = self.randompartition(n, p2SpaceCount)
        for i in range(len(p2Spaces)):
            self.board.append((p2Spaces[i], p2Distribution[i], "R"))
            remainingSpaces.remove(p2Spaces[i])

        for i in range(len(remainingSpaces)):
            self.board.append((remainingSpaces[i], 0, "N/A"))

        self.board.sort(key=self.getfirstindex)
        for i in range(len(self.board)):
            self.board[i] = self.board[i][1:]



        # print(self.board)
        if p1SpaceCount > p2SpaceCount:
            # print("Right Starts")
            self.startingPlayer = "R"
        elif p1SpaceCount == p2SpaceCount:
            # print("Left Starts")
            self.startingPlayer = "L"
        elif p1SpaceCount < p2SpaceCount:
            # print("Left Starts")
            self.startingPlayer = "L"
        else:
            raise RuntimeError("Somehow there are more than 3 comparisons between two fixed integers!")

    def randompartition(self, n, k):
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


    def generateCode(self, playerPerspective):
        code = ""
        for space_ in range(len(self.board)):
            lspace = self.getSpace(space_, -1)
            thisSpace = self.getSpace(space_, 0)
            rspace = self.getSpace(space_, 1)

            if thisSpace[1] == "N/A":
                continue

            # Generate the space's current threat level
            aggressionScore = 0
            if lspace[1] != thisSpace[1]:
                aggressionScore += lspace[0]
            if rspace[1] != thisSpace[1] and rspace is not lspace:
                aggressionScore += rspace[0]
            # See if the space can be aggressed upon
            if aggressionScore > thisSpace[0]:
                if playerPerspective == thisSpace[1]:
                    code += "D"
                else:
                    code += "T"
            else:
                if playerPerspective == thisSpace[1]:
                    code += "S"
                else:
                    code += "P"


            # Check its relationship to the right neighbor
            if rspace[1] == "N/A" or rspace[1] == thisSpace[1]:
                code += "|"

            elif thisSpace[1] != rspace[1]:
                if thisSpace[1] == playerPerspective:
                    if thisSpace[0] > rspace[0]:
                        code += "⬆"
                    elif thisSpace[0] < rspace[0]:
                        code += "⬇"
                    else:
                        code += "="
                else:
                    if rspace[0] > thisSpace[0]:
                        code += "⬆"
                    elif rspace[0] < thisSpace[0]:
                        code += "⬇"
                    else:
                        code += "="

        return code



    def getSpace(self, start, offset):
        return self.board[(start + offset) % len(self.board)]


    def getfirstindex(self, obj):
        return obj[0]





if __name__ == '__main__':
    n = int(input("Please enter the size of the atoll: "))




