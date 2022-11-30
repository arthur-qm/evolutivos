"""

A partir de outros arquivos já criados: simulator.py, config.py, utils.py e nn.py,
esse script utiliza o módulo deap para rodar um algoritmo evolutivo que visa maximizar
a fitness da simulação simulator.PredatorEvolverSimulator para um dado número de presas
e que roda durante um dado número de gerações (modifique as variáveis N_PREYS e N_GEN)

No que se refere ao que foi feito até o dia 16/10/22, evoluímos um "predador" para caçar
presas num cenário de dimensões (1200, 700) (e com  outras informações no arquivo config.py)
que estão PARADAS. É possível pensar no que foi feito até agora como um herbívoro que caça
alfaces em um ritmo/"estratégia" que maximiza sua fitness.

"""

import numpy as np
from deap import base, creator, tools, algorithms
import geometry
import config
import simulator
import utils
import pickle
import nn
import multiprocessing

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

print(pred_poses)
print(positions)

# Número de gerações
N_GEN = 50

"""
Dado uma lista de floats, que é que o deap acha que é o indivíduo, utilizamos a função evaluate
para calcular a fitness desse indivíduo
"""

def evaluate(individual_brain):
    """
    o deap acha que o indivíduo é uma lista de floats
    Mas cada float dessa lista tem um significado especial: essa lista na verdade
    é a lista de weights e biases associada à rede neural do predador

    Predador "ótimo" é aquele que possuirá a maior fitness ao rodar uma simulação completa

    Defini fitness como a soma dos valores de "energia" desse predador para cada instante de tempo.
    Então, como a energia inicial é da ordem dos milhares e a simulação geralmente dura por vários instantes de
    tempo (cada instante de tempo chama-se 'tick'), então a fitness é um número da ordem dos milhões ou dezenas de milhões (10^6/10^7)

    """
    
    model = nn.NN(config.PREDATOR_LAYERS_LIST) # instancia uma rede neural, criada com weights e biases aleatórios
    model.set_weights(individual_brain) # modifica esses valores aleatórios para os especificados pela lista de floats 'individual_brain'
    
    # Rodar 3 simulações e pegar a fitness média considerando todas elas
    
    media = 0

    for j in range(len(tested_angles)):
        game = simulator.PredatorEvolverSimulation(model, None, False, False, 1, N_PREYS)
        for i in range(N_PREYS):
            game.preys[i].pos.x = positions[j][i].x
            game.preys[i].pos.y = positions[j][i].y
        game.preds[0].pos.x = pred_poses[j].x
        game.preds[0].pos.y = pred_poses[j].y
        game.preds[0].dir = tested_angles[j]
        game.preds[0].upd_ac_vector()
        game.start()
        media += game.fitness

    return (media/len(tested_angles),)


# No arquivo de configurações, a lista de inteiros "config.PREDATOR_LAYERS_LIST" é tal que
# o seu primeiro elemento indica o número de neurônios da camada de entrada (que representa o número de 
# valores de 'entrada' da rede neural). O elemento seguinte indica a quantidade de neurônios da
# primeira hidden layer. E assim por diante, até que o último  elemento indica a quantidade de
# neurônios da output layer, a qual, em particular, representa o número de valores de 'saída' da rede neural

# instancia uma rede neural com pesos e biases aleatórios (não vamos utilizá-la)
model = nn.NN(config.PREDATOR_LAYERS_LIST) 

# só instanciamos essa rede neural para acharmos o valor de "model.params"
# esse 'params' é um inteiro calculado a partir da lista config.PREDATOR_LAYERS_LIST
# e representa a quantidade total de valores de peso e valores de biases da rede neural
ind_size = model.params 
print(ind_size)

# Sendo assim, note que existe uma correspondência biunívoca entre listas de floats de tamanho
# 'model.params' e as redes neurais cujos números de neurônios por camadas estão descritos pela
# lista config.PREDATOR_LAYERS_LIST

# Começa o setup do deap
# Criamos a classe FitnessMax para o nosso problema de maximização de fitness
creator.create('FitnessMax', base.Fitness, weights=(1.0,))

# Cria uma classe indivíduo que deriva se origina de uma lista (de fato, cada indivíduo vai ser uma
# lista de floats) e tem como atributo 'fitness' a classe FitnessMax que acabou de ser criada.
creator.create('Individual', list, fitness=creator.FitnessMax)

# essa toolbox é literalmente uma 'caixa de ferramentas' que nos permite fazer as configurações
# para o nosso problema em particular
toolbox = base.Toolbox()

