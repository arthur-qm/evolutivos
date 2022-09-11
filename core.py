import pygame
from pygame.locals import *
import config
import utils
import individual

pygame.init()

running = True
screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

demo = individual.Predator()

while running:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        demo.turn_left()
    if keys[pygame.K_RIGHT]:
        demo.turn_right()
    if keys[pygame.K_w]:
        demo.accelerate()
    if keys[pygame.K_s]:
        demo.decelerate()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
    demo.draw(screen)
    utils.sleep(config.TIME_RATE)
    pygame.display.update()
    demo.erase(screen, config.BG_COLOR)
    demo.move()
    # print(demo.dir)
