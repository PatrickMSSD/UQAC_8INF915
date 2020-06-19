import pygame
import Car
import Evolutionnary as Evo
from circuit import Circuit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 15
        self.exit = False
        self.circuit = Circuit(self.screen)

    def run(self):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(current_dir, "car.png")
        # car_image = pygame.image.load(image_path)

        # MODIFIER LE NOMBRE DE VOITURE ICI POUR EN AVOIR QU UNE
        NombreVoiture = 10
        TabCar = []

        populationNN = Evo.initPopulation(NombreVoiture)
        generationCount = 1
        while not self.exit:
            allCarsCrashed = False

            print(generationCount)
            generationCount += 1

            #  REMPLACER RANDOM PAR LES COORD DE LA VOITURE SI UNIQUE VOITURE, SINON LES 5 AURONT LE MEME COMPORTEMENT ET SERONT INDIFFERENCIABLE
            for i in range(0, NombreVoiture):
                # TabCar.append(Car.Car(random.randint(70, 110), random.randint(80, 120)))
                TabCar.append(Car.Car(73, 350))

            for j in range(0, NombreVoiture):
                TabCar[j].setNeuralNetwork(populationNN[j])

            self.clock = pygame.time.Clock()

            while (allCarsCrashed == False):
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
                        elif (self.isOutOfBounds(c)): #si une voiture est sortie du circuit et de l'écran on la disqualifie
                            c.stop()
                            c.m_nn.setFitness(0)


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
                allCarsCrashed = True
                for c in TabCar:
                    c.update(dt)
                    if c.canRun == True:
                        allCarsCrashed = False

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

            for x in range(0, NombreVoiture):
                populationNN[x].setFitness(TabCar[x].getFitness())

            populationNN = Evo.updateGeneration(populationNN, 0.4, 0.1, 0.2)

            TabCar.clear()

        pygame.quit()

    def isOutOfBounds(self, aCar):
        if aCar.position.x < 0 or aCar.position.x > self.screen.get_width() \
                or aCar.position.y < 0 or aCar.position.y > self.screen.get_height():
            return True


if __name__ == '__main__':
    game = Game()
    game.run()
