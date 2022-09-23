import pickle
import nn
import config
import simulator
import pygame
from deap import creator, base

creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)

model_file = 'predator.pkl'

with open(model_file, 'rb') as f:
    melhor_gen = pickle.load(f)[0]

rn = nn.NN(config.PREDATOR_LAYERS_LIST)
rn.set_weights(melhor_gen)

pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

config.PREDATOR_INITIAL_ENERGY = 10000
config.MAXTIME = 10000

config.PRED_CAN_CROSS_WALLS = False
config.PREY_CAN_CROSS_WALLS = False

jogopred = simulator.PredatorEvolverSimulation(rn, None, 1, 5, True, True, screen, pygame.display.update, pygame.event.get)
jogopred.start()