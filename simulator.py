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
                    self.time_taken = config.MAXTIME
                    return

        for i in range(len(self.preys)):
            self.preys[i].move()
        
        for i in range(len(self.preds)):
            self.preds[i].move()
        
        self.preys = list(filter(lambda prey: all(not prey.hits(pred) for pred in self.preds), self.preys))

    def start(self):
        while self.time_taken < config.MAXTIME:
            self.tick()

