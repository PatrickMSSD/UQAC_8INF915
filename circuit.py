import os
import pygame
import numpy as np
from math import *

# Fenetre de x = longueur : 1280 ; y = hauteurs : 720
# 0 0 en haute à gauche

# épaisseur des murs : 10



class Circuit :

    def __init__(self, screen):
        self.EcartementMur = 50
        self.listObstacle = [[(50,50),(50,100)],[(50,50),(140,50)],[(50,100),(140,100)]]
        self.screen = screen
        self.end = (1200,700)

    def initCircuit(self):
        self.ConstructionTabCircuit()
        print(self.listObstacle)


    def ConstructionSegmentCircuit(self, xNext, yNext):
        x1A = self.listObstacle[-2][1][0]
        y1A = self.listObstacle[-2][1][1]
        x2A = self.listObstacle[-1][1][0]
        y2A = self.listObstacle[-1][1][1]


        self.listObstacle.append([(x1A,y1A),(xNext,yNext)])
        self.listObstacle.append([(x2A,y2A),(x2A+xNext-x1A,y2A+yNext-y1A)])

    def ConstructionTabCircuit(self):
        self.ConstructionSegmentCircuit(200,150)
        self.ConstructionSegmentCircuit(300,350)
        self.ConstructionSegmentCircuit(450,500)
        self.ConstructionSegmentCircuit(750,500)
        self.ConstructionSegmentCircuit(900,600)
        self.ConstructionSegmentCircuit(1200,600)


    def draw(self) : 
        pygame.draw.line(self.screen, (0,0,255), (50,50),(50,100),5)
        pygame.draw.line(self.screen, (0,0,255),(50,50),(140,50),5)
        pygame.draw.line(self.screen, (0,0,255),(50,100),(140,100),5)

        for i  in range (3,len(self.listObstacle)) :
            pygame.draw.line(self.screen, (0,0,255), (self.listObstacle[i][0]),(self.listObstacle[i-2][1]),5)
            pygame.draw.line(self.screen, (0,0,255),(self.listObstacle[i][1]),(self.listObstacle[i-2][1]),5)

        pygame.draw.line(self.screen, (0,0,255),(1200,600),(1200,650),5)
