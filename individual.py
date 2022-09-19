import config
import utils
import pygame.draw
from geometry import LineSegment, Vector, Point

"""
Prey and Predator classes inherit individual class
"""

class Individual:
    # Only sets position
    def __init__(self, acc_mean, acc_noise, spd_mean, spd_noise, neuron_range, neuron_angles, max_dist_to_opposite):
        self.pos = Point(\
            utils.randint(config.LOWX, config.HIGHX),\
            utils.randint(config.LOWY, config.HIGHY))
        
        # dir is the direction of the acceleration vector
        # these two variables are separated for a better way to deal with
        # going backwards

        self.dir = Vector.randomunit()
        self.acc = utils.genrandbynoise(acc_mean, acc_noise)

        self.upd_ac_vector()

        self.direction_enabled = config.DRAW_DIRECTION
        
        self.draw_neurons = config.DRAW_NEURONS
        self.neuron_range = neuron_range
        self.neuron_angles = neuron_angles

        self.distances = [0 for _ in range(len(neuron_angles))]
        self.max_dist_to_opposite = max_dist_to_opposite

        self.wall_distances = [0 for _ in range(len(neuron_angles))]

        self.speed = Vector.randomunit(mag=utils.genrandbynoise(spd_mean, spd_noise))

        self.fitness = 0
    
    # Only draws circle and direction vector
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.L(), self.radius)
        
        if self.direction_enabled:
            pygame.draw.line(screen, self.color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)

        if self.draw_neurons:
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

        if self.direction_enabled:
            pygame.draw.line(screen, erasing_color, (self.pos + self.dir * self.radius).L(), 
                         (self.pos + self.dir * (self.radius*config.DIRECTION_VEC_SIZE)).L(), width=config.DIRECTION_WIDTH)
        
        if self.draw_neurons:
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

        if self.speed.mag > speed_limit:
            self.speed.setmag(speed_limit)
        
        # actually move
        
        self.pos += self.speed
        
        # Collision with the walls
        if self.pos.x < config.LOWX:
            self.pos.x = config.HIGHX
        elif self.pos.x > config.HIGHX:
            self.pos.x = config.LOWX
        
        if self.pos.y < config.LOWY:
            self.pos.y = config.HIGHY
        elif self.pos.y > config.HIGHY:
            self.pos.y = config.LOWY
    
    def accelerate(self):
        self.acc = self.acc + config.ACCELERATION_INCREASE
        if self.acc >= config.ACCELERATION_LIMIT:
            self.acc = config.ACCELERATION_LIMIT

    def decelerate(self):
        self.acc -= config.ACCELERATION_DECREASE
        if self.acc <= -config.ACCELERATION_LIMIT:
            self.acc = -config.ACCELERATION_LIMIT

    def turn_left(self):
        self.dir = self.dir.rotatedby(-config.ANGLE_INCREASE)

    def turn_right(self):
        self.dir = self.dir.rotatedby(config.ANGLE_INCREASE)
    
    def hits(self, other):
        return (self.pos - other.pos).mag < self.radius + other.radius
    
    def update_neurons(self, opposites):
        
        # for the distances to opposites:
        # 1 = opposite very close
        # 0 = nothing

        for i in range(len(self.neuron_angles)):
            self.distances[i] = 0
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
                        # print(f'Increasing {i} because {self.dir} {self.neuron_angles[i]} {self.dir.rotatedby(self.neuron_angles[i])} {neuron_perp_vector} {distance_vector}')
                #if self.distances[i]:
                #    print(f'Detect enemy {self.distances[i]:.5f}')
        # for the distance to the walls
        # 1 = right next to them
        # 0 = cant see them

        for i in range(len(self.neuron_angles)):
            neuron_vector = self.dir.rotatedby(self.neuron_angles[i]) * self.neuron_range

            for j in range(len(config.WALL_LINES)):
                curr_line = config.WALL_LINES[j]
                dist = LineSegment(self.pos, neuron_vector).dist(curr_line)
                
                if dist == -1 or dist > self.neuron_range:
                    continue
                
                self.wall_distances[i] = max(self.wall_distances[i], 1-dist/self.neuron_range)
        
    def decision(self, what):
        turning = utils.random()
        accel = utils.random()

        if turning < 0.2:
            self.turn_left()
        elif turning > 0.7:
            self.turn_right()
        
        if accel < 0.3:
            self.decelerate()
        elif accel > 0.8:
            self.accelerate()
                

class Prey(Individual):
    def __init__(self):
        super().__init__(config.PREY_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREY_SPEED_MEAN, config.SPEED_NOISE, config.PREY_NEURON_RANGE,
                         config.PREY_NEURON_ANGLES, config.MAX_DIST_TO_PRED)
        
        self.radius = config.PREY_RADIUS
        self.color = config.PREY_COLOR
    
    def move(self):
        super().move(config.PREY_ACCELERATION_LIMIT, config.PREY_SPEED_LIMIT)


class Predator(Individual):
    def __init__(self):
        super().__init__(config.PREDATOR_ACCELERATION_MEAN, config.ACCELERATION_NOISE, 
                         config.PREDATOR_SPEED_MEAN, config.SPEED_NOISE, config.PREDATOR_NEURON_RANGE,
                         config.PREDATOR_NEURON_ANGLES, config.MAX_DIST_TO_PREY)
        
        self.radius = config.PREDATOR_RADIUS
        self.color = config.PREDATOR_COLOR
    
    def move(self):
        super().move(config.PREDATOR_ACCELERATION_LIMIT, config.PREDATOR_SPEED_LIMIT)
