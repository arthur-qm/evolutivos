import individual
import config
import utils
from pygame.locals import QUIT

class Game:
    def __init__(self, npreds, npreys, broadcast=False, screen=None, upd=None, get_event=None):
        self.preys = [individual.Prey() for _ in range(npreys)]
        self.preds = [individual.Predator() for _ in range(npreds)]
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

