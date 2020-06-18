import random


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
