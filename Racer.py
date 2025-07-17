import numpy as np
import pygame
import Point

width = 5
length = 20
maxSpeed = 300
dragMaxSpeed = 250
accel = maxSpeed/2.0
turnRadius = width * 2
dragCoef = accel*(maxSpeed - dragMaxSpeed)/(maxSpeed * dragMaxSpeed**2)

class Racer:
    def __init__(self, start = None, hZ = 60):
        if start is None:
            start = Point.Point(0,0)
        self.pos = start.clone()
        self.relVel = Point.Point(0,0,0)
        self.loopTime = 1.0/hZ
        self.hasTraction = True
    
    def update(self, throttle, turn):

        # we have some amount of weight and then we get more with downforce from velociy
        staticFriction = 200 + 300 * (self.relVel.x/dragMaxSpeed)**2
        centripitalForce = 0.5 * self.relVel.x * self.relVel.h # F = m*v^2/r; r = s/theta = relVel.x/relVel.h; F = m*relVel.x*relVel.h
        
        if np.abs(centripitalForce) > staticFriction: # we lose traction if we have more centripital force than our static friction
            self.hasTraction = False
        elif self.relVel.mag() < maxSpeed/6: # we always have traction when going slow enough
            self.hasTraction = True
        
        if self.hasTraction:
            # First term makes it so we gradually decelerate at max speed (no drag), 2nd term is drag
            self.relVel.x += (accel*self.loopTime*throttle)*max((maxSpeed - np.sign(throttle)*self.relVel.x)/maxSpeed,1) - np.sign(self.relVel.x)*(self.relVel.x**2)*self.loopTime*dragCoef
            self.relVel.h += self.relVel.x / turnRadius * turn # S = r * theta --> theta = S/r
        else: # No traction = spin out
            rotVel = self.relVel.h
            self.relVel.h = 0
            self.relVel = self.relVel.rotate(-self.loopTime*rotVel).mult(0.5**self.loopTime) # this spins out and slows us down (we lose 50% speed every second)
            self.relVel.h = rotVel
 
        delta = self.relVel.mult(self.loopTime) # find the delta
        self.pos.h += delta.h
        delta = delta.rotate(self.pos.h) # Convert the delta to a global delta by rotating it to the racer's heading
        delta.h = 0
        self.pos = self.pos.add(delta) # Add the global delta to the position

    def draw(self, screen):
        center = (int(self.pos.x), int(self.pos.y))
        angle = -self.pos.heading  # Pygame rotates counter-clockwise
        car = pygame.Surface((length, width))
        car.fill((255, 255, 0))
        car = pygame.transform.rotate(car, np.degrees(angle))
        rect = car.get_rect(center=center)
        screen.blit(car, rect)