import numpy as np
import Point

class Spline:
    def __init__(self, p1, p2, c = 2):
        d = p1.dist(p2)
        v = c*Point.Point(d,0).rotate(p1.h - p2.h).add(p1.sub(p2)).mag()
        self.coefX = [-2*(p2.x-p1.x) + v*(np.cos(p2.h) + np.cos(p1.h)), 3*(p2.x-p1.x) - v*(np.cos(p2.h) + 2*np.cos(p1.h)), v*np.cos(p1.h), p1.x]
        self.coefY = [-2*(p2.y-p1.y) + v*(np.sin(p2.h) + np.sin(p1.h)), 3*(p2.y-p1.y) - v*(np.sin(p2.h) + 2*np.sin(p1.h)), v*np.sin(p1.h), p1.y]
    
    def get_point(self, t):
        x = sum(c * t**i for i, c in enumerate(reversed(self.coefX)))
        y = sum(c * t**i for i, c in enumerate(reversed(self.coefY)))
        return Point.Point(x, y)