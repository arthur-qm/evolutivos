import individual
import config
import utils
from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.key import get_pressed
from pygame import font
import numpy as np
from math import atan2, pi


class Game:
    def __init__(self, npreds, npreys, broadcast=False, screen=None, upd=None, get_event=None):

        self.preys = [individual.Prey() for _ in range(npreys)]

        self.preds = [individual.Predator() for _ in range(npreds)]

        for i in range(len(self.preys)):
            self.preys[i].pos.x = utils.randint(config.PREY_SPAWN_BOX[0].x, config.PREY_SPAWN_BOX[1].x)
            self.preys[i].pos.y = utils.randint(config.PREY_SPAWN_BOX[0].y, config.PREY_SPAWN_BOX[1].y)
        
        for i in range(len(self.preds)):
            self.preds[i].pos.x = utils.randint(config.PREDATOR_SPAWN_BOX[0].x, config.PREDATOR_SPAWN_BOX[1].x)
            self.preds[i].pos.y = utils.randint(config.PREDATOR_SPAWN_BOX[0].y, config.PREDATOR_SPAWN_BOX[1].y)
            self.preds[i].energy = config.PREDATOR_INITIAL_ENERGY
            self.preds[i].digestion = 0
            self.preds[i].fitness = 0

        self.time_taken = 0
        self.broadcast = broadcast
        self.screen = screen
        self.upd = upd
        self.get_event = get_event
        self.force_end = False

    def tick(self):
        if self.time_taken >= config.MAXTIME:
            return

        self.time_taken += 1

        if self.broadcast:
            for i in range(len(self.preys)):
                self.preys[i].draw(self.screen)
            for i in range(len(self.preds)):
                self.preds[i].draw(self.screen)
            
            self.upd()
            utils.sleep(config.TIME_RATE)

            for i in range(len(self.preys)):
                self.preys[i].erase(self.screen)
            for i in range(len(self.preds)):
                self.preds[i].erase(self.screen)
        
            for ev in self.get_event():
                if ev.type == QUIT:
                    self.force_end = True
                    return

        for i in range(len(self.preys)):
            self.preys[i].update_neurons(self.preds)
            self.preys[i].decision()
        
        for i in range(len(self.preds)):
            self.preds[i].update_neurons(self.preys)
            self.preds[i].decision()
          
        for i in range(len(self.preys)):
            self.preys[i].move()
        
        for i in range(len(self.preds)):
            self.preds[i].move()
            self.preds[i].energy -= config.PREDATOR_BODY_MAINTANCE_COST + self.preds[i].speed.mag**2 * config.PREDATOR_SPEED_COST
            if self.preds[i].digestion > 0:
                self.preds[i].energy += config.PREDATOR_ENERGY_RECOVERY
            self.preds[i].digestion -= config.PREDATOR_DIGESTION_CONVERSION
            if self.preds[i].digestion < 0:
                self.preds[i].digestion = 0
            if self.preds[i].energy > config.PREDATOR_ENERGY_LIMIT:
                self.preds[i].energy = config.PREDATOR_ENERGY_LIMIT
        
        self.preds = [self.preds[i] for i in range(len(self.preds)) if self.preds[i].energy >= 0]

        dead_preys = set()

        for j in range(len(self.preds)):
            for i in range(len(self.preys)):
                if self.preds[j].hits(self.preys[i]) and i not in dead_preys:
                    dead_preys.add(i)
                    self.preds[j].digestion += config.PREDATOR_DIGESTIVE_INCREASE
            if self.preds[j].digestion > config.PREDATOR_MAX_DIGESTION_CAPACITY:
                self.preds[j].digestion = config.PREDATOR_MAX_DIGESTION_CAPACITY

        self.preys = [self.preys[i] for i in range(len(self.preys)) if i not in dead_preys]

        if len(self.preys) == 0:
            self.force_end = True

    def start(self):
        while self.time_taken < config.MAXTIME and not self.force_end:
            self.tick()
    
    @staticmethod
    def make_it_move(individual):
        keys = get_pressed()

        if keys[K_LEFT]:
            individual.turn_left()
        if keys[K_RIGHT]:
            individual.turn_right()
        if keys[K_UP]:
            individual.accelerate()
        if keys[K_DOWN]:
            individual.decelerate()
    

