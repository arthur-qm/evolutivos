import numpy as np
from math import exp

def sigmoid(x):
    return 1/(1 + exp(-x))

sigmoid_vec = np.vectorize(sigmoid)

class NN:
    def __init__(self, layer_list):
        self.weights = []
        self.biases = []
        self.ll = layer_list
        self.params = 0

        for i in range(len(layer_list)-1):
            new_weights = (2*np.random.rand(layer_list[i+1], layer_list[i])-1)
            self.params += layer_list[i+1] * layer_list[i] + layer_list[i+1]

            self.weights.append(new_weights)
            self.biases.append((2*np.random.rand(layer_list[i+1], 1)-1)/10)

    def feed_foward(self, input_list):
        input_list = input_list.reshape((-1, 1))
        # print('a')
        # print(input_list)
        for i in range(len(self.weights)):
            # print('start')
            # print(self.weights[i])
            # print('times')
            # print(input_list)
            input_list = np.matmul(self.weights[i], input_list)
            # print('equals')
            # print(input_list)
            input_list = sigmoid_vec(input_list + self.biases[i])
            # print('sigmoided')
            # print(input_list)
        # print('final return')
        # print(input_list)
        return input_list

    def set_weights(self, weights):
        self.weights = []
        self.biases = []

        for i in range(len(self.ll)-1):
            D = self.ll[i+1] * self.ll[i]
            next_weights = np.array(weights[-D:]).reshape((self.ll[i+1], self.ll[i]))
            weights = weights[:-D]
            next_biases = np.array(weights[-self.ll[i+1]:]).reshape((self.ll[i+1], 1))
            weights = weights[:-self.ll[i+1]]

            self.weights.append(next_weights)
            self.biases.append(next_biases)

