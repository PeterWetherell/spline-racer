import numpy as np
import Point
import pygame

class Racer:
    # all my static variables
    width = 10
    length = 20
    max_speed = 700
    drag_max_speed = 600
    accel = max_speed/1.3
    slip_percentage = 0.8
    deccel = max_speed*3
    turnRadius = width * 4
    dragCoef = accel*(max_speed - drag_max_speed)/(max_speed * drag_max_speed**2)

    def __init__(self, start = None, hZ = 60):
        if start is None:
            start = Point.Point(0,0)
        self.pos = start.clone()
        self.vel = Point.Point(0,0,0)
        self.loop_time = 1.0/hZ
        self.has_traction = True
        self.centripital_force = 0
    
    def update(self, throttle, turn):
        throttle = np.clip(throttle, -1, 1)
        if abs(throttle) < 0.05:
            throttle = 0
        turn = np.clip(turn, -1, 1)

        # we have some amount of weight and then we get more with downforce from velociy
        static_friction = 400 + 600 * (self.vel.x/Racer.drag_max_speed)**2
        centripital_force = 0.08 * self.vel.x * self.vel.h # F = m*v^2/r; r = s/theta = vel.x/vel.h; F = m*vel.x*vel.h
        self.centripital_force = centripital_force
        
        if np.abs(centripital_force) > static_friction: # we lose traction if we have more centripital force than our static friction
            self.has_traction = False
        elif self.vel.mag() < Racer.max_speed/6: # we always have traction when going slow enough
            self.has_traction = True
        
        if self.has_traction:
            # First term makes it so we gradually decelerate at max speed (no drag), 2nd term is drag
            a = Racer.accel
            if throttle*self.vel.x < 0:
                a = Racer.deccel
            self.vel.x += (a*self.loop_time*throttle)*max((Racer.max_speed - np.sign(throttle)*self.vel.x)/Racer.max_speed,1) - np.sign(self.vel.x)*(self.vel.x**2)*self.loop_time*Racer.dragCoef
            if throttle == 0:
                self.vel.x -= np.sign(self.vel.x)*min(abs(self.vel.x),self.loop_time*Racer.accel/3)
            self.vel.h = self.vel.x / Racer.turnRadius * turn # S = r * theta --> theta = S/r
            if abs(centripital_force) > static_friction*Racer.slip_percentage:
                self.vel.y += np.sign(centripital_force)*(abs(centripital_force)-static_friction*Racer.slip_percentage)/(static_friction*(1.0-Racer.slip_percentage))*self.loop_time*Racer.accel
            else:
                self.vel.y -= np.sign(self.vel.y)*min(abs(self.vel.y), self.loop_time*Racer.max_speed*2)
        else: # No traction = spin out
            rotVel = self.vel.h
            self.vel.h = 0
            self.vel = self.vel.rotate(-self.loop_time*rotVel) # this spins out
            self.vel.h = rotVel
            self.vel = self.vel.mult(0.2**self.loop_time) # this slows it down by 80% every sec
 
        self.delta = self.vel.mult(self.loop_time) # find the delta
        self.pos.h += self.delta.h
        self.delta = self.delta.rotate(self.pos.h) # Convert the delta to a global delta by rotating it to the racer's heading

    def draw(self, screen):
        car_surf = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        car_surf.fill((255, 255, 0))
        rotated_surf = pygame.transform.rotate(car_surf, -np.degrees(self.pos.h))
        rect = rotated_surf.get_rect(center=(int(self.pos.x + 400), int(self.pos.y + 300)))
        screen.blit(rotated_surf, rect)