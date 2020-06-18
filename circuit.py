import os
import pygame
import numpy as np
from math import *

# Fenetre de x = longueur : 1280 ; y = hauteurs : 720
# 0 0 en haute à gauche

# épaisseur des murs : 10



class Circuit :

    def __init__(self, screen):
        self.listObstacle = [[(50,50),(50,150)],[(50,50),(200,50)],[(50,150),(200,150)]]
        self.listCheckpoints = []
        self.screen = screen
        self.end = (1200,700)

    def initCircuit(self):
        self.ConstructionTabCircuit()
        self.initCheckpoints()

    def initCheckpoints(self): 
        i = 0
        for x in self.listObstacle[1:len(self.listCheckpoints)-1]:
            if not (i%2):
                self.listCheckpoints.append([x[1],(x[1][0],x[1][1]+100)])
            i= i + 1

        print(self.listCheckpoints)


    def ConstructionSegmentCircuit(self, xNext, yNext):
        x1A = self.listObstacle[-2][1][0]
        y1A = self.listObstacle[-2][1][1]
        x2A = self.listObstacle[-1][1][0]
        y2A = self.listObstacle[-1][1][1]
        self.listObstacle.append([(x1A,y1A),(xNext,yNext)])
        self.listObstacle.append([(x2A,y2A),(x2A+xNext-x1A,y2A+yNext-y1A)])

    def ConstructionTabCircuit(self):
        self.ConstructionSegmentCircuit(300,100)
        self.ConstructionSegmentCircuit(400,200)
        self.ConstructionSegmentCircuit(500,300)
        self.ConstructionSegmentCircuit(700,400)
        self.ConstructionSegmentCircuit(900,500)
        self.ConstructionSegmentCircuit(1200,550)
        self.listObstacle.append([(1200,550),(1200,650)])


    def draw(self) : 
        for i  in range (0,len(self.listObstacle)) :
            pygame.draw.line(self.screen, (0,0,255), (self.listObstacle[i][0]),(self.listObstacle[i][1]),5)
        for i  in range (0,len(self.listCheckpoints)) :
            pygame.draw.line(self.screen, (255,0,0), (self.listCheckpoints[i][0]),(self.listCheckpoints[i][1]),5)

