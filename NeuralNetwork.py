import numpy as np
from keras import layers
from keras.models import Sequential
import tensorflow as tf


class NeuralNetwork():

    def __init__(self, nn_param_choices=None):
        self.m_fitness = 0
        self.entries = 3
        self.m_model = self.newRadomNN()

    def getFitness(self):
        return self.m_fitness

    def setFitness(self, fitness):
        self.m_fitness = fitness

    def newRadomNN(self):
        """Créé un nouveau NN aléatoire et le renvoie"""
        model = Sequential()
        model.add(layers.Dense(4, activation='relu', input_dim=self.entries))
        model.add(layers.Dense(3, activation='relu'))
        model.add(layers.Dense(2, activation='sigmoid'))
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return (model)

    def getPoidsNN(self):
        """Obtient le tableau de poids de model"""
        return (np.array(self.m_model.get_weights()))

    def setPoidsNN(self, poids):
        """Remplace les poids du model par le tableau de poids en argument"""
        return (self.m_model.set_weights(poids))

    def predictNN(self, entry, maxrange):
        """Entry est la sortie du capteur (ex : (-1, 42, 12)) et maxrange est la portée du capteur"""

        x = np.ones((1, self.entries))
        for k in range(0, self.entries):
            if (entry[k] == -1):
                x[0][k] = 1
            else:
                x[0][k] = entry[k] / maxrange
        # print(entry)
        # print("X : ")
        # print(x[0])
        # print("----------------------------------")
        #y = self.m_model.predict(x)
        y = self.m_model(x, training=False)
        # print("PRED :")
        # print(y[0])
        return (y[0])


# -------
# TESTS :

"""
# Application du NN aleatoire, du Predict, du passage des Poids en argument du NN, de la reproduction
import Evolutionnary as ev

model1 = NeuralNetwork()
poids1 = model1.getPoidsNN()
print(model1.predictNN((36, 12, -1), 45))

model2 = NeuralNetwork()
print(model2.predictNN((36, 12, -1), 45))

print(model1.getPoidsNN())
print("_______________________________")
print(model2.getPoidsNN())
print("===============================")
model3 = NeuralNetwork()
model3.setPoidsNN(ev.breed(model1.getPoidsNN(), model2.getPoidsNN()))
print(model3.predictNN((36, 12, -1), 45))
print(model3.getPoidsNN())

model2.setPoidsNN(poids1)
print(model2.predictNN((36, 12, -1), 45))
"""

"""
# Application de la modif des poids
import Evolutionnary as ev

model = NeuralNetwork()
p = model.getPoidsNN()
print(p)
print("---------------")
pmodif = ev.mutate(p, 0.15)
print(pmodif)
"""
