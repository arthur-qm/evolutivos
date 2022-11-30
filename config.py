from geometry import *

# GENERAL SETTINGS

TITLE = 'PREYDATOR'

# screen size and background color
SIZE = (WIDTH, HEIGHT) = (1200, 700)
BG_COLOR = (128, 128, 128)
DIAGONAL = (WIDTH**2 + HEIGHT**2) ** .5

# sleep before each game's next decision
FPS = 200
TIME_RATE = 1 / FPS


# Screen limit parameters
DX = 30 # offset from right and left
DY = 30 # offset from up and down
LOWX = DX # lowest possible x
LOWY = DY # lowest possibe y
HIGHX = WIDTH - DX # highest possible x
HIGHY = HEIGHT - DY # highest possible y


# Individuals in general
# Reference variables only used in this file
RADIUS = 6
ACCELERATION_LIMIT = 0.03
SPEED_LIMIT = 2
SPEED_MEAN = 0 #SPEED_LIMIT * 0.6
SPEED_NOISE=0
ACCELERATION_MEAN=0 #ACCELERATION_LIMIT*0.6
ACCELERATION_NOISE=0
DIRECTION_VEC_SIZE=3 # screen representation only
DIRECTION_WIDTH=2 # line width of representation
DRAW_DIRECTION=True

# Acceleration decrease/increase // change in turning angle
ACCELERATION_INCREASE = ACCELERATION_LIMIT * 0.2
ACCELERATION_DECREASE = ACCELERATION_INCREASE
ANGLE_INCREASE = 0.03 # --> abrupt x pi change in acceleration angle


# Prey Configuration
PREY_RADIUS = 1.5 * RADIUS
PREY_COLOR = (144, 238, 144)
PREY_ACCELERATION_LIMIT = ACCELERATION_LIMIT
PREY_ACCELERATION_MEAN = ACCELERATION_MEAN
PREY_SPEED_LIMIT = SPEED_LIMIT
PREY_SPEED_MEAN = SPEED_MEAN
# Neurons
PREY_NEURONS = 20
PREY_NEURON_RANGE = 20 * PREY_RADIUS
PREY_NEURON_ANGLES = [2*i/PREY_NEURONS for i in range(PREY_NEURONS)]
# Spawn
PREY_SPAWN_BOX_SIZE = HIGHX-LOWX
PREY_SPAWN_BOX = [Point(LOWX, LOWY),
                  Point(HIGHX, HIGHY)]


# Predator configuration
PREDATOR_RADIUS = 2 * RADIUS
PREDATOR_COLOR = (255, 0, 0)
PREDATOR_ACCELERATION_LIMIT = ACCELERATION_LIMIT
PREDATOR_ACCELERATION_MEAN = ACCELERATION_MEAN
PREDATOR_SPEED_LIMIT = SPEED_LIMIT * 1.5
PREDATOR_SPEED_MEAN = SPEED_MEAN
# Neurons
PREDATOR_NEURONS = 10
PREDATOR_NEURON_RANGE = 225 * RADIUS
PREDATOR_ANGLE_VISION = 1/6
PREDATOR_NEURON_ANGLES = [-PREDATOR_ANGLE_VISION/2 + PREDATOR_ANGLE_VISION/(PREDATOR_NEURONS-1) * i for i in range(PREDATOR_NEURONS)]
NEURON_MULTIPLIER = lambda z: 0 if z == 0 else 3*z+1
# Spawn
PREDATOR_SPAWN_BOX_SIZE = HIGHX-LOWX
PREDATOR_SPAWN_BOX = [Point(LOWX, LOWY),
                      Point(HIGHX, HIGHY)]
# Energy balance
PREDATOR_INITIAL_ENERGY = 3000
PREDATOR_ENERGY_LIMIT = PREDATOR_INITIAL_ENERGY * 1.2
PREDATOR_BODY_MAINTANCE_COST = 2
PREDATOR_SPEED_COST = 0.1
PREDATOR_INITIAL_MASS = PREDATOR_SPEED_COST
MASS_INCREMENT = 0.2 * PREDATOR_INITIAL_MASS
PREDATOR_MAX_DIGESTION_CAPACITY = 400
PREDATOR_DIGESTIVE_INCREASE = 320
PREDATOR_DIGESTION_CONVERSION = 1
PREDATOR_ENERGY_RECOVERY = (PREDATOR_SPEED_LIMIT * PREDATOR_SPEED_COST + PREDATOR_BODY_MAINTANCE_COST) * PREDATOR_DIGESTION_CONVERSION * 3



# Variables which help when determining what the wall vision eye sees
MAX_DIST_TO_PRED = (PREY_NEURON_RANGE**2 + PREDATOR_RADIUS**2) ** .5
MAX_DIST_TO_PREY = (PREDATOR_NEURON_RANGE ** 2 + PREY_RADIUS ** 2) ** .5


# General neurons configuration
DRAW_NEURONS = True
WHICH_NEURONS = 'E' # E for enemies, W for wall. This variable selects what neurons to draw on the screen
NEURON_COLOR = (20, 50, 80)
NEURON_WIDTH = 1

# Game manager
MAXTIME = 10**10 # Very high; impossible to reach

# Wall lines
ACTUAL_LINE_OFFSET = -1

WALL_LINES = [LineSegment(Point(LOWX+ACTUAL_LINE_OFFSET, LOWY+ACTUAL_LINE_OFFSET), Vector(WIDTH, 0)),
              LineSegment(Point(LOWX+ACTUAL_LINE_OFFSET, LOWY+ACTUAL_LINE_OFFSET), Vector(0, HEIGHT)),
              LineSegment(Point(HIGHX-ACTUAL_LINE_OFFSET, HIGHY-ACTUAL_LINE_OFFSET), Vector(-WIDTH, 0)),
              LineSegment(Point(HIGHX-ACTUAL_LINE_OFFSET, HIGHY-ACTUAL_LINE_OFFSET), Vector(0, -HEIGHT))]

# PREY TRAINING
PREY_LAYERS_LIST = [2*PREY_NEURONS+6, 5, 2]
PREY_CAN_CROSS_WALLS = False

# PREDATOR TRAINING
PREDATOR_LAYERS_LIST = [PREDATOR_NEURONS*2+5, 2]
PREDATOR_ACC_LAYER_LIST = []
PRED_CAN_CROSS_WALLS = False
