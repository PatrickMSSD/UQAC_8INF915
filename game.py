import os
import pygame
import numpy as np
import random
from math import cos, sin, radians, degrees, copysign, sqrt, pi
from pygame.math import Vector2
from circuit import Circuit
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression


class Car:
    def __init__(self, x, y, angle=0.0, length=30, max_steering=100, max_acceleration=160):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 160
        self.brake_deceleration = 320
        self.free_deceleration = 64

        self.acceleration = 0.0
        self.steering = 0.0

        self.fitness = 0
        self.EstEnCollision = False  # La voiture est présentement en collision, peu importe avec quoi
        self.canRun = True  # La voiture peut ou ne peut pas rouler (passé à false si collision avec un obstacle

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        self.image = pygame.image.load(image_path)

    # Entrainement des NN utilisés par la voiture
    def trainNn(self):
        X = [[-1, -1, -1], [20, -1, 6], [12, -1, 20], [12, 5, 20], [30, 10, 20]]
        yV = [1, 0.5, 0.5, 0, -1]
        yR = [0, 1, -0.2, -0.3, 0.4]

        self.nnV = MLPRegressor(random_state=1, max_iter=100).fit(X, yV)
        self.nnR = MLPRegressor(random_state=1, max_iter=100).fit(X, yR)

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def calculPoint(self, x, y, angle, dist):
        """x, y sont les coord de la voiture, angle est l'angle du capteur, dist
        la distance jusqu'à laquelle peut voir le capteur
        fonction utilisee dans sensors"""
        ang = angle % 360
        a = abs(ang) % 90
        adjacent = cos(radians(a)) * dist
        oppose = sin(radians(a)) * dist
        if (ang <= 90):
            return (x + adjacent, y - oppose)
        elif (ang <= 180):
            return (x - oppose, y - adjacent)
        elif (ang <= 270):
            return (x - adjacent, y + oppose)
        else:
            return (x + oppose, y + adjacent)

    def intersec(self, segment, obs):
        """renvoie la distance entre le 1er point du segment, et le segment de obs le plus proche avec
        lequel segment a une intersection, ou -1 s'il n'a aucune intersection avec aucun segment d'obs
        fonction utilisee dans sensors"""
        x1 = segment[0][0]
        y1 = segment[0][1]
        x2 = segment[1][0]
        y2 = segment[1][1]
        dist = -1
        for k in obs:
            x3 = k[0][0]
            y3 = k[0][1]
            x4 = k[1][0]
            y4 = k[1][1]
            # print(x1, y1, x2, y2, x3, y3, x4, y4)

            det = (x2 - x1) * (y3 - y4) - (x3 - x4) * (y2 - y1)
            if (det != 0):
                t1 = ((x3 - x1) * (y3 - y4) - (x3 - x4) * (y3 - y1)) / det
                t2 = ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / det
                if (t1 <= 1 and t1 >= 0 and t2 <= 1 and t2 >= 0):
                    xintersect = x1 + t1 * (x2 - x1)
                    yintersect = y1 + t1 * (y2 - y1)
                    interdist = sqrt(pow(xintersect - x1, 2) + pow(yintersect - y1, 2))
                    if (dist < 0 or interdist < dist):
                        dist = interdist
        return (dist)

    # Test reussi : print(intersec ([(1,1),(4,4)], [[(2,1),(1,2)]])) renvoie 0.707
    # et print(intersec ([(1,1),(4,4)], [[(1,3),(1,2)]])) renvoie -1

    def sensors(self, obs):
        """
        obs est une liste de liste des points de début et de fin des obstacles :
        [ [(12,8);(6,15)] ; [(4,3);(4,4)] ; ... ] où le premier obstacle
        est un segment de x=12, y=8 à x=6, y=15 par exemple

        Renvoie un triplet, correspondant à la détection d'obstacle et leur distance
        Ex : return (-1, 2.6, 5.3) signifie que le capteur 1 n'a rien capté, le capteur
        2 voit un mur à 2.6 de distance, et le capteur 3 voit un mur à 5.3 de distance

        Utilise les fonctions intermédiaires calculPoint et intersec codées plus haut
        """

        s1 = []
        xsens, ysens = self.calculPoint(self.position[0], self.position[1], (self.angle + 45), 100)
        # 5 = distance à laquelle voit le capteur ; 15 = angle du capteur par rapport au "front" de la voiture
        s1.append((self.position[0], self.position[1]))
        s1.append((xsens, ysens))
        # Donc s1 = [(x, y) , (xsens, ysens)] où (xsens, ysens) est le point final du segment capteur

        s2 = []
        xsens, ysens = self.calculPoint(self.position[0], self.position[1], self.angle, 100)
        s2.append((self.position[0], self.position[1]))
        s2.append((xsens, ysens))

        s3 = []
        xsens, ysens = self.calculPoint(self.position[0], self.position[1], self.angle - 45, 100)
        s3.append((self.position[0], self.position[1]))
        s3.append((xsens, ysens))

        return (self.intersec(s1, obs), self.intersec(s2, obs), self.intersec(s3, obs))

    def testCollision(self, obs):
        """
        obs est une liste de liste des points de début et de fin des obstacles :
        [ [(12,8);(6,15)] ; [(4,3);(4,4)] ; ... ] où le premier obstacle
        est un segment de x=12, y=8 à x=6, y=15 par exemple

        Calcule les 4 segments représentant les côtés du collider de la voiture en utilisant la position
        de la voiture, ses dimensions (celles de son image) ainsi que sa rotation,
        puis vérifie si un de ces segments est en collision avec un des segments passées dans obs

        Retourne True si la voiture est en collision avec un segment du tableau passé en paramètres,
        False sinon

        Utilise la fonction intermédiaire intersec codée plus haut
        """

        collVertices = []
        collVertices.append(
            (self.position.x + (self.image.get_width() / 2), self.position.y + (-self.image.get_height() / 2)))
        collVertices.append(
            (self.position.x + (self.image.get_width() / 2), self.position.y + (self.image.get_height() / 2)))
        collVertices.append(
            (self.position.x + (-self.image.get_width() / 2), self.position.y + (self.image.get_height() / 2)))
        collVertices.append(
            (self.position.x + (-self.image.get_width() / 2), self.position.y + (-self.image.get_height() / 2)))

        radAngle = (self.angle % 360) * pi / 180

        temp = []
        for point in collVertices:
            xPoint = point[0] - self.position.x
            yPoint = point[1] - self.position.y
            xRot = xPoint * cos(radAngle) + yPoint * sin(radAngle) + self.position.x
            yRot = -xPoint * sin(radAngle) + yPoint * cos(radAngle) + self.position.y
            temp.append((xRot, yRot))

        collVertices = temp

        seg1 = []
        seg1.append((collVertices[0][0], collVertices[0][1]))
        seg1.append((collVertices[1][0], collVertices[1][1]))
        seg2 = []
        seg2.append((collVertices[1][0], collVertices[1][1]))
        seg2.append((collVertices[2][0], collVertices[2][1]))
        seg3 = []
        seg3.append((collVertices[2][0], collVertices[2][1]))
        seg3.append((collVertices[3][0], collVertices[3][1]))
        seg4 = []
        seg4.append((collVertices[3][0], collVertices[3][1]))
        seg4.append((collVertices[0][0], collVertices[0][1]))

        colliderSegments = []
        colliderSegments.append(seg1)
        colliderSegments.append(seg2)
        colliderSegments.append(seg3)
        colliderSegments.append(seg4)

        isColliding = 0
        for segment in colliderSegments:
            isColliding = self.intersec(segment, obs)
            if (isColliding != -1):
                self.EstEnCollision = True
                # print("Collision")
                return (True)
                break
            else:
                self.EstEnCollision = False
        return (False)

    def CalculFitness(self):
        self.fitness = self.position.x / 1150

    # Fonction d'agent de la voiture
    def run(self, obs, dt):
        Entrée = self.sensors(obs)
        SortieVitesse = self.nnV.predict(np.asarray(Entrée).reshape(1, -1))
        SortieRotation = self.nnR.predict(np.asarray(Entrée).reshape(1, -1))

        self.acceleration += SortieVitesse[0] * 640 * dt
        self.steering += SortieRotation[0] * 300 * dt

    def stop(self):
        self.canRun = False
        self.acceleration = 0.0
        self.steering = 0.0
        self.velocity = Vector2(0.0, 0.0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.circuit = Circuit(self.screen)

    def run(self):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(current_dir, "car.png")
        # car_image = pygame.image.load(image_path)

        # MODIFIER LE NOMBRE DE VOITURE ICI POUR EN AVOIR QU UNE
        NombreVoiture = 5
        TabCar = []

        #  REMPLACER RANDOM PAR LES COORD DE LA VOITURE SI UNIQUE VOITURE, SINON LES 5 AURONT LE MEME COMPORTEMENT ET SERONT INDIFFERENCIABLE
        for i in range(0, NombreVoiture):
            TabCar.append(Car(random.randint(70, 110), random.randint(80, 120)))

        for c in TabCar:
            c.trainNn()

        # ppu = 32

        self.circuit.initCircuit()

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Mouvement de la voiture par IA
            for c in TabCar:
                if (c.canRun):
                    c.run(self.circuit.listObstacle, dt)
                    if (c.testCollision(self.circuit.listObstacle)):
                        c.stop()

            # Mouvement de la voiture par l'utilisateur
            """
            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 640 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 640 * dt
            # elif pressed[pygame.K_SPACE]:
            # if abs(car.velocity.x) > dt * car.brake_deceleration:
            # car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
            # else:
            # car.acceleration = -car.velocity.x / dt'''
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 300 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 300 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
            """

            # Logic
            for c in TabCar:
                c.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            for c in TabCar:
                rotated = pygame.transform.rotate(c.image, c.angle)
                # print (car.angle % 360)
                # print(car.angle)
                # print(car.position[0], car.position[1])
                # Test des Sensor >>>
                # print(self.circuit.listObstacle)
                # print(car.sensors(self.circuit.listObstacle))
                # car.sensors(self.circuit.listObstacle)
                # car.testCollision(self.circuit.listObstacle)
                rect = rotated.get_rect()
                self.screen.blit(rotated, c.position - (rect.width / 2, rect.height / 2))

            self.circuit.draw()

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
