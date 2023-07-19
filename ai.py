from minesweeper import game as gameIns
import neat.nn
import pygame

class ai:

    def __init__(self, view = False):
        self.game = gameIns(3,3,2)
        self.view = view

    def test_ai_win(self, genome, config, games, display=False, delay=True):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        wins = 0
        games_played = 0
        while games_played < games:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.game.displayBoard(self.game.board)

            input = []

            for row in self.game.board.board:
                for cell in row:
                    input.append((cell.nearbyBombs if cell.revealed else -1))

            output = net.activate(input)
            lst = [i for i in range(len(output))]
            unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

            ind_to_pop = []
            for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                if self.game.board.board[int(i / self.game.board.height)][i % self.game.board.width].revealed:
                    ind_to_pop.append(i)
            for ind in reversed(ind_to_pop):
                unrevealed_squares.pop(ind)

            pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples
            # print(pick[1])

            if not self.game.endgame:
                print(f'cells left: {self.game.board.cellsLeft} unrevealed_squares: {len(unrevealed_squares)}')
                print(f'index: {pick[1]} x: {pick[1] % self.game.board.width} y: {int(pick[1] / self.game.board.height)}')
            self.game.reveal(pick[1] % self.game.board.width, int(pick[1] / self.game.board.height))
            if self.game.board.checkWin():
                self.game.endgame = True
                wins += 1
            if self.game.endgame:
                games_played += 1
                self.game.endgame = False
                self.game.board.randomizeBoard(self.game.difficultySettings[self.game.difficulty][0],
                                          self.game.difficultySettings[self.game.difficulty][1],
                                          self.game.difficultySettings[self.game.difficulty][2])
            if display:
                pygame.display.update()
                if delay:
                    pygame.time.wait(500)
        return wins / games

    def test(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        print(f'fitness: {genome.fitness}')
        guesses = 0
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not self.endgame:
                        self.pause = not self.pause

            if not self.game.pause:
                self.game.displayBoard(self.game.board)

                input = []

                for row in self.game.board.board:
                    for cell in row:
                        input.append((cell.nearbyBombs if cell.revealed else -1))

                output = net.activate(input)
                lst = [i for i in range(len(output))]
                unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

                ind_to_pop = []
                for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                    if self.game.board.board[int(i / self.game.board.height)][i % self.game.board.width].revealed:
                        ind_to_pop.append(i)
                for ind in reversed(ind_to_pop):
                    unrevealed_squares.pop(ind)

                pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples
                # print(pick[1])
                guesses += 1
                if not self.game.endgame:
                    print(f'cells left: {self.game.board.cellsLeft} unrevealed_squares: {len(unrevealed_squares)}')
                    print(f'x: {pick[1] % self.game.board.width} y: {int(pick[1] / self.game.board.height)}')
                self.game.reveal(pick[1] % self.game.board.width, int(pick[1] / self.game.board.height))
                if self.game.endgame:
                    fitness_delta = 0
                    fitness_delta += 5 if self.game.board.checkWin() else -5
                    fitness_delta += guesses
                    print(f'fitness_delta:{fitness_delta}')
                    pygame.display.update()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()

                pygame.display.update()
                pygame.time.wait(500)

    def train(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        guesses = 0
        wins = 0

        self.game.board.randomizeBoard(self.game.board.width,self.game.board.height,self.game.board.numBombs)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.game.displayBoard(self.game.board)

            input = []

            for row in self.game.board.board:
                for cell in row:
                    input.append((cell.nearbyBombs if cell.revealed else -1))

            output = net.activate(input)
            lst = [i for i in range(len(output))]
            unrevealed_squares = list(zip(lst, output))  # make this a list of tuples

            ind_to_pop = []
            for i in range(len(output)):  # leaves only the unrevealed squares to pick from
                if self.game.board.board[int(i / self.game.board.height)][i % self.game.board.width].revealed:
                    ind_to_pop.append(i)
            for ind in reversed(ind_to_pop):
                unrevealed_squares.pop(ind)

            pick = min((out, ind) for ind, out in unrevealed_squares)  # instead of using index, we use the tuples

            hit_bomb = not self.game.reveal(pick[1] % self.game.board.width, int(pick[1] / self.game.board.height))

            if self.game.board.checkWin():
                wins += 1
                self.game.board.randomizeBoard(self.game.board.width,self.game.board.height,self.game.board.numBombs)

            if hit_bomb:
                self.calculate_fitness(genome, wins, guesses)
                break
            
            guesses += 1

            if self.view:
                pygame.display.update()
                pygame.time.wait(250)

    def calculate_fitness(self, genome, wins, guesses):
        fitness_delta = -5
        # if wins > 0:
        #     print(wins)
        # for row in self.game.board.board:
        #     for cell in row:
        #         if cell.revealed and not cell.bomb:
        #             fitness_delta += cell.nearbyBombs
        fitness_delta += 50 * wins
        fitness_delta += guesses
        genome.fitness += fitness_delta