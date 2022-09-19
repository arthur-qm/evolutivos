from time import sleep
from random import randint, random, seed

# e.g. generates a random velocity from
# (mean-nose) to (mean+noise)
def genrandbynoise(mean, noise):
    return mean*(1-noise) + 2 * noise * mean * random()
