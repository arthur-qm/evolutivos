from config import *

n_preys = 3

energy = PREDATOR_INITIAL_ENERGY
digestion = 0
max_fitness_val = 0
curr_n_preys = n_preys

# Compute the maximum value for fitness


while curr_n_preys >= 1:
    energy -= PREDATOR_BODY_MAINTANCE_COST
    if digestion > 0:
        energy += PREDATOR_ENERGY_RECOVERY
    digestion -= PREDATOR_DIGESTION_CONVERSION
    if digestion < 0:
        digestion = 0
    if energy > PREDATOR_ENERGY_LIMIT:
        energy = PREDATOR_ENERGY_LIMIT
    max_fitness_val += energy
    if digestion + PREDATOR_DIGESTIVE_INCREASE < PREDATOR_MAX_DIGESTION_CAPACITY:
        if energy + (PREDATOR_ENERGY_RECOVERY - PREDATOR_BODY_MAINTANCE_COST) * (PREDATOR_MAX_DIGESTION_CAPACITY / PREDATOR_DIGESTION_CONVERSION) < PREDATOR_ENERGY_LIMIT:
            curr_n_preys -= 1
            digestion += PREDATOR_DIGESTIVE_INCREASE
    print(energy, digestion)

print(max_fitness_val)
