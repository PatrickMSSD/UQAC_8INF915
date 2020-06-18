from keras import layers
from keras.models import Sequential
import tensorflow as tf
import numpy as np
import random


def newRadomNN():
    """Créé un nouveau NN aléatoire et le renvoie"""
    model = Sequential()
    model.add(layers.Dense(4, activation='relu', input_dim=3))
    model.add(layers.Dense(3, activation='relu'))
    model.add(layers.Dense(2, activation='sigmoid'))
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return (model)


def getPoidsNN(model):
    """Obtient le tableau de poids de model"""
    return (np.array(model.get_weights()))


def setPoidsNN(model, poids):
    """Remplace les poids du model par le tableau de poids en argument"""
    return (model.set_weights(poids))


def predictNN(model, entry, maxrange):
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
    y = model.predict(x)
    # print("PRED :")
    # print(y[0])
    return (y[0])


def mutate(poids, maxmodif):
    """Produit un nouveau tableau de poids en se basant sur le tableau de poids d'entrée et en le modifiant légèrement aléatoirement.
    maxmodif est la valeur maximale de modification des poids. On peut donc, pour chaque poids, varier de -maxmodif à +maxmodif"""
    for k in poids:
        if (k.ndim > 1):
            ii = k.shape[0]
            jj = k.shape[1]
            for i in range(0, ii):
                for j in range(0, jj):
                    rd = random.uniform(-maxmodif, maxmodif)
                    k[i][j] += rd
                    if (k[i][j] > 1):
                        k[i][j] = 1
                    elif (k[i][j] < -1):
                        k[i][j] = -1
    return poids


def breed(motherWeights, fatherWeights):
    """Produit un nouveau tableau de poids en se basant sur les tableaux de poids de la mere et du pere et en les combinant aleatoirement.
    Pour l'instant la vérification de compatibilité des parents ne se fait que sur le nombre de layers"""

    if (len(motherWeights) != len(motherWeights)):
        print("Erreur : Mere et Pere de dimensions differentes")
        return  # ERREUR

    childWeights = motherWeights

    for k in range(0, len(motherWeights)):
        if (motherWeights[k].ndim > 1):
            ii = motherWeights[k].shape[0]
            jj = motherWeights[k].shape[1]
            for i in range(0, ii):
                for j in range(0, jj):
                    childWeights[k][i][j] = random.choice([motherWeights[k][i][j], fatherWeights[k][i][j]])
    return childWeights


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
