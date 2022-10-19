"""

RUN THIS SCRIPT LIKE THIS:

python test.py test num_of_preys num_of_preds 0_for_prey_1_for_pred 0_for_others_cant_move_1_for_can
i.e. : python test.py test 4 2 0 0 
begins a game where you control a prey and there are 4 preys and 2 predators; Also, everyone else cant move

python test.py observe num_of_preys num_of_preds one_for_broadcast
i.e. : python test.py observe 3 3 1
begins a game where there are 3 preys and 3 preds. Since the last argument is one, its possible to see the gaming running in a screen
If it were zero, then the game would run silently

"""


import pygame
from pygame.locals import *
import config
import utils
import individual
import sys
import simulator


def follow(prey):
    def decision(self):
        self.speed = (prey.pos - self.pos).normalized() * (config.SPEED_LIMIT )
        self.acc = 0
    return decision


if sys.argv[1] == 'test':

    preys, preds, controlled, movable = map(int, sys.argv[2:])

    pygame.init()

    running = True
    screen = pygame.display.set_mode(config.SIZE)
    pygame.display.set_caption(config.TITLE)
    screen.fill(config.BG_COLOR)

    pygame.display.update()

    if controlled and preds == 0:
        print('How come you want to control a predator and yet you say there\'s no predator')
    if (not controlled) and preys == 0:
        print('Whyy do you want to control preys if there aren\'t any')
    
    if controlled:
        demo = individual.Predator()
        preds -= 1
    else:
        demo = individual.Prey()
        preys -= 1
    
    preys_array = [individual.Prey() for _ in range(preys)]
    preds_array = [individual.Predator() for _ in range(preds)]


    while running:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            demo.turn_left()
        if keys[pygame.K_RIGHT]:
            demo.turn_right()
        if keys[pygame.K_UP]:
            demo.accelerate()
        if keys[pygame.K_DOWN]:
            demo.decelerate()
        if keys[pygame.K_q]:
            pygame.quit()
            break
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
        demo.draw(screen)
        
        for prey in preys_array:
            prey.draw(screen)

        for pred in preds_array:
            pred.draw(screen)

        utils.sleep(config.TIME_RATE)
        pygame.display.update()
        
        demo.erase(screen)
        if controlled:
            demo.update_neurons(preys_array)
        else:
            demo.update_neurons(preds_array)
        
        demo.move()

        for prey in preys_array:
            prey.erase(screen)
            if movable:
                prey.update_neurons(preds_array if controlled else preds_array + [demo])
                prey.move()
        
        for pred in preds_array:
            pred.erase(screen)
            if movable:
                pred.update_neurons(preys_array if controlled else preys_array + [demo])
                pred.move()
        

        
        # other2.update_neurons([other, demo])
        # pygame.draw.line(screen, (0, 0, 255), other.pos.L(), (other.pos + (demo.pos-other.pos)).L())
        # print(demo.dir)

elif sys.argv[1] == 'observe':

    preys, preds, broadcast = map(int, sys.argv[2:])

    if broadcast:
        pygame.init()
    
        screen = pygame.display.set_mode(config.SIZE)
        pygame.display.set_caption(config.TITLE)
        screen.fill(config.BG_COLOR)
    
        pygame.display.update()
    else:
        screen = None

    game = simulator.Game(preys, preds, broadcast, screen, pygame.display.update, pygame.event.get)
    game.start()
elif sys.argv[1] == 'run':

    pygame.init()

    running = True
    screen = pygame.display.set_mode(config.SIZE)
    pygame.display.set_caption(config.TITLE)
    screen.fill(config.BG_COLOR)

    pygame.display.update()
    
    demo = individual.Prey()
    rival = individual.Predator()
    rival.decision = follow(demo)


    while running:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            demo.turn_left()
        if keys[pygame.K_RIGHT]:
            demo.turn_right()
        if keys[pygame.K_UP]:
            demo.accelerate()
        if keys[pygame.K_DOWN]:
            demo.decelerate()
        if keys[pygame.K_q]:
            pygame.quit()
            break
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
        demo.draw(screen)
        
        rival.draw(screen)

        utils.sleep(config.TIME_RATE)
        pygame.display.update()
        
        demo.erase(screen)
        
        rival.erase(screen)
        
        demo.move()
        rival.decision(rival)
        rival.move()
        # print(demo.speed.mag, rival.speed.mag)
