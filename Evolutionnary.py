import random
import NeuralNetwork as NN


def initPopulation(nbIndividus):
    population = []
    for i in range(0, nbIndividus):
        population.append(NN.NeuralNetwork())
    return population


'''
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
'''


def mutate(poids, maxmodif):
    k = random.randint(0, poids.size - 1)

    print("Mutation of ", k)

    if (poids[k].ndim > 1):
        i = random.randint(0, poids[k].shape[0] - 1)
        j = random.randint(0, poids[k].shape[1] - 1)
        rd = random.uniform(-maxmodif, maxmodif)
        poids[k][i][j] += rd
        if (poids[k][i][j] > 1):
            poids[k][i][j] = 1
        elif (poids[k][i][j] < -1):
            poids[k][i][j] = -1

    elif(poids[k].ndim == 1):
        i = random.randint(0, poids[k].shape[0] - 1)
        rd = random.uniform(-maxmodif, maxmodif)
        poids[k][i] += rd
        if (poids[k][i] > 1):
            poids[k][i] = 1
        elif (poids[k][i] < -1):
            poids[k][i] = -1
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


def updateGeneration(population, parentsRatio, randOtherProb, mutationProb, mutMaxModif):
    """Produit les NeuralNetworks d'une nouvelle population à partir d'une population donnée
    parentsRatio est le pourcentage de parents (individus les plus performants de l'ancienne génération) qui seront repris tel-quels
    randOtherProb est la probabilité qu'un individu moins performant soit repris tel-quel dans la nouvelle génération
    mutationProb est la probabilité qu'un bébé issu de deux parents subisse une mutation"""

    sortedNetworks = []

    for network in population:
        sortedNetworks.append(network)

    sortedNetworks.sort(key=lambda network: network.getFitness(), reverse=True)
    nbKeptParents = int(len(sortedNetworks) * parentsRatio)
    parents = sortedNetworks[:nbKeptParents]

    for individual in sortedNetworks[nbKeptParents:]:
        if randOtherProb > random.random():
            parents.append(individual)

    nbParents = len(parents)

    if (nbParents <= 1):
        print("Erreur: Il foit y avoir plus d'un parent")
        return -1

    remainingNb = len(population) - nbParents
    childrens = []

    while (len(childrens) < remainingNb):
        # emulation d'un do-while
        mother = random.randint(0, nbParents - 1)
        father = random.randint(0, nbParents - 1)
        while (mother == father):
            mother = random.randint(0, nbParents - 1)
            father = random.randint(0, nbParents - 1)

        mother = parents[mother]
        father = parents[father]
        baby = NN.NeuralNetwork()
        baby.setPoidsNN(breed(mother.getPoidsNN(), father.getPoidsNN()))
        if mutationProb > random.random():
            baby.setPoidsNN(mutate(baby.getPoidsNN(), mutMaxModif))
        childrens.append(baby)

    parents.extend(childrens)
    return parents

def setLearningPhase(phase):
    NN.tf.keras.backend.set_learning_phase(phase)

# -------
# TESTS :

"""
# Génère les réseaux de neurones aléatoires pour une population donnée, change la fitness, 
# puis met à jour la population (nouvelle génération)

pop = initPopulation(5)
print(pop)
pop[0].setFitness(0)
pop[1].setFitness(2)
pop[2].setFitness(1)
pop[3].setFitness(4)
pop[4].setFitness(3)
pop = updateGeneration(pop, 0.4, 0.1, 0.2)
print(pop)
"""
