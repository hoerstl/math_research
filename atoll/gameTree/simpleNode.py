

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.isBiological = ""
        self.cachedPlayerWhoWins = None  # Can have the value 1, or 2

    @property
    def playerWhoWins(self):
        if self.cachedPlayerWhoWins:
            return self.cachedPlayerWhoWins

        if not self.children:  # Then the game is over
            self.calculateBaseCaseWhoWins()
            return self.cachedPlayerWhoWins

        playerCanForceAWin = False
        for child in self.children:
            if self.value.playerToMove == child.playerWhoWins:  # If the player to move can move to a board where they win
                playerCanForceAWin = True
        self.cachedPlayerWhoWins = self.value.playerToMove if playerCanForceAWin else self.value.playerToMove ^ 3
        return self.cachedPlayerWhoWins


    def calculateBaseCaseWhoWins(self):
        p1ControlledRegions = [armyValue for armyValue in self.value.board if armyValue > 0]
        p2ControlledRegions = [armyValue for armyValue in self.value.board if armyValue < 0]
        p1RegionCount = len(p1ControlledRegions)
        p2RegionCount = len(p2ControlledRegions)
        if p1RegionCount > p2RegionCount:
            self.cachedPlayerWhoWins = 1
            return
        elif p1RegionCount < p2RegionCount:
            self.cachedPlayerWhoWins = 2
            return

        # Break the tie
        p1Armies = abs(sum(p1ControlledRegions))
        p2Armies = abs(sum(p2ControlledRegions))
        if p1Armies > p2Armies:
            self.cachedPlayerWhoWins = 1
        elif p1Armies < p2Armies:
            self.cachedPlayerWhoWins = 2
        else:
            self.cachedPlayerWhoWins = self.value.firstToAttack  # Default Winner when tied for land and forces


    def __str__(self):
        return str(self.value)