class PredatorEvolverSimulation(Game):
    def __init__(self, model, model_preys, playable=False, show_energy=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.initial_p = len(self.preys) 
        self.fitness = 0
        self.model_preys = model_preys
        self.playable = playable
        if self.broadcast:
            self.my_font = font.SysFont('Comic Sans MS', 30)

    
    def tick(self):
        if self.time_taken >= config.MAXTIME:
            return

        self.time_taken += 1
        if self.broadcast:
            for i in range(len(self.preys)):
                self.preys[i].draw(self.screen)
            for i in range(len(self.preds)):
                self.preds[i].draw(self.screen)
            
            # Write stats of self.preds[0] (energy, hunger, speed, acceleration)
            stats = f"""Energy: {self.preds[0].energy:.2f} 
Digestion: {self.preds[0].digestion}
Speed: {self.preds[0].speed.mag}
Acceleration: {self.preds[0].acc}
Mass: {self.preds[0].mass}"""
            text_surfaces = [self.my_font.render(stat, False, (0, 0, 0)) for stat in stats.split('\n')]
            for i in range(len(text_surfaces)):
                self.screen.blit(text_surfaces[i], (0, 15*i))

            self.upd()
            utils.sleep(config.TIME_RATE)

            self.screen.fill(config.BG_COLOR)
            for ev in self.get_event():
                if ev.type == QUIT:
                    self.force_end = True
                    return
            

        for i in range(len(self.preds)):
            self.preds[i].update_neurons(self.preys)
            PredatorEvolverSimulation.update_acceleration(self.preds[i], self.model)
        
        if self.playable:
            for i in range(len(self.preys)):
                Game.make_it_move(self.preys[i])
        elif self.model_preys != None:
            for i in range(len(self.preys)):
                self.preys[i].update_neurons(self.preds)

        for i in range(len(self.preds)):
            self.preds[i].move()
            self.preds[i].energy -= config.PREDATOR_BODY_MAINTANCE_COST + self.preds[i].speed.mag**2 * self.preds[i].mass
            if self.preds[i].digestion > 0:
                self.preds[i].energy += config.PREDATOR_ENERGY_RECOVERY
            self.preds[i].digestion -= config.PREDATOR_DIGESTION_CONVERSION
            if self.preds[i].digestion < 0:
                self.preds[i].digestion = 0
            if self.preds[i].energy > config.PREDATOR_ENERGY_LIMIT:
                self.preds[i].energy = config.PREDATOR_ENERGY_LIMIT
            
        
        if self.playable:
        
            for i in range(len(self.preys)):
                self.preys[i].move()
        elif self.model_preys != None:
            for i in range(len(self.preys)):
                self.preys[i].move()
            
        
        self.preds = [self.preds[i] for i in range(len(self.preds)) if self.preds[i].energy >= 0]
        self.fitness += sum(self.preds[i].energy for i in range(len(self.preds)))

        dead_preys = set()

        for j in range(len(self.preds)):
            for i in range(len(self.preys)):
                if self.preds[j].hits(self.preys[i]) and i not in dead_preys:
                    dead_preys.add(i)
                    self.preds[j].digestion += config.PREDATOR_DIGESTIVE_INCREASE
                    self.preds[j].mass += config.MASS_INCREMENT
            if self.preds[j].digestion > config.PREDATOR_MAX_DIGESTION_CAPACITY:
                self.preds[j].digestion = config.PREDATOR_MAX_DIGESTION_CAPACITY

        self.preys = [self.preys[i] for i in range(len(self.preys)) if i not in dead_preys]

        if len(self.preds) == 0 or self.time_taken >= config.MAXTIME:
            self.force_end = True
    
    @staticmethod
    def update_acceleration(pred, model):
        arr = np.array(pred.distances + pred.wall_distances +\
            [pred.speed.mag / config.PREDATOR_SPEED_LIMIT, atan2(pred.speed * pred.dir.rot90anti(), pred.speed * pred.dir) / pi,
            pred.acc/config.PREDATOR_ACCELERATION_LIMIT, pred.energy / config.PREDATOR_ENERGY_LIMIT,
            pred.digestion / config.PREDATOR_MAX_DIGESTION_CAPACITY])

        arr = np.expand_dims(arr.reshape(-1), axis=0)

        prediction = model.feed_foward(arr)

        if prediction[0][0] < 0.3:
            pred.turn_left()
        elif prediction[0][0] > 0.7:
            pred.turn_right()
        if prediction[1][0] < 0.3:
            pred.decelerate()
        elif prediction[1][0] > 0.7:
            pred.accelerate()

    @staticmethod
    def follow(pred, prey, fraction=0.95):
        pred.speed = (prey.pos - pred.pos).normalized() * (config.SPEED_LIMIT * fraction) 
