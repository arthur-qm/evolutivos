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


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

with open('predator.pkl', 'rb') as f:
    melhor_ger = pickle.load(f)
    # print(melhor_ger)    

true_best = 0
true_best_mean_score = 0

"""
for i in range(len(melhor_ger)-1, -1, -1):
    score = 0
    for j in range(5):
        rn = nn.NN(config.PREDATOR_LAYERS_LIST)
        rn.set_weights(melhor_ger[i])
        game = simulator.PredatorEvolverSimulation(rn, None, False, 1, 30, False, None, None, None)
        game.start()
        score += game.fitness
    score /= 5
    if score > true_best_mean_score:
        true_best = i
        true_best_mean_score = score
"""

print(true_best, true_best_mean_score)

pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

rn = nn.NN(config.PREDATOR_LAYERS_LIST)
rn.set_weights(melhor_ger[true_best])

game = simulator.PredatorEvolverSimulation(rn, None, False, True, 1, 30, True, screen, pygame.display.update, pygame.event.get)
#game.preds[0].dir = geometry.Vector(1, 1).normalized()
#game.preds[0].pos = geometry.Point(0, 0)
#game.preds[0].speed = geometry.Vector(1, 1, mag=config.PREDATOR_SPEED_LIMIT/2)
#for i in range(len(prey_positions)):
#    game.preys[i].pos = prey_positions[i]
game.start()
