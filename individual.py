import config
import utils
import pygame.draw
from geometry import Vector, Point

"""
Prey and Predator classes inherit individual class
"""

class Individual:
    # Only sets position
    def __init__(self, acc_mean, acc_noise, spd_mean, spd_noise):
        self.pos = Point(\
            utils.randint(config.LOWX, config.HIGHX),\
            utils.randint(config.LOWY, config.HIGHY))
        
        # dir is the direction of the acceleration vector
        # these two variables are separated for a better way to deal with
        # going backwards

        self.dir = Vector.randomunit()
        self.acc = utils.genrandbynoise(acc_mean, acc_noise)

        self.upd_ac_vector()
        
        self.speed = Vector.randomunit(mag=utils.genrandbynoise(spd_mean, spd_noise))
    
    # Only draws circle and direction vector
    def draw(self, screen, direction_enabled=True):
        pygame.draw.circle(screen, self.color, self.pos.L(), self.radius)
        if direction_enabled:
            pygame.draw.line(screen, self.color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)

    # Only erases circle
    def erase(self, screen, erasing_color, direction_enabled=True):
        pygame.draw.circle(screen, erasing_color, self.pos.L(), self.radius)
        if direction_enabled:
            pygame.draw.line(screen, erasing_color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)

    def upd_ac_vector(self):
        self.accvec = Vector.from_direction_and_val(self.dir, self.acc)

    def move(self, acceleration_limit, speed_limit):
        if self.acc > acceleration_limit:
            self.acc = acceleration_limit
        elif self.acc < -acceleration_limit:
            self.acc = -acceleration_limit
        
        self.upd_ac_vector()

        # vector addition
        self.speed += self.accvec

        if self.speed.mag > speed_limit:
            self.speed.setmag(speed_limit)
        
        # actually move
        
        self.pos += self.speed
        
        # Collision with the walls
        if self.pos.x < config.LOWX:
            self.pos.x = config.LOWX
        elif self.pos.x > config.HIGHX:
            self.pos.x = config.HIGHX
        
        if self.pos.y < config.LOWY:
            self.pos.y = config.LOWY
        elif self.pos.y > config.HIGHY:
            self.pos.y = config.HIGHY
    
    def accelerate(self):
        self.acc = self.acc + config.ACCELERATION_INCREASE
        if self.acc >= config.ACCELERATION_LIMIT:
            self.acc = config.ACCELERATION_LIMIT

    def decelerate(self):
        self.acc -= config.ACCELERATION_DECREASE
        if self.acc <= -config.ACCELERATION_LIMIT:
            self.acc = -config.ACCELERATION_LIMIT

    def turn_left(self):
        self.dir = self.dir.rotatedby(config.ANGLE_INCREASE)

    def turn_right(self):
        self.dir = self.dir.rotatedby(-config.ANGLE_INCREASE)
    
    def hits(self, other):
        return (self.pos - other.pos).mag < self.radius + other.radius
    
    


class Prey(Individual):
    def __init__(self):
        super().__init__(config.PREY_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREY_SPEED_MEAN, config.SPEED_NOISE)
        
        self.radius = config.PREY_RADIUS
        self.color = config.PREY_COLOR
    
    def draw(self, screen):
        super().draw(screen)
    
    def erase(self, screen, erasing_color):
        super().erase(screen, erasing_color)
    
    def move(self):
        super().move(config.PREY_ACCELERATION_LIMIT, config.PREY_SPEED_LIMIT)


class Predator(Individual):
    def __init__(self):
        super().__init__(config.PREDATOR_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREDATOR_SPEED_MEAN, config.SPEED_NOISE)
        
        self.radius = config.PREDATOR_RADIUS
        self.color = config.PREDATOR_COLOR
    
    def draw(self, screen):
        super().draw(screen)
    
    def erase(self, screen, erasing_color):
        super().erase(screen, erasing_color)
    
    def move(self):
        super().move(config.PREDATOR_ACCELERATION_LIMIT, config.PREDATOR_SPEED_LIMIT)
