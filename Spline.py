import numpy as np
import Point

class Spline:
    def __init__(self, p1, p2, c = 2):
        d = p1.dist(p2)
        v = c*Point.Point(d,0).rotate(p1.h - p2.h).add(p1.sub(p2)).mag()
        self.coefX = [-2*(p2.x-p1.x) + v*(np.cos(p2.h) + np.cos(p1.h)), 3*(p2.x-p1.x) - v*(np.cos(p2.h) + 2*np.cos(p1.h)), v*np.cos(p1.h), p1.x]
        self.coefY = [-2*(p2.y-p1.y) + v*(np.sin(p2.h) + np.sin(p1.h)), 3*(p2.y-p1.y) - v*(np.sin(p2.h) + 2*np.sin(p1.h)), v*np.sin(p1.h), p1.y]
    
    def update(self, delta):
        self.coefX[3] += delta.x
        self.coefY[3] += delta.y

    def get_closest_t(self, t, p):
        while True:
            d = p.sub(self.get_point(t))
            v = self.get_vel(t)
            dt = d.dot(v)/(v.mag()**2)
            t += dt
            if (dt < 1e-4):
                return t

    def get_vel(self, t):
        return Point.Point(
            3*self.coefX[0]*t**2 + 2*self.coefX[1]*t + self.coefX[2],
            3*self.coefY[0]*t**2 + 2*self.coefY[1]*t + self.coefY[2]
            )

    def get_point(self, t):
        x = sum(c * t**i for i, c in enumerate(reversed(self.coefX)))
        y = sum(c * t**i for i, c in enumerate(reversed(self.coefY)))
        return Point.Point(x, y)