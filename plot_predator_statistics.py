from compute_theoretical_limits import get_theoretical_limit
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
from deap import creator, base
import pickle
import utils
import geometry
import config
import nn
import simulator
import pygame

TL = get_theoretical_limit()

input_hof = 'hof2022-12-02 002058.683055.pkl'


# Fixa a seed
utils.seed(1)

# Número de presas utilizadas na simulação de cálculo de fitness
N_PREYS = 7

SITUATIONS = 30

position_considered = 0

pred_poses = [geometry.Point(utils.randint(config.LOWX, config.HIGHX), 
                            utils.randint(config.LOWY, config.HIGHY)) for _ in range(SITUATIONS)]

positions = [[geometry.Point(utils.randint(config.LOWX, config.HIGHX), 
                            utils.randint(config.LOWY, config.HIGHY)) for _ in range(N_PREYS)] for __ in range(SITUATIONS)]

# initial_angle = geometry.Vector.randomunit()

tested_angles = [geometry.Vector.randomunit() for _ in range(SITUATIONS)]

# rint(positions)

# Aqui, fazemos algumas definições com o deap não porque vamos rodar
# outro algoritmo evolutivo, mas sim porque, ao ler o arquivo com a última 
# geração, ocorre um erro se essas definições não estiverem colocadas.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

with open(input_hof, 'rb') as f:
    ultima_ger = pickle.load(f)

rn = nn.NN(config.PREDATOR_LAYERS_LIST)
rn.set_weights(ultima_ger[0])

game = simulator.PredatorEvolverSimulation(rn, None, False, True, 1, N_PREYS, False)
for i in range(N_PREYS):
    game.preys[i].pos.x = positions[position_considered][i].x
    game.preys[i].pos.y = positions[position_considered][i].y
game.preds[0].pos.x = pred_poses[position_considered].x
game.preds[0].pos.y = pred_poses[position_considered].y
game.preds[0].dir = tested_angles[position_considered]
game.preds[0].upd_ac_vector()

xs_time = []
ys_speed = []
ys_acc = []
ys_energy = []
ys_digestion = []
ys_accumulated_energy = []


while not game.force_end:
    xs_time.append(game.time_taken)
    ys_speed.append(game.preds[0].speed.mag)
    ys_energy.append(game.preds[0].energy)
    ys_digestion.append(game.preds[0].digestion)
    ys_acc.append(game.preds[0].acc)
    ys_accumulated_energy.append(ys_accumulated_energy[-1] + ys_energy[-1] if len(ys_accumulated_energy) > 0 else ys_energy[-1])
    
    game.tick()


ys_accumulated_energy = [ys_accumulated_energy[i] / TL * 100 for i in range(len(ys_accumulated_energy))]

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Tempo (núm. de iterações)')

mode = 1
figname = ''


if mode == 1:
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
    figname = 'fifthlog_gauss1.png'
elif mode == 2:
    ax.set_ylabel('Energia')
    ax.plot(xs_time, ys_energy, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax.set_ylim([0, 3700])
    ax2 = ax.twinx()
    ax2.set_ylabel('Velocidade', color='red')
    ax2.plot(xs_time, ys_speed, color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim([0, 6])
    ax3 = ax.twinx()
    ax3.plot(xs_time, ys_acc, color='green')
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_ylabel('Variável de aceleração "acc"')
    ax3.set_ylim([-0.03, 0.15])
    ax3.spines['right'].set_position(('outward', 60))
    ax3.spines['right'].set_visible(True)
    ax3.yaxis.set_label_position('right')
    ax3.yaxis.set_ticks_position('right')
    figname = 'movimento1.png'

fig.tight_layout()
plt.legend()
plt.savefig(figname)

plt.show()

