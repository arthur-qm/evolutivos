import pygame
from pygame.locals import *
import config
import utils
import individual
import sys


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
        utils.sleep(config.TIME_RATE)
        pygame.display.update()
        demo.erase(screen, config.BG_COLOR)
        demo.move()
        # print(demo.dir)
