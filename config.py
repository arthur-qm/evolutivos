# GENERAL SETTINGS

TITLE = 'PREYDATOR'

# screen size and background color
SIZE = (WIDTH, HEIGHT) = (800, 800)
BG_COLOR = (128, 128, 128)

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
ACCELERATION_LIMIT = 0.1
SPEED_LIMIT = 2
SPEED_MEAN = SPEED_LIMIT * 0.6
SPEED_NOISE=0.1
ACCELERATION_MEAN=ACCELERATION_LIMIT*0.6
ACCELERATION_NOISE=0.1
DIRECTION_VEC_SIZE=3 # screen representation only
DIRECTION_WIDTH=2 # line width of representation

# Acceleration decrease/increase // change in turning angle
ACCELERATION_INCREASE = ACCELERATION_MEAN / 100
ACCELERATION_DECREASE = ACCELERATION_INCREASE * 1.1
ANGLE_INCREASE = 0.005 # --> abrupt x pi change in acceleration angle


# Prey Configuration
PREY_RADIUS = 1.5 * RADIUS
PREY_COLOR = (144, 238, 144)
PREY_ACCELERATION_LIMIT = ACCELERATION_LIMIT
PREY_ACCELERATION_MEAN = ACCELERATION_MEAN
PREY_SPEED_LIMIT = SPEED_LIMIT
PREY_SPEED_MEAN = SPEED_MEAN

# Predator configuration
PREDATOR_RADIUS = 2 * RADIUS
PREDATOR_COLOR = (255, 0, 0)
PREDATOR_ACCELERATION_LIMIT = ACCELERATION_LIMIT
PREDATOR_ACCELERATION_MEAN = ACCELERATION_MEAN
PREDATOR_SPEED_LIMIT = SPEED_LIMIT
PREDATOR_SPEED_MEAN = SPEED_MEAN
