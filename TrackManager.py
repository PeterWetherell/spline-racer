import Point
import Spline
import pygame
import random
import numpy as np

def draw_spline(screen, spline, color=(255, 255, 255), resolution=100):
    points = []
    for i in range(resolution + 1):
        t = i / resolution
        pt = spline.get_point(t)
        points.append((int(pt.x+400), int(pt.y+300)))
    pygame.draw.lines(screen, color, False, points, 2)

def addSpline(s, p, c=1):
    return Spline.Spline(s.get_point(1),p,c=c)
    #return Spline.Spline(s.get_point(1),p,pVel=s.get_vel(1),pAccel=s.get_accel(1),c=c)

class TrackManager:
    def __init__(self):
        self.splines = [Spline.Spline(Point.Point(-500,0,0),Point.Point(0,0,0))]
        self.addNewSpline()
        self.addNewSpline()
        self.index = 1
        self.time = 0

    def addNewSpline(self):
        end = self.splines[-1].get_point(1)
        d = np.clip(np.random.normal(600,75),300,900)
        theta = random.choice([-1, 1])*np.clip(np.random.normal(np.pi/4,np.pi/10),0,np.pi/2) + end.h
        theta_f = theta + np.clip(np.random.normal(0,np.pi/10),-np.pi/3,np.pi/3)
        self.splines.append(addSpline(self.splines[-1],Point.Point(end.x+d*np.cos(theta), end.y+d*np.sin(theta), theta_f)))
        
    def update(self, racer_delta):
        racer_delta = racer_delta.mult(-1)
        for i in range(len(self.splines)):
            self.splines[i].update(racer_delta)
        prevT = self.time + self.index
        self.getClosestPoint()
        self.deltaT = (self.time + self.index) - prevT
        if self.index > 1:
            self.splines.pop(0)
            self.index -= 1
            self.addNewSpline()
    
    def get_point(self, t):
        t += self.time
        i = self.index
        if t > 1:
            t -= 1
            i += 1
        elif t < 0:
            t += 1
            i -= 1
        return self.splines[i].get_point(t)
    
    def getClosestPoint(self):
        t1 = self.splines[self.index].get_closest_t(self.time)
        if t1 < 0:
            if (self.index < 1): # Has gone too far backward on the track -- we dq them
                return
            t0 = np.clip(self.splines[self.index-1].get_closest_t(1),0,1) # start at t=1 bc that is theoretically the closest point on the last spline
            if self.splines[self.index].get_point(0).mag() > self.splines[self.index-1].get_point(t0).mag(): # if the point on the previous spline is closer -- use that one
                self.index -= 1
                self.time = t0
            else:
                self.time = 0
        elif t1 > 1:
            t2 = np.clip(self.splines[self.index+1].get_closest_t(0),0,1) # start at t=0 bc that is theoretically the closest point on the next spline
            if self.splines[self.index].get_point(1).mag() > self.splines[self.index+1].get_point(t2).mag(): # if the point on the next spline is closer -- use that one
                self.index += 1
                self.time = t2
            else:
                self.time = 1
        else:
            self.time = t1
        self.closestPoint = self.splines[self.index].get_point(self.time)
        self.curvature = self.splines[self.index].get_curvature(self.time)

    def draw(self,screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.closestPoint.x+400), int(self.closestPoint.y)+300), 6)
        end = self.splines[1].get_point(1)
        pygame.draw.circle(screen, (255, 0, 0), (int(end.x+400), int(end.y)+300), 6)
        draw_spline(screen, self.splines[0], color=(0, 255, 0), resolution=200)
        draw_spline(screen, self.splines[1], color=(0, 255, 0), resolution=200)
        draw_spline(screen, self.splines[2], color=(0, 255, 0), resolution=200)
    
