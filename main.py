import neat
import os
import pickle
from ai import ai as ai_ins
import sys


def runNeat(config, checkpoint = -1):
    if checkpoint != -1:
        p = neat.Checkpointer.restore_checkpoint(f'neat-checkpoint-{checkpoint}')
    else:
        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))

    winner = p.run(eval_genomes, 25)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def eval_genomes(genomes, config):
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0 if genome.fitness == None else genome.fitness
        ai = ai_ins()
        ai.train(genome, config)

def test_ai_win_percentage(config, games, display, delay):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    ai = ai_ins()
    percent = ai.test_ai_win(winner, config, games, display, delay)
    print(f'percent: {percent*100}%')


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    ai = ai_ins(True)
    ai.test(winner, config)



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                         neat.DefaultStagnation, config_path)
    if len(sys.argv) != 2:
        print('give an option')
    elif sys.argv[1] == 'train':
        runNeat(config)
    elif sys.argv[1] == 'test':
        test_ai(config)
    elif sys.argv[1] == 'percent':
        test_ai_win_percentage(config, 100, False, False)
