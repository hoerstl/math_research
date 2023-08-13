


class AtollBoard:
    """
    This class is meant to simulate the behavior of a game of Aggression on an atoll.
    To store the parentBoard in memory, all of player 1's armies will be represented with the positive integers while
    player 2's armies will be represented with the negative integers. The logic that follows assumes this is true.
    """
    def __init__(self, size, playerToMove=1):
        self.board = [0 for i in range(size)]
        self.size = size

        self.p1UsedArmies = 0
        self.p2UsedArmies = 0
        self.playerToMove = playerToMove
        self.firstToAttack = None
        self.inDeploymentPhase = True
        self.skipCount = 0


    def getAvaialbleMoves(self):  # TODO: Make it so that the last deployment action always places the remaining armies of either player
        """
        Returns the Moves available to the player currently taking their playerToMove.
        :return:
        """
        if self.playerToMove == 1:
            return self.getP1AvailableMoves()
        else:
            return self.getP2AvailableMoves()


    def getP1AvailableMoves(self):
        """
        This function gets the moves that are available to P1 at the current phase of the game. If it's the deployment
        phase, tuples contianing the index of an empty space and the number of armies to deploy there are returned.
        If it's the aggression phase, the indexes of vulnerable P2 spaces are returned
        :return:
        """
        if self.inDeploymentPhase:
            availableArmies = self.size - self.p1UsedArmies
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
            availableArmies = self.size - self.p2UsedArmies
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


    def tryToSkipTurn(self):
        if self.skipCount == 2:
            return False
        else:
            self.playerToMove ^= 3
            self.skipCount += 1
            return True


    def deploy(self, index, armyCount):
        if self.playerToMove == 1:
            self.p1Deploy(index, armyCount)
        else:
            self.p2Deploy(index, armyCount)
        self.playerToMove ^= 3
        self.checkDeploymentPhaseComplete()
        self.skipCount = 0


    def p1Deploy(self, index, armyCount):
        assert self.inDeploymentPhase
        assert armyCount > 0
        assert self.board[index] == 0
        self.board[index] = armyCount
        self.p1UsedArmies += armyCount
        if self.firstToAttack is None and self.p1UsedArmies == self.size:
            self.firstToAttack = 1


    def p2Deploy(self, index, armyCount):
        assert self.inDeploymentPhase
        assert armyCount < 0
        assert self.board[index] == 0
        self.board[index] = armyCount
        self.p2UsedArmies += abs(armyCount)
        if self.firstToAttack is None and self.p2UsedArmies == self.size:
            self.firstToAttack = 2


    def checkDeploymentPhaseComplete(self):
        boardIsFull = 0 not in self.board
        playersOutOfArmies = self.p1UsedArmies == self.p2UsedArmies and self.p2UsedArmies == self.size
        if boardIsFull or playersOutOfArmies:
            self.inDeploymentPhase = False
            self.playerToMove = self.firstToAttack if self.firstToAttack else 1


    def attack(self, index):
        if self.playerToMove == 1:
            self.p1Attack(index)
        else:
            self.p2Attack(index)
        self.playerToMove ^= 3
        self.skipCount = 0


    def p1Attack(self, index):
        assert not self.inDeploymentPhase
        assert self.board[index] < 0
        self.board[index] = 0


    def p2Attack(self, index):
        assert not self.inDeploymentPhase
        assert self.board[index] > 0
        self.board[index] = 0


    def getCounterClockwiseValue(self, index):
        return self.board[(index-1)%len(self.board)]

    def getClockwiseValue(self, index):
        return self.board[(index+1)%len(self.board)] if self.size != 2 else 0


    def __str__(self):
        return f"P{self.playerToMove} to move, inDeployment {self.inDeploymentPhase}: {self.board}"

