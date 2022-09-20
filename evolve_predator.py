import numpy as np
from deap import base, creator, tools, algorithms
import config
import simulator
import individual
import utils
import pickle
import geometry
import nn
import multiprocessing
from scipy import stats as spystats
import pygame

utils.seed(0)
counter = 0
prey_positions = []
for prey in range(30):
    prey_positions.append(geometry.Point(utils.randint(config.PREDATOR_SPAWN_BOX[1].x, config.HIGHX), utils.randint(config.PREDATOR_SPAWN_BOX[1].y, config.HIGHY)))

def evaluate(individual_brain):
    model = nn.NN(config.PREDATOR_LAYERS_LIST)
    model.set_weights(individual_brain)
    game = simulator.PredatorEvolverSimulation(model, 1, len(prey_positions))
    #game.preds[0].dir = geometry.Vector(1, 1).normalized()
    #game.preds[0].pos = geometry.Point(0, 0)
    #game.preds[0].speed = geometry.Vector(1, 1, mag=config.PREDATOR_SPEED_LIMIT/2)
    #for i in range(len(prey_positions)):
    #    game.preys[i].pos = prey_positions[i]
    
    game.start()

    return (game.fitness,)


model = nn.NN(config.PREDATOR_LAYERS_LIST)
ind_size = model.params
print(ind_size)

creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register('weight_bin', utils.random)
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.weight_bin, n=ind_size)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

toolbox.register('mate', tools.cxTwoPoint)
toolbox.register('mutate', tools.mutFlipBit, indpb=0.2)
toolbox.register('select', tools.selTournament, tournsize=3)
toolbox.register('evaluate', evaluate)
pool = multiprocessing.Pool()
toolbox.register('map', pool.map)



stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register('Max', np.max)
stats.register('Min', np.min)
stats.register('Mean', np.mean)
stats.register('Std', np.std)
stats.register('25%', lambda arr: np.percentile(arr, 25))
stats.register('Median', np.median)
stats.register('75%', lambda arr: np.percentile(arr, 75))
# stats.register('Counts', lambda arr: np.unique(arr, return_counts=True))

pop = toolbox.population(n=200)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=100, halloffame=hof, stats=stats)
pops = sorted(pop, key=lambda ind: ind.fitness, reverse=True)
print(log)

with open("predator2.pkl", "wb") as cp_file:
    pickle.dump(pops[0], cp_file)
