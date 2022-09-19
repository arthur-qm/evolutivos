import pickle
import simulator
import pygame
from individual import Individual
from deap import creator, base
import nn
import config
import numpy as np

def decide_on(model):
    def decision(self):
        arr = np.expand_dims(np.array(self.distances + self.wall_distances + [self.acc/config.PREY_ACCELERATION_LIMIT, (self.speed *self.dir)/config.PREY_SPEED_LIMIT]).reshape(-1), axis=0)
        # print(len(arr), 2*config.PREY_NEURONS)
        prediction = model.feed_foward(arr)
        # print(prediction)
        if prediction[0][0] < 0.3:
            self.turn_left()
        elif prediction[0][0] > 0.7:
            self.turn_right()
        if prediction[1][0] < 0.3:
            self.decelerate()
        elif prediction[1][0] > 0.7:
            self.accelerate()
    return decision


def follow(prey):
    def decision(self):
        self.speed = (prey.pos - self.pos).normalized() * (config.SPEED_LIMIT * 0.95) 
    return decision


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

with open('randomodel.pkl', 'rb') as f:
    melhor_ger = pickle.load(f)

pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

model = nn.NN(config.PREY_LAYERS_LIST)
model.set_weights(melhor_ger)


game = simulator.PreyEvolverSimulation(model, 10, 1, True, screen, pygame.display.update, pygame.event.get)
    


for pred in game.preds:
    pred.decision = follow(game.preys[0])
    
game.start()
print(game.time_taken)