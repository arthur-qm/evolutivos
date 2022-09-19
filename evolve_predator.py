import numpy as np
from deap import base, creator, tools, algorithms
import config
import simulator
import individual
import utils
import pickle
import geometry
import nn

utils.seed(0)
counter = 0
prey_positions = []
for prey in range(30):
    prey_positions.append(geometry.Point(utils.randint(config.PREDATOR_SPAWN_BOX[1].x, config.HIGHX), utils.randint(config.PREDATOR_SPAWN_BOX[1].y, config.HIGHY)))

def evaluate(individual_brain):
    global counter
    
    counter += 1

    if counter % 100 == 0:
        print(counter)

    model = nn.NN(config.PREDATOR_LAYERS_LIST)
    model.set_weights(individual_brain)
    game = simulator.PredatorEvolverSimulation(model, 1, len(prey_positions))
    game.preds[0].dir = geometry.Vector(1, 1).normalized()
    game.preds[0].pos = geometry.Point(0, 0)
    for i in range(len(prey_positions)):
        game.preys[i].pos = prey_positions[i]
    
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
toolbox.register('mutate', tools.mutFlipBit, indpb=0.01)
toolbox.register('select', tools.selTournament, tournsize=3)
toolbox.register('evaluate', evaluate)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register('Mean', np.mean)
stats.register('Max', np.max)
stats.register('Min', np.min)

pop = toolbox.population(n=200)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.05, ngen=500, halloffame=hof, stats=stats)
pops = sorted(pop, key=lambda ind: ind.fitness, reverse=True)
print(log)

with open("predator.pkl", "wb") as cp_file:
    for i in range(len(pops)):
        bpop = pops[i]
        pickle.dump([i] + bpop, cp_file)
