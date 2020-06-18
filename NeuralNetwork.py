import numpy as np
from keras import layers
from keras.models import Sequential
import tensorflow as tf


class NeuralNetwork():

    def __init__(self, nn_param_choices=None):
        self.m_model = self.newRadomNN()

    def newRadomNN(self):
        """Créé un nouveau NN aléatoire et le renvoie"""
        model = Sequential()
        model.add(layers.Dense(4, activation='relu', input_dim=3))
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
        x = np.ones((1, 3))
        for k in range(0, 2):
            if (entry[k] == -1):
                x[0][k] = 1
            else:
                x[0][k] = entry[k] / maxrange
        # print("X : ")
        # print(x[0])
        # print("----------------------------------")
        y = self.m_model.predict(x)
        # print("PRED :")
        # print(y[0])
        return (y[0])


# -------
# TESTS :

"""
# Application du NN aleatoire, du Predict, du passage des Poids en argument du NN, de la reproduction

model1 = newRadomNN()
poids1 = getPoidsNN(model1)
print(predictNN(model1, (36, 12, -1), 45))

model2 = newRadomNN()
print(predictNN(model2, (36, 12, -1), 45))

#print(getPoidsNN(model1))
#print("_______________________________")
#print(getPoidsNN(model2))
#print("===============================")
model3 = newRadomNN()
setPoidsNN(model3, breed(getPoidsNN(model1), getPoidsNN(model2)))
print(predictNN(model3, (36, 12, -1), 45))
#print(getPoidsNN(model3))

setPoidsNN(model2, poids1)
# print(predictNN(model2, (36, 12, -1), 45))
"""

"""
# Application de la modif des poids

model = newRadomNN()
p = getPoidsNN(model)
print(p)
print("---------------")
pmodif = mutate(p, 0.15)
print(pmodif)
"""
