from config import *
import matplotlib.pyplot as plt

def plot_theoretical_limit():
    xs_time = []
    ys_energy = []
    ys_digestion = []
    ys_accumulated_energy = []
    
    n_preys = 7

    energy = PREDATOR_INITIAL_ENERGY
    digestion = 0
    max_fitness_val = 0
    curr_n_preys = n_preys
    curr_time = 0

    # Compute the maximum value for fitness


    while energy >= 0:
        curr_time += 1
        xs_time.append(curr_time)
        ys_energy.append(energy)
        ys_digestion.append(digestion)
        ys_accumulated_energy.append(max_fitness_val + energy)
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
    
    print(max_fitness_val / 10**6)
    ys_accumulated_energy = [acc_en / max_fitness_val * 100 for acc_en in ys_accumulated_energy]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Tempo (núm. de iterações)')
    ax.set_ylabel('Energia')
    ax.plot(xs_time, ys_energy, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax.set_ylim([0, 3700])
    ax2 = ax.twinx()
    ax2.set_ylabel('Acúmulo de energia/Máximo teórico em %', color='red')
    ax2.plot(xs_time, ys_accumulated_energy, color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim([0, 100])
    ax3 = ax.twinx()
    ax3.plot(xs_time, ys_digestion, color='green')
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_ylabel('Digestão')
    ax3.set_ylim([0, 3000])
    ax3.spines['right'].set_position(('outward', 60))
    ax3.spines['right'].set_visible(True)
    ax3.yaxis.set_label_position('right')
    ax3.yaxis.set_ticks_position('right')
    
    figname = 'theoretical_limits.png'

    fig.tight_layout()
    plt.legend()
    plt.savefig(figname)

    plt.show()

if __name__ == '__main__':
    plot_theoretical_limit()