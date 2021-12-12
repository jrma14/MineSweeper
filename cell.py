class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.flagged = False
        self.bomb = False
        self.nearbyBombs = 0
