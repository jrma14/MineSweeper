import pygame
import Board

# implement ai

pygame.init()

backgroundColor = (200, 200, 200)

cols = 4
rows = 4
bombs = 2

difficultySettings = {
    'easy': (10, 8, 10),
    'medium': (18, 14, 40),
    'hard': (24, 20, 99),
    'custom': (cols, rows, bombs)
}

difficulty = 'custom'

width = 1920
height = 1080
gridSize = (width / cols, height / rows)

buttonWidth = 300
buttonHeight = height / 6
distBetweenButtons = (height - 3 * buttonHeight) / 3
center = (width / 2, height / 2)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load('minesweeper.png')
pygame.display.set_icon(icon)
font = pygame.font.SysFont('rockwellextra', 32)

imageTileOffset = {
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
tiles = pygame.image.load('minesweeper_tiles.jpg')

board = Board.Board(cols, rows, bombs)

exit = False
running = False
pause = False
endgame = False
settings = False


def displayBoard(board):
    surface = pygame.Surface((128, 128))
    for i in range(board.height):
        for j in range(board.width):
            if board.board[i][j].revealed:
                offset = imageTileOffset[board.board[i][j].nearbyBombs]
            elif board.board[i][j].flagged:
                offset = imageTileOffset['flag']
            else:
                offset = imageTileOffset['unopened']
            surface.blit(tiles, (0, 0), (128 * offset[0], 128 * offset[1], 128, 128))
            scaledSurface = pygame.transform.scale(surface, (gridSize[0], gridSize[1]))
            screen.blit(scaledSurface, (gridSize[0] * j, gridSize[1] * i))


def displayMenu():
    color = (0, 0, 0)
    screen.fill(backgroundColor)
    play = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    settings = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2, buttonWidth, buttonHeight)
    exit = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 + (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    pygame.draw.rect(screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    playText = font.render('Play', True, (255, 0, 0), (255, 255, 255))
    playTextRect = playText.get_rect()
    playTextRect.center = (center[0], center[1] - (buttonHeight + distBetweenButtons))
    settingsText = font.render('Difficulty', True, (255, 0, 0), (255, 255, 255))
    settingsTextRect = settingsText.get_rect()
    settingsTextRect.center = (center[0], center[1])
    exitText = font.render('Exit', True, (255, 0, 0), (255, 255, 255))
    exitTextRect = exitText.get_rect()
    exitTextRect.center = (center[0], center[1] + (buttonHeight + distBetweenButtons))
    screen.blit(playText, playTextRect)
    screen.blit(settingsText, settingsTextRect)
    screen.blit(exitText, exitTextRect)


def displaySettings():
    color = (0, 0, 0)
    screen.fill(backgroundColor)
    play = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    settings = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2, buttonWidth, buttonHeight)
    exit = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 + (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    pygame.draw.rect(screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    playText = font.render('Easy', True, (255, 0, 0), (255, 255, 255))
    playTextRect = playText.get_rect()
    playTextRect.center = (center[0], center[1] - (buttonHeight + distBetweenButtons))
    settingsText = font.render('Medium', True, (255, 0, 0), (255, 255, 255))
    settingsTextRect = settingsText.get_rect()
    settingsTextRect.center = (center[0], center[1])
    exitText = font.render('Hard', True, (255, 0, 0), (255, 255, 255))
    exitTextRect = exitText.get_rect()
    exitTextRect.center = (center[0], center[1] + (buttonHeight + distBetweenButtons))
    screen.blit(playText, playTextRect)
    screen.blit(settingsText, settingsTextRect)
    screen.blit(exitText, exitTextRect)


def displayPause():
    color = (0, 0, 0)
    play = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    settings = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2, buttonWidth, buttonHeight)
    exit = pygame.Rect(center[0] - buttonWidth / 2, center[1] - buttonHeight / 2 + (buttonHeight + distBetweenButtons),
                       buttonWidth, buttonHeight)
    pygame.draw.rect(screen, color, play, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, settings, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    pygame.draw.rect(screen, color, exit, border_top_left_radius=10, border_bottom_right_radius=10,
                     border_top_right_radius=10, border_bottom_left_radius=10)
    playText = font.render('Resume', True, (255, 0, 0), (255, 255, 255))
    playTextRect = playText.get_rect()
    playTextRect.center = (center[0], center[1] - (buttonHeight + distBetweenButtons))
    settingsText = font.render('Restart', True, (255, 0, 0), (255, 255, 255))
    settingsTextRect = settingsText.get_rect()
    settingsTextRect.center = (center[0], center[1])
    exitText = font.render('Back To Menu', True, (255, 0, 0), (255, 255, 255))
    exitTextRect = exitText.get_rect()
    exitTextRect.center = (center[0], center[1] + (buttonHeight + distBetweenButtons))
    screen.blit(playText, playTextRect)
    screen.blit(settingsText, settingsTextRect)
    screen.blit(exitText, exitTextRect)


def displayEndgame(win):
    gameOverText = font.render('Game Over', True, (255, 0, 0), (255, 255, 255))
    gameOverTextRect = gameOverText.get_rect()
    gameOverTextRect.center = (center[0], center[1] - (buttonHeight + distBetweenButtons))
    winLossText = font.render('You Win!' if win else 'You Lose', True, (255, 0, 0), (255, 255, 255))
    winLossTextRect = winLossText.get_rect()
    winLossTextRect.center = (center[0], center[1])
    exitText = font.render('Back To Menu', True, (255, 0, 0), (255, 255, 255))
    exitTextRect = exitText.get_rect()
    exitTextRect.center = (center[0], center[1] + (buttonHeight + distBetweenButtons))
    screen.blit(gameOverText, gameOverTextRect)
    screen.blit(winLossText, winLossTextRect)
    screen.blit(exitText, exitTextRect)


def displayBombs(board):
    surface = pygame.Surface((128, 128))
    for i in range(board.height):
        for j in range(board.width):
            if board.board[i][j].revealed:
                offset = imageTileOffset[board.board[i][j].nearbyBombs]
            elif board.board[i][j].flagged:
                offset = imageTileOffset['flag']
            else:
                offset = imageTileOffset['unopened']
            if board.board[i][j].bomb:
                offset = imageTileOffset[-1]
            surface.blit(tiles, (0, 0), (128 * offset[0], 128 * offset[1], 128, 128))
            scaledSurface = pygame.transform.scale(surface, (gridSize[0], gridSize[1]))
            screen.blit(scaledSurface, (gridSize[0] * j, gridSize[1] * i))


while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN and settings:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if center[0] - buttonWidth / 2 <= pos[0] <= center[0] + buttonWidth / 2:
                    if center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons) <= pos[1] \
                            <= center[1] - buttonHeight / 2 - distBetweenButtons:  # easy
                        difficulty = 'easy'
                        gridSize = (
                        width / difficultySettings[difficulty][0], height / difficultySettings[difficulty][1])
                        settings = False
                        break
                    if center[1] - buttonHeight / 2 <= pos[1] <= center[1] + buttonHeight / 2:  # medium
                        difficulty = 'medium'
                        gridSize = (
                        width / difficultySettings[difficulty][0], height / difficultySettings[difficulty][1])
                        settings = False
                        break
                    if center[1] + buttonHeight / 2 + distBetweenButtons <= pos[1] \
                            <= center[1] + 3 * buttonHeight / 2 + distBetweenButtons:  # hard
                        difficulty = 'hard'
                        gridSize = (
                        width / difficultySettings[difficulty][0], height / difficultySettings[difficulty][1])
                        settings = False
                        break
        if event.type == pygame.MOUSEBUTTONDOWN and not settings:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if center[0] - buttonWidth / 2 <= pos[0] <= center[0] + buttonWidth / 2:
                    if center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons) <= pos[1] \
                            <= center[1] - buttonHeight / 2 - distBetweenButtons and not settings:  # play
                        board.randomizeBoard(difficultySettings[difficulty][0], difficultySettings[difficulty][1],
                                             difficultySettings[difficulty][2])
                        running = True
                    if center[1] - buttonHeight / 2 <= pos[1] <= center[1] + buttonHeight / 2:  # settings
                        print('Settings!')
                        settings = True
                        displaySettings()
                    if center[1] + buttonHeight / 2 + distBetweenButtons <= pos[1] \
                            <= center[1] + 3 * buttonHeight / 2 + distBetweenButtons and not settings:  # exit
                        exit = True

    if settings:
        displaySettings()
    if not settings:
        displayMenu()
    pygame.display.update()

    while running:
        if not pause and not endgame:
            screen.fill(backgroundColor)
        if pause:
            displayPause()
        if board.checkWin():
            endgame = True
            displayBoard(board)
            displayEndgame(True)
        if not pause and not endgame:
            displayBoard(board)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not endgame:
                    pause = not pause
            if event.type == pygame.MOUSEBUTTONDOWN and not pause and not endgame:
                pos = pygame.mouse.get_pos()
                coords = ((int)(pos[0] / gridSize[0]), (int)(pos[1] / gridSize[1]))
                if event.button == 1:
                    if not board.board[coords[1]][coords[0]].flagged:
                        if board.board[coords[1]][coords[0]].bomb:
                            board.board[coords[1]][coords[0]].revealed = True
                            displayBombs(board)
                            displayEndgame(False)
                            endgame = True
                        if not board.board[coords[1]][coords[0]].revealed:
                            board.board[coords[1]][coords[0]].revealed = True
                            board.cellsLeft -= 1
                            if board.board[coords[1]][coords[0]].nearbyBombs == 0:
                                board.revealZeros(coords[0], coords[1])
                if event.button == 3:
                    if not board.board[coords[1]][coords[0]].revealed:
                        if board.board[coords[1]][coords[0]].flagged:
                            board.board[coords[1]][coords[0]].flagged = not board.board[coords[1]][coords[0]].flagged
                            board.flags += 1
                        elif board.flags > 0:
                            board.board[coords[1]][coords[0]].flagged = not board.board[coords[1]][coords[0]].flagged
                            board.flags -= 1
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if center[0] - buttonWidth / 2 <= pos[0] <= center[0] + buttonWidth / 2:
                        if center[1] - buttonHeight / 2 - (buttonHeight + distBetweenButtons) <= pos[1] \
                                <= center[1] - buttonHeight / 2 - distBetweenButtons:  # resume
                            pause = False
                        if center[1] - buttonHeight / 2 <= pos[1] <= center[1] + buttonHeight / 2:  # restart
                            board.randomizeBoard(difficultySettings[difficulty][0], difficultySettings[difficulty][1],
                                                 difficultySettings[difficulty][2])
                            pause = False
                        if center[1] + buttonHeight / 2 + distBetweenButtons <= pos[1] \
                                <= center[1] + 3 * buttonHeight / 2 + distBetweenButtons:  # back to menu
                            running = False
                            pause = False
            if event.type == pygame.MOUSEBUTTONDOWN and endgame:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if center[0] - buttonWidth / 2 <= pos[0] <= center[0] + buttonWidth / 2:
                        if center[1] + buttonHeight / 2 + distBetweenButtons <= pos[1] \
                                <= center[1] + 3 * buttonHeight / 2 + distBetweenButtons:  # back to menu
                            running = False
                            endgame = False
