import os
import pygame
from math import cos, sin, radians, degrees, copysign, sqrt
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

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
        
    def calculPointSensor(self, x, y, angle, dist):
        """x, y sont les coord de la voiture, angle est l'angle du capteur, dist 
        la distance jusqu'à laquelle peut voir le capteur
        fonction utilisee dans sensors"""
        ang = angle % 360
        a = abs(ang) % 90
        adjacent = cos(radians(a)) * dist
        oppose = sin(radians(a)) * dist
        if (ang<=90):
            return(x + adjacent, y - oppose)
        elif(ang<=180):
            return(x - oppose, y - adjacent)
        elif(ang <=270):
            return(x - adjacent, y + oppose)
        else:
            return(x + oppose, y + adjacent)
        
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
           #print(x1, y1, x2, y2, x3, y3, x4, y4)
           
           det = (x2 - x1)*(y3 - y4 ) - (x3 - x4 )*(y2 - y1)
           if(det!=0):
               t1 = ((x3 - x1)*(y3 - y4 ) - (x3 - x4 )*(y3 - y1))/det
               t2 = ((x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1))/det
               if (t1 <= 1 and t1 >= 0 and t2 <= 1 and t2 >= 0):
                   xintersect = x1 + t1*(x2 - x1)
                   yintersect = y1 + t1*(y2 - y1)
                   interdist = sqrt(pow(xintersect-x1, 2) + pow(yintersect-y1, 2))
                   if (dist < 0 or interdist < dist):
                       dist = interdist    
        return(dist)
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
            
        Utilise les fonctions intermédiaires calculPointSensor et intersec codées plus haut
        """
        
        s1 = []
        xsens, ysens = self.calculPointSensor(self.position[0], self.position[1], (self.angle + 15), 5)
        # 5 = distance à laquelle voit le capteur ; 15 = angle du capteur par rapport au "front" de la voiture
        s1.append( (self.position[0], self.position[1]))
        s1.append((xsens, ysens))
        # Donc s1 = [(x, y) , (xsens, ysens)] où (xsens, ysens) est le point final du segment capteur
        
        s2 = []
        xsens,ysens = self.calculPointSensor(self.position[0], self.position[1], self.angle, 5) 
        s2.append( (self.position[0], self.position[1]))
        s2.append((xsens, ysens))
        
        s3 = []
        xsens,ysens = self.calculPointSensor(self.position[0], self.position[1], self.angle - 15, 5) 
        s3.append( (self.position[0], self.position[1]))
        s3.append((xsens, ysens))
        
        return(self.intersec(s1, obs), self.intersec(s2, obs), self.intersec(s3, obs))
        


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

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(1, 1)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, car.angle)
            #print (car.angle % 360)
            #print(car.angle)
            #print(car.position[0], car.position[1])
#Test des Sensor >>> print(car.sensors([[(20,10),(19,9)],[(25,15),(20,15)]]))
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()