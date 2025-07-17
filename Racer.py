import numpy as np
import Point

class Racer:
    # all my static variables
    width = 10
    length = 20
    maxSpeed = 700
    dragMaxSpeed = 600
    accel = maxSpeed/1.3
    deccel = maxSpeed*3
    turnRadius = width * 2
    dragCoef = accel*(maxSpeed - dragMaxSpeed)/(maxSpeed * dragMaxSpeed**2)

    def __init__(self, start = None, hZ = 60):
        if start is None:
            start = Point.Point(0,0)
        self.pos = start.clone()
        self.relVel = Point.Point(0,0,0)
        self.loopTime = 1.0/hZ
        self.hasTraction = True
    
    def update(self, throttle, turn):
        throttle = np.clip(throttle, -1, 1)
        if abs(throttle) < 0.05:
            throttle = 0
        turn = np.clip(turn, -1, 1)

        # we have some amount of weight and then we get more with downforce from velociy
        staticFriction = 400 + 800 * (self.relVel.x/Racer.dragMaxSpeed)**2
        centripitalForce = 0.08 * self.relVel.x * self.relVel.h # F = m*v^2/r; r = s/theta = relVel.x/relVel.h; F = m*relVel.x*relVel.h
        
        if np.abs(centripitalForce) > staticFriction: # we lose traction if we have more centripital force than our static friction
            self.hasTraction = False
        elif self.relVel.mag() < Racer.maxSpeed/6: # we always have traction when going slow enough
            self.hasTraction = True
        
        if self.hasTraction:
            # First term makes it so we gradually decelerate at max speed (no drag), 2nd term is drag
            a = Racer.accel
            if throttle*self.relVel.x < 0:
                a = Racer.deccel
            self.relVel.x += (a*self.loopTime*throttle)*max((Racer.maxSpeed - np.sign(throttle)*self.relVel.x)/Racer.maxSpeed,1) - np.sign(self.relVel.x)*(self.relVel.x**2)*self.loopTime*Racer.dragCoef
            if throttle == 0:
                self.relVel.x -= np.sign(self.relVel.x)*min(abs(self.relVel.x),self.loopTime*Racer.accel/3)
            self.relVel.h = self.relVel.x / Racer.turnRadius * turn # S = r * theta --> theta = S/r
            self.relVel.y -= np.sign(self.relVel.y)*min(abs(self.relVel.y), self.loopTime*Racer.maxSpeed*2)
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