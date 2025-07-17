import numpy as np
import pygame
import Point

width = 10
length = 20
maxSpeed = 700
dragMaxSpeed = 600
accel = maxSpeed/1.3
deccel = maxSpeed*3
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
        throttle = np.clip(throttle, -1, 1)
        turn = np.clip(turn, -1, 1)

        # we have some amount of weight and then we get more with downforce from velociy
        staticFriction = 400 + 800 * (self.relVel.x/dragMaxSpeed)**2
        centripitalForce = 0.08 * self.relVel.x * self.relVel.h # F = m*v^2/r; r = s/theta = relVel.x/relVel.h; F = m*relVel.x*relVel.h
        
        if np.abs(centripitalForce) > staticFriction: # we lose traction if we have more centripital force than our static friction
            self.hasTraction = False
        elif self.relVel.mag() < maxSpeed/6: # we always have traction when going slow enough
            self.hasTraction = True
        
        if self.hasTraction:
            # First term makes it so we gradually decelerate at max speed (no drag), 2nd term is drag
            a = accel
            if throttle*self.relVel.x < 0:
                a = deccel
            self.relVel.x += (a*self.loopTime*throttle)*max((maxSpeed - np.sign(throttle)*self.relVel.x)/maxSpeed,1) - np.sign(self.relVel.x)*(self.relVel.x**2)*self.loopTime*dragCoef
            self.relVel.h = self.relVel.x / turnRadius * turn # S = r * theta --> theta = S/r
            self.relVel.y -= np.sign(self.relVel.y)*min(abs(self.relVel.y), self.loopTime*maxSpeed*2)
        else: # No traction = spin out
            rotVel = self.relVel.h
            self.relVel.h = 0
            self.relVel = self.relVel.rotate(-self.loopTime*rotVel) # this spins out
            self.relVel.h = rotVel
            self.relVel = self.relVel.mult(0.2**self.loopTime) # this slows it down by 80% every sec
 
        delta = self.relVel.mult(self.loopTime) # find the delta
        self.pos.h += delta.h
        delta = delta.rotate(self.pos.h) # Convert the delta to a global delta by rotating it to the racer's heading
        delta.h = 0
        self.pos = self.pos.add(delta) # Add the global delta to the position

    def draw(self, screen):
        car_surf = pygame.Surface((length, width), pygame.SRCALPHA)
        car_surf.fill((255, 255, 0))
        rotated_surf = pygame.transform.rotate(car_surf, -np.degrees(self.pos.h))
        rect = rotated_surf.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(rotated_surf, rect)