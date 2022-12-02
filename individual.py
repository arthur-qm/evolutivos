"""

Em simulator.py eu trabalho com os indivíduos, que podem ser "presas" ou "predadores"
Neste arquivo eu defino essas classes.

"""


import config
import utils
import pygame.draw
from geometry import LineSegment, Vector, Point

"""
Prey and Predator classes inherit individual class
"""

class Individual:
    
    """
    Creates an Individual at a random position, with a given initial variables
    Each individual has a vision reach (passed as 'neuron_range' in __init__), and 
    "neuron" angles which tells angle from the "direction" vector for each of the "vision rays"
    of the individual 

    "max_dist_to_opposite" will be explained later, but it basically helps when detecting the collision
    of the line segment and another individual

    if "crosses walls" is enabled, then, when an individual touches some wall, it gets teleported to the
    opposite wall

    (note: As of 16/10/2022, the noise is set as zero in the config.py file.)
    In any case, all this "noise" and "mean" do is to set the initial acceleration/speed as a "mean" plus a "displacement" (called noise) from the mean.

    "Neuron range" measures how far away the individual can "see"
    

    """
    
    def __init__(self, acc_mean, acc_noise, spd_mean, spd_noise, neuron_range, neuron_angles, max_dist_to_opposite, crosses_walls, mass, acc_limit, spd_limit):
        self.pos = Point(\
            utils.randint(config.LOWX, config.HIGHX),\
            utils.randint(config.LOWY, config.HIGHY))
        
        # dir is the direction of the acceleration vector
        # these two variables (self.dir and self.acc) are separated for a better way to deal with
        # going backwards
        self.dir = Vector.randomunit()
        self.acc = utils.genrandbynoise(acc_mean, acc_noise)
        
        # it keeps computing the acceleration vector by multiplying self.acc and self.dir
        self.upd_ac_vector()
        
        self.neuron_range = neuron_range
        self.neuron_angles = neuron_angles

        # the 'distances' list stores the result of a calculation involving
        # the distance from the individual to other individual along a given
        # vision ray
        self.distances = [0 for _ in range(len(neuron_angles))]

        # same as distances but considers distances to walls rather than other individuals
        self.wall_distances = [0 for _ in range(3)]

        # Precomputed number for helping in calculating distances and wall distances
        self.max_dist_to_opposite = max_dist_to_opposite

        # generate random unit speed vector considering noise
        self.speed = Vector.randomunit(mag=utils.genrandbynoise(spd_mean, spd_noise))

        self.fitness = 0

        self.wall_crosser = crosses_walls

        self.mass = mass

        self.acc_limit = acc_limit

        self.spd_limit = spd_limit
    
    # Only draws circle and direction vector
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.L(), self.radius)
        
        if config.DRAW_DIRECTION:
            pygame.draw.line(screen, self.color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)

        if config.DRAW_NEURONS:
            for i in range(len(self.neuron_angles)):
                angle = self.neuron_angles[i]

                if config.WHICH_NEURONS == 'E' and self.distances[i] == 0:
                    thecolor = config.NEURON_COLOR
                elif config.WHICH_NEURONS == 'W' and self.wall_distances[i] == 0:
                    thecolor = config.NEURON_COLOR
                else:
                    thecolor = (255, 0, 0)
                pygame.draw.line(screen, thecolor, self.pos.L(), (self.pos + self.dir.rotatedby(angle) * self.neuron_range).L(), width=config.NEURON_WIDTH)

    # Only erases circle
    def erase(self, screen, erasing_color=config.BG_COLOR):
        pygame.draw.circle(screen, erasing_color, self.pos.L(), self.radius)

        if config.DRAW_DIRECTION:
            pygame.draw.line(screen, erasing_color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)
        
        if config.DRAW_NEURONS:
            for angle in self.neuron_angles:
                pygame.draw.line(screen, erasing_color, self.pos.L(), (self.pos + self.dir.rotatedby(angle) * self.neuron_range).L(), width=config.NEURON_WIDTH)

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

        if self.speed.mag > self.spd_limit:
            self.speed.setmag(self.spd_limit)
        
        # actually move
        
        self.pos += self.speed
        
        # Collision with the walls
        if self.pos.x < config.LOWX:
            self.pos.x = config.HIGHX if self.wall_crosser else config.LOWX
        elif self.pos.x > config.HIGHX:
            self.pos.x = config.LOWX if self.wall_crosser else config.HIGHX
        
        if self.pos.y < config.LOWY:
            self.pos.y = config.HIGHY if self.wall_crosser else config.LOWY
        elif self.pos.y > config.HIGHY:
            self.pos.y = config.LOWY if self.wall_crosser else config.HIGHY
    
    def accelerate(self):
        self.acc = self.acc + config.ACCELERATION_INCREASE
        if self.acc >= self.acc_limit:
            self.acc = self.acc_limit

    def decelerate(self):
        self.acc -= config.ACCELERATION_DECREASE
        if self.acc <= -self.acc_limit:
            self.acc = -self.acc_limit

    def turn_left(self):
        self.dir = self.dir.rotatedby(-config.ANGLE_INCREASE)

    def turn_right(self):
        self.dir = self.dir.rotatedby(config.ANGLE_INCREASE)
    
    def hits(self, other):
        return (self.pos - other.pos).mag < self.radius + other.radius
    

    """
    Given an array of individuals which may be on the field of view of this individual,
    this function updates the values of self.distances
    It also updates self.wall_distances
    """
    def update_neurons(self, opposites):
        

        for i in range(len(self.neuron_angles)):
            self.distances[i] = 0
        for i in range(3):
            self.wall_distances[i] = 0

        for opposite in opposites:
            if opposite.pos.dist(self.pos) > self.neuron_range:
                continue
            distance_vector = opposite.pos - self.pos

            for i in range(len(self.neuron_angles)):
                neuron_perp_vector = self.dir.rotatedby(self.neuron_angles[i]).rot90anti()

                dist_to_line = distance_vector * neuron_perp_vector
                if abs(dist_to_line) <= opposite.radius:
                    # We know the line passing through the center of self and the current
                    # neuron vector passes through the opposite individual. But we want the
                    # intersection to the segment, not the line
                    # so I need to check the semiplane in which the opposite center is
                    # so for this I use the cross product

                    if neuron_perp_vector ^ distance_vector < 0:
                        # We want: distance = radius sum --> 1
                        #          distance = maxdist --> 0
                        # (distance-radius sum) / (maxdist - radius_sum) gives the opposite so
                        self.distances[i] = max(self.distances[i], 
                        1-(distance_vector.mag-(self.radius+opposite.radius))/(self.max_dist_to_opposite - (self.radius+opposite.radius)))

        for i in range(len(self.neuron_angles)):
            self.distances[i] = config.NEURON_MULTIPLIER(self.distances[i])
        
        
        # for the distance to the walls
        # 1 = right next to them
        # 0.5 = intermediary distance
        # 0 = cant see them

        for i in range(len(self.wall_distances)):
            neuron_vector = self.dir.rotatedby(config.PREDATOR_NEURON_WALL_ANGLES[i]) * self.neuron_range

            for j in range(len(config.WALL_LINES)):
                curr_line = config.WALL_LINES[j]
                dist = LineSegment(self.pos, neuron_vector).dist(curr_line)
                
                if dist == -1 or dist > self.neuron_range:
                    continue
                
                self.wall_distances[i] = max(self.wall_distances[i], 1-dist/self.neuron_range)
        


    def decision(self, what):
        turning = utils.random()
        accel = utils.random()

        if turning < 0.3:
            self.turn_left()
        elif turning > 0.7:
            self.turn_right()
        
        if accel < 0.3:
            self.decelerate()
        elif accel > 0.7:
            self.accelerate()
                

