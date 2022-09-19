import numpy as np
from deap import base, creator, tools, algorithms
import config
import simulator
import individual
import utils
import pickle
import nn

counter = 0

def evaluate(individual_brain):
    global counter
    
    counter += 1
    soma = 0

    if counter % 20 == 0:
        print(counter)

    for i in range(5):

        model = nn.NN(config.PREY_LAYERS_LIST)
        model.set_weights(individual_brain)
        game = simulator.PreyEvolverSimulation(model, 10, 5)
        
        game.start()

        soma += game.fitness

    
    
    return (soma/5,)


model = nn.NN(config.PREY_LAYERS_LIST)
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

pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.01, ngen=100, halloffame=hof, stats=stats)
best_pop = sorted(pop, key=lambda ind: ind.fitness, reverse=True)[0]
print(log)

with open("randomodel.pkl", "wb") as cp_file:
    pickle.dump(best_pop, cp_file)
