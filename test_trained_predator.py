import pickle
import simulator
import pygame
from individual import Individual
from deap import creator, base
import nn
import config
import numpy as np
import geometry
import utils


#utils.seed(0)
prey_positions = []
for prey in range(30):
    prey_positions.append(geometry.Point(utils.randint(config.PREDATOR_SPAWN_BOX[1].x, config.HIGHX), utils.randint(config.PREDATOR_SPAWN_BOX[1].y, config.HIGHY)))


pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


with open('predator2.pkl', 'rb') as f:
    melhor_ger = pickle.load(f)

print(melhor_ger)

model = nn.NN(config.PREDATOR_LAYERS_LIST)
model.set_weights(melhor_ger)
    

game = simulator.PredatorEvolverSimulation(model, 1, 30, True, screen, pygame.display.update, pygame.event.get)
#game.preds[0].dir = geometry.Vector(1, 1).normalized()
#game.preds[0].pos = geometry.Point(0, 0)
#game.preds[0].speed = geometry.Vector(1, 1, mag=config.PREDATOR_SPEED_LIMIT/2)
#for i in range(len(prey_positions)):
#    game.preys[i].pos = prey_positions[i]
game.start()
