import neat.nn
import pygame
import Board
import copy


# implement ai

class game:

    def __init__(self):
        pygame.init()

        self.backgroundColor = (200, 200, 200)

        self.cols = 9
        self.rows = 9
        self.bombs = 12

        self.difficultySettings = {
            'easy': (10, 8, 10),
            'medium': (18, 14, 40),
            'hard': (24, 20, 99),
            'custom': (self.cols, self.rows, self.bombs)
        }

        self.difficulty = 'custom'

        self.width = 700
        self.height = 500
        self.gridSize = (self.width / self.cols, self.height / self.rows)

        self.buttonWidth = 300
        self.buttonHeight = self.height / 6
        self.distBetweenButtons = (self.height - 3 * self.buttonHeight) / 3
        self.center = (self.width / 2, self.height / 2)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        self.icon = pygame.image.load('minesweeper.png')
        pygame.display.set_icon(self.icon)
        self.font = pygame.font.SysFont('rockwellextra', 32)

        self.imageTileOffset = {
            'unopened': (0, 0),
            'flag': (1, 0),
            -1: (2, 0),
            0: (3, 0),
            1: (0, 1),
            2: (1, 1),
            3: (2, 1),
            4: (3, 1),
            5: (0, 2),
            6: (1, 2),
            7: (2, 2),
            8: (3, 2)
        }
        self.tiles = pygame.image.load('minesweeper_tiles.jpg')

        self.board = Board.Board(self.cols, self.rows, self.bombs)

        self.exit = False
        self.running = False
        self.pause = False
        self.endgame = False
        self.settings = False

    def displayBoard(self, board):
        surface = pygame.Surface((128, 128))
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.board[i][j].revealed:
                    offset = self.imageTileOffset[self.board.board[i][j].nearbyBombs]
                elif self.board.board[i][j].flagged:
                    offset = self.imageTileOffset['flag']
                else:
                    offset = self.imageTileOffset['unopened']
                surface.blit(self.tiles, (0, 0), (128 * offset[0], 128 * offset[1], 128, 128))
                scaledSurface = pygame.transform.scale(surface, (self.gridSize[0], self.gridSize[1]))
                self.screen.blit(scaledSurface, (self.gridSize[0] * j, self.gridSize[1] * i))

    def displayMenu(self):
        color = (0, 0, 0)
        self.screen.fill(self.backgroundColor)
        play = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 - (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        settings = pygame.Rect(self.center[0] - self.buttonWidth / 2, self.center[1] - self.buttonHeight / 2,
                               self.buttonWidth, self.buttonHeight)
        exit = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 + (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        pygame.draw.rect(self.screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        playText = self.font.render('Play', True, (255, 0, 0), (255, 255, 255))
        playTextRect = playText.get_rect()
        playTextRect.center = (self.center[0], self.center[1] - (self.buttonHeight + self.distBetweenButtons))
        settingsText = self.font.render('Difficulty', True, (255, 0, 0), (255, 255, 255))
        settingsTextRect = settingsText.get_rect()
        settingsTextRect.center = (self.center[0], self.center[1])
        exitText = self.font.render('Exit', True, (255, 0, 0), (255, 255, 255))
        exitTextRect = exitText.get_rect()
        exitTextRect.center = (self.center[0], self.center[1] + (self.buttonHeight + self.distBetweenButtons))
        self.screen.blit(playText, playTextRect)
        self.screen.blit(settingsText, settingsTextRect)
        self.screen.blit(exitText, exitTextRect)

    def displaySettings(self):
        color = (0, 0, 0)
        self.screen.fill(self.backgroundColor)
        play = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 - (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        settings = pygame.Rect(self.center[0] - self.buttonWidth / 2, self.center[1] - self.buttonHeight / 2,
                               self.buttonWidth, self.buttonHeight)
        exit = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 + (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        pygame.draw.rect(self.screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        playText = self.font.render('Easy', True, (255, 0, 0), (255, 255, 255))
        playTextRect = playText.get_rect()
        playTextRect.center = (self.center[0], self.center[1] - (self.buttonHeight + self.distBetweenButtons))
        settingsText = self.font.render('Medium', True, (255, 0, 0), (255, 255, 255))
        settingsTextRect = settingsText.get_rect()
        settingsTextRect.center = (self.center[0], self.center[1])
        exitText = self.font.render('Hard', True, (255, 0, 0), (255, 255, 255))
        exitTextRect = exitText.get_rect()
        exitTextRect.center = (self.center[0], self.center[1] + (self.buttonHeight + self.distBetweenButtons))
        self.screen.blit(playText, playTextRect)
        self.screen.blit(settingsText, settingsTextRect)
        self.screen.blit(exitText, exitTextRect)

    def displayPause(self):
        color = (0, 0, 0)
        play = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 - (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        settings = pygame.Rect(self.center[0] - self.buttonWidth / 2, self.center[1] - self.buttonHeight / 2,
                               self.buttonWidth, self.buttonHeight)
        exit = pygame.Rect(self.center[0] - self.buttonWidth / 2,
                           self.center[1] - self.buttonHeight / 2 + (self.buttonHeight + self.distBetweenButtons),
                           self.buttonWidth, self.buttonHeight)
        pygame.draw.rect(self.screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        pygame.draw.rect(self.screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                         border_top_right_radius=10, border_bottom_left_radius=10)
        playText = self.font.render('Resume', True, (255, 0, 0), (255, 255, 255))
        playTextRect = playText.get_rect()
        playTextRect.self.center = (self.center[0], self.center[1] - (self.buttonHeight + self.distBetweenButtons))
        settingsText = self.font.render('Restart', True, (255, 0, 0), (255, 255, 255))
        settingsTextRect = settingsText.get_rect()
        settingsTextRect.self.center = (self.center[0], self.center[1])
        exitText = self.font.render('Back To Menu', True, (255, 0, 0), (255, 255, 255))
        exitTextRect = exitText.get_rect()
        exitTextRect.self.center = (self.center[0], self.center[1] + (self.buttonHeight + self.distBetweenButtons))
        self.screen.blit(playText, playTextRect)
        self.screen.blit(settingsText, settingsTextRect)
        self.screen.blit(exitText, exitTextRect)

    def displayEndgame(self, win):
        gameOverText = self.font.render('Game Over', True, (255, 0, 0), (255, 255, 255))
        gameOverTextRect = gameOverText.get_rect()
        gameOverTextRect.center = (self.center[0], self.center[1] - (self.buttonHeight + self.distBetweenButtons))
        winLossText = self.font.render('You Win!' if win else 'You Lose', True, (255, 0, 0), (255, 255, 255))
        winLossTextRect = winLossText.get_rect()
        winLossTextRect.center = (self.center[0], self.center[1])
        exitText = self.font.render('Back To Menu', True, (255, 0, 0), (255, 255, 255))
        exitTextRect = exitText.get_rect()
        exitTextRect.center = (self.center[0], self.center[1] + (self.buttonHeight + self.distBetweenButtons))
        self.screen.blit(gameOverText, gameOverTextRect)
        self.screen.blit(winLossText, winLossTextRect)
        self.screen.blit(exitText, exitTextRect)

    def displayBombs(self, board):
        surface = pygame.Surface((128, 128))
        for i in range(self.board.height):
            for j in range(self.board.width):
                if self.board.board[i][j].revealed:
                    offset = self.imageTileOffset[self.board.board[i][j].nearbyBombs]
                elif self.board.board[i][j].flagged:
                    offset = self.imageTileOffset['flag']
                else:
                    offset = self.imageTileOffset['unopened']
                if self.board.board[i][j].bomb:
                    offset = self.imageTileOffset[-1]
                surface.blit(self.tiles, (0, 0), (128 * offset[0], 128 * offset[1], 128, 128))
                scaledSurface = pygame.transform.scale(surface, (self.gridSize[0], self.gridSize[1]))
                self.screen.blit(scaledSurface, (self.gridSize[0] * j, self.gridSize[1] * i))

    def reveal(self, x, y):
        if self.board.board[y][x].bomb:
            self.board.board[y][x].revealed = True
            self.displayBombs(self.board)
            self.displayEndgame(False)
            self.endgame = True
            return False
        if not self.board.board[y][x].revealed:
            self.board.board[y][x].revealed = True
            self.board.cellsLeft -= 1
            if self.board.board[y][x].nearbyBombs == 0:
                self.board.revealZeros(x, y)
            return True
        # print('invalid')
        return False

    def test_ai_win(self, genome, config, games, display=False, delay=True):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        wins = 0
        games_played = 0
        while games_played < games:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.displayBoard(self.board)

            input = []

            for row in self.board.board:
                for cell in row:
                    input.append((cell.nearbyBombs if cell.revealed else -1))

            output = net.activate(input)
            lst = [i for i in range(len(output))]
            unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

            ind_to_pop = []
            for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                if self.board.board[int(i / self.board.height)][i % self.board.width].revealed:
                    ind_to_pop.append(i)
            for ind in reversed(ind_to_pop):
                unrevealed_squares.pop(ind)

            pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples
            # print(pick[1])

            if not self.endgame:
                print(f'cells left: {self.board.cellsLeft} unrevealed_squares: {len(unrevealed_squares)}')
                print(f'index: {pick[1]} x: {pick[1] % self.board.width} y: {int(pick[1] / self.board.height)}')
            self.reveal(pick[1] % self.board.width, int(pick[1] / self.board.height))
            if self.board.checkWin():
                self.endgame = True
                wins += 1
            if self.endgame:
                games_played += 1
                self.endgame = False
                self.board.randomizeBoard(self.difficultySettings[self.difficulty][0],
                                          self.difficultySettings[self.difficulty][1],
                                          self.difficultySettings[self.difficulty][2])
            if display:
                pygame.display.update()
                if delay:
                    pygame.time.wait(500)
        return wins / games

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.endgame:
                        self.pause = not self.pause

            if not self.pause:
                self.displayBoard(self.board)

                input = []

                for row in self.board.board:
                    for cell in row:
                        input.append((cell.nearbyBombs if cell.revealed else -1))

                output = net.activate(input)
                lst = [i for i in range(len(output))]
                unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

                ind_to_pop = []
                for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                    if self.board.board[int(i / self.board.height)][i % self.board.width].revealed:
                        ind_to_pop.append(i)
                for ind in reversed(ind_to_pop):
                    unrevealed_squares.pop(ind)

                pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples
                print(pick[1])

                if not self.endgame:
                    print(f'cells left: {self.board.cellsLeft} unrevealed_squares: {len(unrevealed_squares)}')
                    print(f'index: {pick[1]} x: {pick[1] % self.board.width} y: {int(pick[1] / self.board.height)}')
                self.reveal(pick[1] % self.board.width, int(pick[1] / self.board.height))
                if self.endgame:
                    fitness_delta = 0
                    for row in self.board.board:
                        for cell in row:
                            if cell.revealed:
                                if cell.bomb:
                                    fitness_delta -= 50  # will be multiplied by 2 because there are 2 bombs, so basically erases winning one game
                                else:
                                    fitness_delta += cell.nearbyBombs + 1
                    print(f'fitness_delta:{fitness_delta}')
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()

                pygame.display.update()
                pygame.time.wait(500)

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        guesses = 0
        predicted = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.displayBoard(self.board)

            input = []

            for row in self.board.board:
                for cell in row:
                    input.append((cell.nearbyBombs if cell.revealed else -1))

            output = net.activate(input)
            lst = [i for i in range(len(output))]
            unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

            ind_to_pop = []
            for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                if self.board.board[int(i / self.board.height)][i % self.board.width].revealed:
                    ind_to_pop.append(i)
            for ind in reversed(ind_to_pop):
                unrevealed_squares.pop(ind)

            pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples

            hit_bomb = not self.reveal(pick[1] % self.board.width, int(pick[1] / self.board.height))

            if self.board.checkWin():
                self.calculate_fitness(genome, True, guesses, predicted)
                break

            if hit_bomb:
                self.calculate_fitness(genome, False, guesses, predicted)
                break

            # pygame.display.update()
            # pygame.time.wait(250)

    def calculate_fitness(self, genome, won, guesses, predicted):
        fitness_delta = 0
        for row in self.board.board:
            for cell in row:
                if cell.revealed and not cell.bomb:
                    fitness_delta += cell.nearbyBombs
        fitness_delta += 100 if won else -50
        fitness_delta -= guesses
        fitness_delta += predicted
        genome.fitness += fitness_delta

    def loop(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.MOUSEBUTTONDOWN and self.settings:  # if we are in the settings and there is an event
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if self.center[0] - self.buttonWidth / 2 <= pos[0] <= self.center[0] + self.buttonWidth / 2:
                            if self.center[1] - self.buttonHeight / 2 - (self.buttonHeight + self.distBetweenButtons) <= \
                                    pos[1] \
                                    <= self.center[1] - self.buttonHeight / 2 - self.distBetweenButtons:  # easy
                                self.difficulty = 'easy'
                                self.gridSize = (
                                    self.width / self.difficultySettings[self.difficulty][0],
                                    self.height / self.difficultySettings[self.difficulty][1])
                                self.settings = False
                                break
                            if self.center[1] - self.buttonHeight / 2 <= pos[1] <= self.center[
                                1] + self.buttonHeight / 2:  # medium
                                self.difficulty = 'medium'
                                self.gridSize = (
                                    self.width / self.difficultySettings[self.difficulty][0],
                                    self.height / self.difficultySettings[self.difficulty][1])
                                self.settings = False
                                break
                            if self.center[1] + self.buttonHeight / 2 + self.distBetweenButtons <= pos[1] \
                                    <= self.center[1] + 3 * self.buttonHeight / 2 + self.distBetweenButtons:  # hard
                                self.difficulty = 'hard'
                                self.gridSize = (
                                    self.width / self.difficultySettings[self.difficulty][0],
                                    self.height / self.difficultySettings[self.difficulty][1])
                                self.settings = False
                                break
                if event.type == pygame.MOUSEBUTTONDOWN and not self.settings:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if self.center[0] - self.buttonWidth / 2 <= pos[0] <= self.center[0] + self.buttonWidth / 2:
                            if self.center[1] - self.buttonHeight / 2 - (self.buttonHeight + self.distBetweenButtons) <= \
                                    pos[1] \
                                    <= self.center[
                                1] - self.buttonHeight / 2 - self.distBetweenButtons and not self.settings:  # play
                                self.board.randomizeBoard(self.difficultySettings[self.difficulty][0],
                                                          self.difficultySettings[self.difficulty][1],
                                                          self.difficultySettings[self.difficulty][2])
                                self.running = True
                            if self.center[1] - self.buttonHeight / 2 <= pos[1] <= self.center[
                                1] + self.buttonHeight / 2:  # self.settings
                                print('Settings!')
                                self.settings = True
                                self.displaySettings()
                            if self.center[1] + self.buttonHeight / 2 + self.distBetweenButtons <= pos[1] \
                                    <= self.center[
                                1] + 3 * self.buttonHeight / 2 + self.distBetweenButtons and not self.settings:  # self.exit
                                self.exit = True

            if self.settings:
                self.displaySettings()
            if not self.settings:
                self.displayMenu()
            pygame.display.update()

            while self.running:
                if not self.pause and not self.endgame:
                    self.screen.fill(self.backgroundColor)
                if self.pause:
                    self.displayPause()
                if self.board.checkWin():
                    self.endgame = True
                    self.displayBoard(self.board)
                    self.displayEndgame(True)
                if not self.pause and not self.endgame:
                    self.displayBoard(self.board)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.exit = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and not self.endgame:
                            self.pause = not self.pause
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.pause and not self.endgame:
                        pos = pygame.mouse.get_pos()
                        coords = ((int)(pos[0] / self.gridSize[0]), (int)(pos[1] / self.gridSize[1]))
                        if event.button == 1:
                            if not self.board.board[coords[1]][coords[0]].flagged:
                                self.reveal(coords[0], coords[1])
                                # if self.board.board[coords[1]][coords[0]].bomb:
                                #     self.board.board[coords[1]][coords[0]].revealed = True
                                #     self.displayBombs(self.board)
                                #     self.displayEndgame(False)
                                #     self.endgame = True
                                # if not self.board.board[coords[1]][coords[0]].revealed:
                                #     self.board.board[coords[1]][coords[0]].revealed = True
                                #     self.board.cellsLeft -= 1
                                #     if self.board.board[coords[1]][coords[0]].nearbyBombs == 0:
                                #         self.board.revealZeros(coords[0], coords[1])
                        if event.button == 3:
                            if not self.board.board[coords[1]][coords[0]].revealed:
                                if self.board.board[coords[1]][coords[0]].flagged:
                                    self.board.board[coords[1]][coords[0]].flagged = not \
                                        self.board.board[coords[1]][coords[0]].flagged
                                    self.board.flags += 1
                                elif self.board.flags > 0:
                                    self.board.board[coords[1]][coords[0]].flagged = not \
                                        self.board.board[coords[1]][coords[0]].flagged
                                    self.board.flags -= 1
                    if event.type == pygame.MOUSEBUTTONDOWN and self.pause:
                        pos = pygame.mouse.get_pos()
                        if event.button == 1:
                            if self.center[0] - self.buttonWidth / 2 <= pos[0] <= self.center[0] + self.buttonWidth / 2:
                                if self.center[1] - self.buttonHeight / 2 - (
                                        self.buttonHeight + self.distBetweenButtons) <= pos[1] \
                                        <= self.center[1] - self.buttonHeight / 2 - self.distBetweenButtons:  # resume
                                    self.pause = False
                                if self.center[1] - self.buttonHeight / 2 <= pos[1] <= self.center[
                                    1] + self.buttonHeight / 2:  # restart
                                    self.board.randomizeBoard(self.difficultySettings[self.difficulty][0],
                                                              self.difficultySettings[self.difficulty][1],
                                                              self.difficultySettings[self.difficulty][2])
                                    self.pause = False
                                if self.center[1] + self.buttonHeight / 2 + self.distBetweenButtons <= pos[1] \
                                        <= self.center[
                                    1] + 3 * self.buttonHeight / 2 + self.distBetweenButtons:  # back to menu
                                    self.running = False
                                    self.pause = False
                    if event.type == pygame.MOUSEBUTTONDOWN and self.endgame:
                        pos = pygame.mouse.get_pos()
                        if event.button == 1:
                            if self.center[0] - self.buttonWidth / 2 <= pos[0] <= self.center[0] + self.buttonWidth / 2:
                                if self.center[1] + self.buttonHeight / 2 + self.distBetweenButtons <= pos[1] \
                                        <= self.center[
                                    1] + 3 * self.buttonHeight / 2 + self.distBetweenButtons:  # back to menu
                                    self.running = False
                                    self.endgame = False