class Prey(Individual):
    def __init__(self):
        super().__init__(config.PREY_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREY_SPEED_MEAN, config.SPEED_NOISE, config.PREY_NEURON_RANGE,
                         config.PREY_NEURON_ANGLES, config.MAX_DIST_TO_PRED, config.PREY_CAN_CROSS_WALLS, 0, 
                         config.PREY_ACCELERATION_LIMIT, config.PREY_SPEED_LIMIT)
        
        self.radius = config.PREY_RADIUS
        self.color = config.PREY_COLOR
    
    def move(self):
        super().move(config.PREY_ACCELERATION_LIMIT, config.PREY_SPEED_LIMIT)


class Predator(Individual):
    def __init__(self):
        super().__init__(config.PREDATOR_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREDATOR_SPEED_MEAN, config.SPEED_NOISE, config.PREDATOR_NEURON_RANGE,
                         config.PREDATOR_NEURON_ANGLES, config.MAX_DIST_TO_PREY, config.PRED_CAN_CROSS_WALLS,
                         config.PREDATOR_INITIAL_MASS, config.PREDATOR_ACCELERATION_LIMIT, config.PREDATOR_SPEED_LIMIT)
        
        self.radius = config.PREDATOR_RADIUS
        self.color = config.PREDATOR_COLOR
    
    def move(self):
        super().move(config.PREDATOR_ACCELERATION_LIMIT, config.PREDATOR_SPEED_LIMIT)
