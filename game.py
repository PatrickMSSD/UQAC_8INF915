import os
import pygame
import numpy as np
import random
import Car
from math import cos, sin, radians, degrees, copysign, sqrt, pi
from pygame.math import Vector2
from circuit import Circuit
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from keras.layers import Dense
from keras.models import Sequential


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
            TabCar.append(Car.Car(random.randint(70, 110), random.randint(80, 120)))

        for c in TabCar:
            c.trainNn()

        # ppu = 32

        #self.circuit.initCircuit()

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
