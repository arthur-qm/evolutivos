import numpy as np
from deap import base, creator, tools, algorithms
import config
import simulator
import individual
import utils
import pickle
import nn
import multiprocessing


creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)


with open('predator.pkl', 'rb') as f:
    melhor_ger = pickle.load(f)[0]

modelpred = nn.NN(config.PREDATOR_LAYERS_LIST)
modelpred.set_weights(melhor_ger)


def evaluate(individual_brain):

    model = nn.NN(config.PREY_LAYERS_LIST)
    model.set_weights(individual_brain)
    game = simulator.PreyEvolverSimulation(model, modelpred, 30, 1)
    
    game.start()

    return (game.fitness,)


model = nn.NN(config.PREY_LAYERS_LIST)
ind_size = model.params
print(ind_size)


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
stats.register('Mean', np.mean)
stats.register('Max', np.max)
stats.register('Min', np.min)
stats.register('Std', np.std)
stats.register('25%', lambda arr: np.percentile(arr, 25))
stats.register('Median', np.median)
stats.register('75%', lambda arr: np.percentile(arr, 75))

pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=20, halloffame=hof, stats=stats)
best_pop = sorted(pop, key=lambda ind: ind.fitness, reverse=True)[0]
print(log)

with open("prey.pkl", "wb") as cp_file:
    pickle.dump(best_pop, cp_file)
