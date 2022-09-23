import individual
import config
import utils
from pygame.locals import QUIT, K_LEFT, K_RIGHT, K_UP, K_DOWN
from pygame.key import get_pressed
import numpy as np



class Game:
    def __init__(self, npreds, npreys, broadcast=False, screen=None, upd=None, get_event=None):

        self.preys = [individual.Prey() for _ in range(npreys)]

        self.preds = [individual.Predator() for _ in range(npreds)]

        for i in range(len(self.preys)):
            self.preys[i].pos.x = utils.randint(config.PREY_SPAWN_BOX[0].x, config.PREY_SPAWN_BOX[1].x)
            self.preys[i].pos.y = utils.randint(config.PREY_SPAWN_BOX[0].y, config.PREY_SPAWN_BOX[1].y)
            self.preys[i].mean_distance_to_pred = 0
        
        for i in range(len(self.preds)):
            self.preds[i].pos.x = utils.randint(config.PREDATOR_SPAWN_BOX[0].x, config.PREDATOR_SPAWN_BOX[1].x)
            self.preds[i].pos.y = utils.randint(config.PREDATOR_SPAWN_BOX[0].y, config.PREDATOR_SPAWN_BOX[1].y)

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
        # print(self.time_taken)

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
        
        self.preys = list(filter(lambda prey: all(not prey.hits(pred) for pred in self.preds), self.preys))
        
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
    def __init__(self, model, model_preys, playable=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.initial_p = len(self.preys)
        for pred in self.preds:
            pred.energy = config.PREDATOR_INITIAL_ENERGY
            pred.prox = 0
        self.fitness = 0
        self.model_preys = model_preys
        self.playable = playable
        
    
    def tick(self):
        if self.time_taken >= config.MAXTIME:
            return

        self.time_taken += 1
        # print(self.time_taken)

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

        for i in range(len(self.preds)):
            self.preds[i].update_neurons(self.preys)
            PredatorEvolverSimulation.act_on_model(self.preds[i], self.model)

        #for i in range(len(self.preys)):
        #    self.preys[i].update_neurons(self.preds)
        #    PreyEvolverSimulation.act_on_model(self.preys[i], self.model_preys)
        
        if self.playable:
            for i in range(len(self.preys)):
                Game.make_it_move(self.preys[i])
        elif self.model_preys != None:
            for i in range(len(self.preys)):
                self.preys[i].update_neurons(self.preds)
                PreyEvolverSimulation.act_on_model(self.preys[i], self.model_preys)

        for i in range(len(self.preds)):
            pred = self.preds[i]
            pred.move()
            
            pred.energy -= 1
        
        if self.playable:
        
            for i in range(len(self.preys)):
                self.preys[i].move()
        elif self.model_preys != None:
            for i in range(len(self.preys)):
                self.preys[i].move()
            
        
        dead_preys = set()
        for i in range(len(self.preds)):
            for j in range(len(self.preys)):
                if self.preys[j].hits(self.preds[i]) and j not in dead_preys:
                    dead_preys.add(j)
                    self.preds[i].energy += config.ENERGY_ON_MEAL
        
        self.preys = [self.preys[ind] for ind in range(len(self.preys)) if ind not in dead_preys]

        dead_preds = set()
        for i in range(len(self.preds)):
            if self.preds[i].energy < 0:
                dead_preds.add(i)
        
        new_preds = []
        for ind in range(len(self.preds)):
            if ind not in dead_preds:
                new_preds.append(self.preds[ind])
        
        self.preds = new_preds

        if len(self.preys) == 0 or len(self.preds) == 0 or self.time_taken >= config.MAXTIME:
            self.force_end = True
            self.fitness += self.initial_p-len(self.preys)

    
    @staticmethod
    def act_on_model(pred, model):
        arr = np.array(pred.distances + pred.wall_distances +\
            [(pred.speed * pred.dir) / config.PREDATOR_SPEED_LIMIT, (pred.speed * pred.dir.rot90anti()) / config.PREDATOR_SPEED_LIMIT,
            pred.acc/config.PREDATOR_ACCELERATION_LIMIT])

        arr = np.expand_dims(arr.reshape(-1), axis=0)
        # print(len(arr), 2*config.PREY_NEURONS)
        prediction = model.feed_foward(arr)
        # print(prediction)
        # print(prediction)
        if prediction[0][0] < 0.4:
            pred.turn_left()
        elif prediction[0][0] > 0.6:
            pred.turn_right()
        if prediction[1][0] < 0.2:
            pred.decelerate()
        elif prediction[1][0] > 0.6:
            pred.accelerate()

    @staticmethod
    def follow(pred, prey, fraction=0.95):
        pred.speed = (prey.pos - pred.pos).normalized() * (config.SPEED_LIMIT * fraction) 


class PreyEvolverSimulation(Game):
    def __init__(self, model, modelpred, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modelpred = modelpred
        self.model = model
        for i in range(len(self.preds)):
            self.preds[i].pos.x = utils.randint(config.PREY_SPAWN_BOX[0].x, config.PREY_SPAWN_BOX[1].x)
            self.preds[i].pos.y = utils.randint(config.PREY_SPAWN_BOX[0].y, config.PREY_SPAWN_BOX[1].y)
    
    def tick(self):
        if self.time_taken >= config.MAXTIME:
            return

        self.time_taken += 1
        # print(self.time_taken)

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
            PreyEvolverSimulation.act_on_model(self.preys[i], self.model)
        
        for i in range(len(self.preds)):
            self.preds[i].update_neurons(self.preys)
            # PreyEvolverSimulation.follow(self.preds[i], self.preys[0])
            PredatorEvolverSimulation.act_on_model(self.preds[i], self.modelpred)
          
        for i in range(len(self.preys)):
            prey = self.preys[i]
            prey.move()
        
        for i in range(len(self.preds)):
            self.preds[i].move()
        
        dead_preys = set()
        for i in range(len(self.preds)):
            for j in range(len(self.preys)):
                if self.preys[j].hits(self.preds[i]):
                    dead_preys.add(j)
        
        
        self.preys = [self.preys[ind] for ind in range(len(self.preys)) if ind not in dead_preys]
                
        if len(self.preys) == 0 or self.time_taken >= config.MAXTIME:
            self.force_end = True
            self.fitness = len(self.preys)
    
    @staticmethod
    def act_on_model(prey, model):
        arr = np.array(prey.distances + prey.wall_distances +\
            [(prey.speed * prey.dir) / config.PREY_SPEED_LIMIT, (prey.speed * prey.dir.rot90anti()) / config.PREY_SPEED_LIMIT,
            prey.acc/config.PREY_ACCELERATION_LIMIT])

        arr = np.expand_dims(arr.reshape(-1), axis=0)
        # print(len(arr), 2*config.PREY_NEURONS)
        prediction = model.feed_foward(arr)
        # print(prediction)
        if prediction[0][0] < 0.4:
            prey.turn_left()
        elif prediction[0][0] > 0.6:
            prey.turn_right()
        if prediction[1][0] < 0.2:
            prey.decelerate()
        elif prediction[1][0] > 0.6:
            prey.accelerate()

