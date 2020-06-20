import os
import pygame
import numpy as np
from math import *


# Fenetre de x = longueur : 1280 ; y = hauteurs : 720
# 0 0 en haute à gauche

# épaisseur des murs : 10


class Circuit:

    def __init__(self, screen):
        self.listObstacle = [[(48, 51), (191, 51)], [(1089, 607), (1227, 601)], [(52, 54), (91, 591)],
                             [(191, 58), (225, 516)], [(227, 517), (274, 550)], [(274, 551), (324, 557)],
                             [(325, 561), (361, 534)], [(94, 589), (200, 644)], [(200, 645), (409, 648)],
                             [(411, 649), (474, 568)], [(361, 537), (619, 46)], [(476, 572), (550, 310)],
                             [(552, 312), (709, 106)], [(620, 50), (725, 19)], [(725, 21), (820, 20)],
                             [(710, 108), (758, 103)], [(757, 103), (802, 202)], [(819, 22), (865, 180)],
                             [(866, 178), (979,
                                           232)], [(802, 202), (941, 320)], [(981, 233), (1230, 271)],
                             [(943, 321), (1088, 433)], [(1088, 432), (1094, 611)], [(1230, 272), (1228, 600)]]
        self.listCheckpoints = [[(62, 161), (200, 171)], [(78, 374), (216, 370)], [(131, 607), (230, 519)],
                                [(326, 558), (358, 649)], [(494, 287), (554, 315)], [(619, 51), (708, 112)],
                                [(779, 149), (846, 112)], [(948, 217), (909, 289)], [(1030, 387), (1070, 250)],
                                [(1092, 449), (1232, 451)], [(430, 411), (506, 481)], [(560, 164), (630, 214)]]
        self.screen = screen
        self.end = (1200, 700)

    """
    def initCircuit(self):
        self.ConstructionTabCircuit()
        self.initCheckpoints()

    def initCheckpoints(self): 
        i = 0
        for x in self.listObstacle[1:len(self.listCheckpoints)-1]:
            if not (i%2):
                self.listCheckpoints.append([x[1],(x[1][0],x[1][1]+100)])
            i= i + 1



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

    """

    def draw(self):
        for i in range(0, len(self.listObstacle)):
            pygame.draw.line(self.screen, (0, 0, 255), (self.listObstacle[i][0]), (self.listObstacle[i][1]), 5)
        for i in range(0, len(self.listCheckpoints)):
            pygame.draw.line(self.screen, (255, 0, 0), (self.listCheckpoints[i][0]), (self.listCheckpoints[i][1]), 5)
