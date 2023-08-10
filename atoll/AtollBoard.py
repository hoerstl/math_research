


class AtollBoard:
    """
    This class is meant to simulate the behavior of a game of Aggression on an atoll.
    To store the board in memory, all of player 1's armies will be represented with the positive integers while
    player 2's armies will be represented with the negative integers. The logic that follows assumes this is true.
    """
    def __init__(self, size):
        self.board = [0 for i in range(size)]
        self.size = size
        self.turn = 1
        self.inDeploymentPhase = True


    def getP1AvailableMoves(self):
        """
        This function gets the moves that are available to P1 at the current phase of the game. If it's the deployment
        phase, tuples contianing the index of an empty space and the number of armies to deploy there are returned.
        If it's the aggression phase, the indexes of vulnerable P2 spaces are returned
        :return:
        """
        if self.inDeploymentPhase:
            usedArmies = sum([p1Armies for p1Armies in self.board if p1Armies > 0])
            availableArmies = self.size - usedArmies
            deploymentOptions = []
            for emptySpaceIndex in [i for i in range(self.size) if self.board[i] == 0]:
                for armyOption in range(1, availableArmies+1):
                    deploymentOptions.append((emptySpaceIndex, armyOption))
            return deploymentOptions
        else:
            vulnerableP2Indexes = []
            for p2Space in [i for i in range(self.size) if self.board[i] < 0]:
                attackPower = 0
                left = self.getCounterClockwiseValue(p2Space)
                right = self.getClockwiseValue(p2Space)
                attackPower += left if left > 0 else 0
                attackPower += right if right > 0 else 0
                if abs(attackPower) > abs(self.board[p2Space]):
                    vulnerableP2Indexes.append(p2Space)
            return vulnerableP2Indexes


    def getP2AvailableMoves(self):
        """
        This function gets the moves that are available to P2 at the current phase of the game. If it's the deployment
        phase, tuples contianing the index of an empty space and the number of armies to deploy there are returned.
        If it's the aggression phase, the indexes of vulnerable P1 spaces are returned
        :return:
        """
        if self.inDeploymentPhase:
            usedArmies = sum([p2Armies for p2Armies in self.board if p2Armies < 0])
            availableArmies = self.size - usedArmies
            deploymentOptions = []
            for emptySpaceIndex in [i for i in range(self.size) if self.board[i] == 0]:
                for armyOption in range(1, availableArmies+1):
                    deploymentOptions.append((emptySpaceIndex, -armyOption))
            return deploymentOptions
        else:
            vulnerableP1Indexes = []
            for p1Space in [i for i in range(self.size) if self.board[i] > 0]:
                attackPower = 0
                left = self.getCounterClockwiseValue(p1Space)
                right = self.getClockwiseValue(p1Space)
                attackPower += left if left < 0 else 0
                attackPower += right if right < 0 else 0
                if abs(attackPower) > abs(self.board[p1Space]):
                    vulnerableP1Indexes.append(p1Space)
            return vulnerableP1Indexes


    def p1Deploy(self, index, armyCount):
        assert armyCount > 0
        assert self.board[index] == 0
        self.board[index] = armyCount


    def p2Deploy(self, index, armyCount):
        assert armyCount < 0
        assert self.board[index] == 0
        self.board[index] = armyCount


    def p1Attack(self, index):
        assert self.board[index] < 0
        self.board[index] = 0


    def p2Attack(self, index):
        assert self.board[index] > 0
        self.board[index] = 0


    def getCounterClockwiseValue(self, index):
        return self.board[(index-1)%len(self.board)]

    def getClockwiseValue(self, index):
        return self.board[(index+1)%len(self.board)]

