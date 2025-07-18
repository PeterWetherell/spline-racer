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

class TrackManager:
    def __init__(self):
        self.splines = [Spline.Spline(Point.Point(-500,0,0),Point.Point(0,0,0)),
                        Spline.Spline(Point.Point(0,0,0),Point.Point(600,500,0)),
                        Spline.Spline(Point.Point(600,500,0),Point.Point(900,0,np.pi/2.0))]
        self.t = 1
        end = self.splines[1].get_point(1)
        print(end.x)
        print(end.y)
        print(end.h)
        
    def update(self, racer_delta):
        racer_delta = racer_delta.mult(-1)
        self.splines[0].update(racer_delta)
        self.splines[1].update(racer_delta)
        self.splines[2].update(racer_delta)

        i = int(self.t//1)
        self.t = i + self.splines[i].get_closest_t(self.t - i, racer_delta)
        if (i < 0): #Gone too far back -- dead
            return
        while (i > 1):
            self.splines.pop(0)
            end = self.splines[1].get_point(1)
            print(end.x)
            print(end.y)
            print(end.h)
            d = np.clip(np.random.normal(600,75),300,900)
            theta = random.choice([-1, 1])*np.clip(np.random.normal(np.pi/4,np.pi/8),0,np.pi/2) + end.h
            theta_f = theta + np.clip(np.random.normal(0,np.pi/8),-np.pi/2,np.pi/2)
            self.splines.append(Spline.Spline(end,Point.Point(end.x + d*np.cos(theta), end.y + d*np.sin(theta), theta_f)))
            i -= 1
            self.t = i + self.splines[i].get_closest_t(self.t - 1 - i, racer_delta)
            i = int(self.t//1)
        self.closestPoint = self.splines[i].get_point(self.t - i)

    def draw(self,screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.closestPoint.x+400), int(self.closestPoint.y)+300), 6)
        draw_spline(screen, self.splines[0], color=(0, 255, 0), resolution=200)
        draw_spline(screen, self.splines[1], color=(0, 255, 0), resolution=200)
        draw_spline(screen, self.splines[2], color=(0, 255, 0), resolution=200)
    
