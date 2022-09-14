import pygame
from pygame.locals import *
import config
import utils
import individual
import sys
import simulator

if sys.argv[1] == 'test':
    pygame.init()

    running = True
    screen = pygame.display.set_mode(config.SIZE)
    pygame.display.set_caption(config.TITLE)
    screen.fill(config.BG_COLOR)

    pygame.display.update()

    if sys.argv[2][0] == '1':
        demo = individual.Predator()
        
    else:
        demo = individual.Prey()
        other = individual.Predator()

    others = [individual.Prey() for _ in range(3)]

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
        
        for other in others:
            other.decision()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
        demo.draw(screen)
        for other in others:
            other.draw(screen)
        utils.sleep(config.TIME_RATE)
        pygame.display.update()
        demo.erase(screen)
        for other in others:
            other.erase(screen)
        demo.move()
        other.update_neurons([])
        demo.update_neurons([])
        # other2.update_neurons([other, demo])
        # pygame.draw.line(screen, (0, 0, 255), other.pos.L(), (other.pos + (demo.pos-other.pos)).L())
        # print(demo.dir)

elif sys.argv[1] == 'o':
    pygame.init()

    running = True
    screen = pygame.display.set_mode(config.SIZE)
    pygame.display.set_caption(config.TITLE)
    screen.fill(config.BG_COLOR)

    pygame.display.update()

    game = simulator.Game(5, 50, True, screen, pygame.display.update, pygame.event.get)
    game.start()
    


