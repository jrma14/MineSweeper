import random
import cell


class Board:
    board = [[]]
    width = None
    height = None
    numBombs = None
    cellsLeft = -1
    flags = 0

    def __init__(self, x, y, bombs):
        self.width = x
        self.height = y
        self.flags = bombs
        self.cellsLeft = self.width * self.height - bombs
        self.numBombs = bombs
        self.board = [[cell.cell(i, j) for i in range(self.width)] for j in range(self.height)]
        self.__placeBombs()
        self.__generateBoard()

    def __getNearbyBombs(self, x, y):
        nearbyBombs = 0
        if y == 0 or y == self.height - 1:
            if x == 0 or x == self.width - 1:
                xInc = 1 if y == 0 else -1
                yInc = 1 if x == 0 else -1
                nearbyBombs = nearbyBombs + 1 if self.board[y + xInc][x].bomb else nearbyBombs
                nearbyBombs = nearbyBombs + 1 if self.board[y][x + yInc].bomb else nearbyBombs
                nearbyBombs = nearbyBombs + 1 if self.board[y + xInc][x + yInc].bomb else nearbyBombs
                self.board[y][x].nearbyBombs = nearbyBombs
                return
            for i in range(-1, 2):
                nearbyBombs = nearbyBombs + 1 if self.board[y + 1 if y == 0 else y - 1][x + i].bomb else nearbyBombs
            nearbyBombs = nearbyBombs + 1 if self.board[y][x - 1].bomb else nearbyBombs
            nearbyBombs = nearbyBombs + 1 if self.board[y][x + 1].bomb else nearbyBombs
            self.board[y][x].nearbyBombs = nearbyBombs
            return
        if x == 0 or x == self.width - 1:
            for i in range(-1, 2):
                nearbyBombs = nearbyBombs + 1 if self.board[y + i][x + 1 if x == 0 else x - 1].bomb else nearbyBombs
            nearbyBombs = nearbyBombs + 1 if self.board[y - 1][x].bomb else nearbyBombs
            nearbyBombs = nearbyBombs + 1 if self.board[y + 1][x].bomb else nearbyBombs
            self.board[y][x].nearbyBombs = nearbyBombs
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                nearbyBombs = nearbyBombs + 1 if self.board[y + i][x + j].bomb else nearbyBombs
        self.board[y][x].nearbyBombs = nearbyBombs
        return

    def __placeBombs(self):
        for i in range(self.numBombs):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while self.board[y][x].bomb:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
            self.board[y][x].bomb = True
            self.board[y][x].nearbyBombs = -1

    def __generateBoard(self):
        for i in range(self.height):
            for j in range(self.width):
                if not self.board[i][j].bomb:
                    self.__getNearbyBombs(j, i)

    def randomizeBoard(self, x, y, b):
        self.__init__(x, y, b)

    def revealAround(self, currCell, queue, visited):
        x = currCell.x
        y = currCell.y
        xInc = [0, 0, 1, -1, 1, 1, -1, -1]
        yInc = [1, -1, 0, 0, 1, -1, 1, -1]
        for i in range(8):
            newX = x + xInc[i]
            newY = y + yInc[i]
            if 0 <= newY < self.height and 0 <= newX < self.width:
                c = self.board[newY][newX]
                if c not in visited:
                    visited.append(c)
                    if c.nearbyBombs == 0:
                        queue.append(c)
                    self.flags += 1 if c.flagged else 0
                    c.revealed = True
                    self.cellsLeft -= 1

    def checkWin(self):
        return self.cellsLeft == 0

    def revealZeros(self, x, y):
        if self.board[y][x].nearbyBombs == 0:
            queue = [self.board[y][x]]
            visited = [self.board[y][x]]
            while len(queue) > 0:
                currCell = queue.pop(0)
                self.revealAround(currCell, queue, visited)
