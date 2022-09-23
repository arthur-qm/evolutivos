import pickle
import simulator
import pygame
from individual import Individual
from deap import creator, base
import nn
import config
import numpy as np

creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)


with open('predator.pkl', 'rb') as f:
    melhor_ger = pickle.load(f)[0]

modelpred = nn.NN(config.PREDATOR_LAYERS_LIST)
modelpred.set_weights(melhor_ger)



creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

model = nn.NN(config.PREY_LAYERS_LIST)

config.PRED_CAN_CROSS_WALLS = True
config.PREY_CAN_CROSS_WALLS = True

game = simulator.PreyEvolverSimulation(model, modelpred, 5, 20, True, screen, pygame.display.update, pygame.event.get)

game.start()
print(game.time_taken)
