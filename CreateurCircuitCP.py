import pygame
from pygame.locals import *

pygame.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1280, 720))
fenetre.fill((0, 0, 0))

# Rafraîchissement de l'écran
pygame.display.flip()

# BOUCLE INFINIE
continuer = 1
premierpoint = (0, 0)
deuxiemepoint = (0, 0)
tabCircuit = []
tabCP = []
while continuer:
    for event in pygame.event.get():  # Attente des événements
        if event.type == QUIT:
            continuer = 0
        if event.type == KEYDOWN and event.key == K_r:
            fenetre.fill((0, 0, 0))
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            premierpoint = event.pos
        if event.type == MOUSEBUTTONUP and event.button == 1:
            deuxiemepoint = event.pos
            pygame.draw.line(fenetre, (0, 0, 255), premierpoint, deuxiemepoint, 5)
            tabCircuit.append([premierpoint, deuxiemepoint])
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            premierpoint = event.pos
        if event.type == MOUSEBUTTONUP and event.button == 3:
            deuxiemepoint = event.pos
            pygame.draw.line(fenetre, (255, 0, 0), premierpoint, deuxiemepoint, 5)
            tabCP.append([premierpoint, deuxiemepoint])

    # Rafraichissement
    pygame.display.flip()
print(tabCircuit)
print(tabCP)
