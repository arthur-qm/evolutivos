from config import *

def get_theoretical_limit():
    n_preys = 7

    energy = PREDATOR_INITIAL_ENERGY
    digestion = 0
    max_fitness_val = 0
    curr_n_preys = n_preys

    # Compute the maximum value for fitness


    while energy >= 0:
        energy -= PREDATOR_BODY_MAINTANCE_COST
        if digestion > 0:
            energy += PREDATOR_ENERGY_RECOVERY
        digestion -= PREDATOR_DIGESTION_CONVERSION
        if digestion < 0:
            digestion = 0
        if energy > PREDATOR_ENERGY_LIMIT:
            energy = PREDATOR_ENERGY_LIMIT
        max_fitness_val += energy
        if curr_n_preys >= 1 and digestion == 0 and energy + 320 * (PREDATOR_ENERGY_RECOVERY - PREDATOR_BODY_MAINTANCE_COST) <= PREDATOR_ENERGY_LIMIT:
            curr_n_preys -= 1
            digestion += PREDATOR_DIGESTIVE_INCREASE
        if digestion > PREDATOR_MAX_DIGESTION_CAPACITY:
            digestion = PREDATOR_MAX_DIGESTION_CAPACITY
    
    return max_fitness_val

print(get_theoretical_limit() / 10**6)
