from minesweeper import game
import neat
import os
import pickle


def runNeat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-13')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 25)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai_win_percentage(config, games, display, delay):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    gameIns = game()
    percent = gameIns.test_ai_win(winner, config, games, display, delay)
    print(f'percent: {percent*100}%')


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    gameIns = game()
    gameIns.test_ai(winner, config)


def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0 if genome.fitness == None else genome.fitness
        gameInstance = game()
        force_quit = gameInstance.train_ai(genome, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                         neat.DefaultStagnation, config_path)

    runNeat(config)
    # test_ai(config)
    # test_ai_win_percentage(config, 100, False, False)
