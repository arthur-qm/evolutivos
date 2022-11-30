"""

Após ter rodado o script evolve_predator.py, foi gerado um arquivo .pkl
contendo a última geração.
Neste script visualizamos como essa última geração se comporta.

"""


import pickle
import simulator
import pygame
from deap import creator, base
import nn
import config
import geometry
import utils

# Fixa a seed
utils.seed(0)

# Número de presas utilizadas na simulação de cálculo de fitness
N_PREYS = 7

SITUATIONS = 30

pred_poses = [geometry.Point(utils.randint(config.LOWX, config.HIGHX), 
                            utils.randint(config.LOWY, config.HIGHY)) for _ in range(SITUATIONS)]

positions = [[geometry.Point(utils.randint(config.LOWX, config.HIGHX), 
                            utils.randint(config.LOWY, config.HIGHY)) for _ in range(N_PREYS)] for __ in range(SITUATIONS)]

# initial_angle = geometry.Vector.randomunit()

tested_angles = [geometry.Vector.randomunit() for _ in range(SITUATIONS)]

print(positions)

# Aqui, fazemos algumas definições com o deap não porque vamos rodar
# outro algoritmo evolutivo, mas sim porque, ao ler o arquivo com a última 
# geração, ocorre um erro se essas definições não estiverem colocadas.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

with open('hof.pkl', 'rb') as f:
    ultima_ger = pickle.load(f)

# Nós definimos a fitness "final" de um indivíduo como a média da fitness "por simulação"
# ao longo de 3 simulações, cada uma delas aleatória. Por isso, pode ser que um indivíduo
# 'sortudo', mesmo sendo 'pior' que outro 'azarado' tenha ficado com fitness maior

# Por isso, utilizo a função look_for_true_best para, dentro dessa última geração,
# procurar aquele indivíduo que é verdadeiramente o melhor.

# Como não é possível ser determinístico quanto a isso, o que eu faço é rodar
# 7 simulações (ao invés de 3) para cada indivíduo para tentar ser mais acurado 

look_for_true_best = False
test_best_on_trained_setting = True
true_best = 1
true_best_mean_score = 0

if look_for_true_best:
    
    rn = nn.NN(config.PREDATOR_LAYERS_LIST)

    for i in range(len(ultima_ger)-1, -1, -1):
        print(f'Testando {len(ultima_ger)-i}/{len(ultima_ger)}')
        rn.set_weights(ultima_ger[i])
        score = 0
        for j in range(SITUATIONS):
            game = simulator.PredatorEvolverSimulation(rn, None, False, False, 1, 7, False, None, None, None)
            for i in range(N_PREYS):
                game.preys[i].pos.x = positions[i].x
                game.preys[i].pos.y = positions[i].y
            game.preds[0].pos.x = pred_poses[j].x
            game.preds[0].pos.y = pred_poses[j].y
            game.preds[0].dir = tested_angles[j]
            game.preds[0].upd_ac_vector()

            game.start()
            score += game.fitness
            print(f'{game.fitness/10**6} milhões nessa simulação')
            game.fitness = 0
        score /= SITUATIONS
        print(f'Consegui um score {score}')
        if score > true_best_mean_score:
            true_best = i
            print(f'Isso substitui o recorde que era {true_best_mean_score}')
            true_best_mean_score = score
            


# Mostra o índice no vetor da geração que é verdadeiramente melhor e seu score

print(true_best, true_best_mean_score)

# Setup inicial do pygame

pygame.init()

screen = pygame.display.set_mode(config.SIZE)
pygame.display.set_caption(config.TITLE)
screen.fill(config.BG_COLOR)

pygame.display.update()

# cria a rede neural e seta os pesos e biases para os do melhor indivíduo da última geração
rn = nn.NN(config.PREDATOR_LAYERS_LIST)
rn.set_weights(ultima_ger[true_best])
print(ultima_ger[true_best])

# Inicia a simulação para um predador com o cérebro do indivíduo de maior fitness e 5 presas paradas
# A simulação é mostrada na tela

media = 0

if test_best_on_trained_setting:
    for j in range(len(tested_angles)):
        # print(j)
        game = simulator.PredatorEvolverSimulation(rn, None, False, True, 1, N_PREYS, True, screen, pygame.display.update, pygame.event.get)
        for i in range(N_PREYS):
            game.preys[i].pos.x = positions[j][i].x
            game.preys[i].pos.y = positions[j][i].y
        game.preds[0].pos.x = pred_poses[j].x
        game.preds[0].pos.y = pred_poses[j].y
        game.preds[0].dir = tested_angles[j]
        game.preds[0].upd_ac_vector()
        game.start()
        media += game.fitness
        print(game.fitness)

# Ao final da simulação, mostra a fitness dessa simulação em particular
print(media/len(tested_angles))
