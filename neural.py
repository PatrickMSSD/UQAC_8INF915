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
    return(model)

def getPoidsNN(model):
    """Obtient le tableau de poids de model"""
    return(np.array(model.get_weights()))

def setPoidsNN(model, poids):
    """Remplace les poids du model par le tableau de poids en argument"""
    return(model.set_weights(poids))

def predictNN(model, entry, maxrange):
    """Entry est la sortie du capteur (ex : (-1, 42, 12)) et maxrange est la portée du capteur"""
    x = np.ones((1, 3))
    for k in range(0, 2):
        if(entry[k]==-1):
            x[0][k] = 1
        else:
            x[0][k] = entry[k] / maxrange
    #print("X : ")
    #print(x[0])
    #print("----------------------------------")
    y = model.predict(x)
    #print("PRED :")
    #print(y[0])
    return(y[0])

def hybrid(poids, maxmodif):
    """Produit un nouveau tableau de poids en se basant sur le tableau de poids d'entrée et en le modifiant légèrement aléatoirement. 
    maxmodif est la valeur maximale de modification des poids. On peut donc, pour chaque poids, varier de -maxmodif à +maxmodif"""
    for k in poids:
        if(k.ndim>1):            
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

# -------
# TESTS :

"""
# Application du NN aleatoire, du Predict, du passage des Poids en argument du NN

model1 = newRadomNN()
poids1 = getPoidsNN(model1)
print(predictNN(model1, (36, 12, -1), 45))

model2 = newRadomNN()
print(predictNN(model2, (36, 12, -1), 45))

setPoidsNN(model2, poids1)
print(predictNN(model2, (36, 12, -1), 45))
"""

"""
# Application de la modif des poids

model = newRadomNN()
p = getPoidsNN(model)
print(p)
print("---------------")
pmodif = hybrid(p, 0.15)
print(pmodif)
"""
    