# Cria a função toolbox.weight_bin, a qual retorna um número aleatório de -1 até 1
toolbox.register('weight_bin', lambda: 2*utils.random()-1)

# Cria a função toolbox.individual, a qual retorna uma instância da classe creator.Individual que já criamos
# Como essa classe é baseada em uma lista, os parâmetros toolbox.weight_bin e n=ind_size fazem com que
# seja criado um indivíduo que é representado por uma lista de 'ind_size' floats em que cada valor é um
# número aleatório de -1 até 1
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.weight_bin, n=ind_size)

# A função toolbox.population retorna uma lista de indivíduos, cada um deles criado pela função toolbox.individual
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

# A função toolbox.mate é responsável pelo cruzamento (crossing-over), que vai
# cruzar dois indivíduos (duas listas de floats)
# Eu escolhi o algoritmo de crossing over "cxUniform", o qual gera uma lista de
# duas floats "filhas" de outras duas listas de floats. Ele funciona percorrendo as listas
# e pra cada posição, troca os elementos correspondentes a mesma posição de cada uma das listas
# originais com probabilidade indpb, especificada abaixo
toolbox.register('mate', tools.cxUniform, indpb=0.7)

# A função toolbox.mutate é responsável pela mutação de indivíduos. Foi utilizado
# o algoritmo de mutação para floats "tools.mutGaussian". Será definido mais abaixo
# a chance de ocorrer mutação em um indivíduo. Mas, caso ela ocorra, será da seguinte forma:
# Para cada atributo, existe uma probabilidade indpb de acontecer uma mutação nele
# Quando essa mutação ocorre, o valor se transforma conforme cuja distribuição de valores é centrada em 'mu'
# e possui desvio padrão 'sigma'
toolbox.register('mutate', tools.mutGaussian, indpb=0.7, mu=0, sigma=0.7) # ver se funciona pra real

# A função toolbox.select é responsável por selecionar os indivíduos para a próxima geração
# Em particular, tools.selTournament funciona assim:
# Ela seleciona vários grupos de 'tournsize' indivíduos aleatórios da geração anterior e
# para cada grupinho, seleciona o com maior fitness
toolbox.register('select', tools.selTournament, tournsize=4)

# A função toolbox.evaluate é definida como a função evaluate, escrita na parte de cima
# desse mesmo arquivo que você está lendo. Ela retorna a fitness e já foi explicada em sua 
# definição
toolbox.register('evaluate', evaluate)

# Como cada simulação tem milhares de ticks e são centenas de indivíduos e dezenas de gerações,
# utilizo multithreading para acelerar
pool = multiprocessing.Pool()
toolbox.register('map', pool.map)


# Para acompanhar o desenvolvimento do algoritmo, uso o tools.Statistics
# assim, ao fim de cada geração, são mostrados na tela informações como o
# maior valor de fitness, a média, etc
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register('Max', np.max)
stats.register('Min', np.min)
stats.register('Mean', np.mean)
stats.register('Std', np.std)
stats.register('25%', lambda arr: np.percentile(arr, 25))
stats.register('Median', np.median)
stats.register('75%', lambda arr: np.percentile(arr, 75))

# Criar tambem historico
history = tools.History()
toolbox.decorate('mate', history.decorator)
toolbox.decorate('mutate', history.decorator)

# Cria uma população inicial de 20 indivíduos
pop = toolbox.population(n=20)
history.update(pop)

# Cria um hall of fame
hof = tools.HallOfFame(1)

# algorithms.eaSimple roda o algoritmo genético mais simples
# Retorna a população da última geração e as estatísticas de toda a evolução
# cxpb = probabilidade de cruzar 2 indivíduos
# mutpb = probabilidade de um indivíduo mutar

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.03, ngen=N_GEN, stats=stats, halloffame=hof)

# Ordena a população da última geração pela fitness
pops = sorted(pop, key=lambda ind: ind.fitness, reverse=True)

# Printa (novamente) os dados da evolução de todas as gerações
print(log)

# Guarda a última geração num arquivo
# Assim, é possível ver como ela desempenha

from datetime import datetime as dt

with open(f"last_generation{dt.today()}.pkl", "wb") as cp_file:
    pickle.dump(pops, cp_file)

with open(f'history{dt.today()}.pkl', 'wb') as cp_file:
    pickle.dump(history, cp_file)

with open(f'hof{dt.today()}.pkl', 'wb') as cp_file:
    pickle.dump(hof, cp_file)



with open(f'log{dt.today()}.pkl', 'wb') as cp_file:
    pickle.dump(log, cp_file)
