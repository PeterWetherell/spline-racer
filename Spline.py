import numpy as np
import Point

class Spline:
    def __init__(self, p1, p2, c=1, pVel = None, pAccel = None):
        d = p1.dist(p2)
        v = c*p1.add(Point.Point(d*np.cos(p1.h),d*np.sin(p1.h))).sub(p2.add(Point.Point(d*np.cos(p2.h),d*np.sin(p2.h)))).mag()
        if pVel is None:
            self.coefX = [0,-2*(p2.x-p1.x) + v*(np.cos(p2.h) + np.cos(p1.h)), 3*(p2.x-p1.x) - v*(np.cos(p2.h) + 2*np.cos(p1.h)), v*np.cos(p1.h), p1.x]
            self.coefY = [0,-2*(p2.y-p1.y) + v*(np.sin(p2.h) + np.sin(p1.h)), 3*(p2.y-p1.y) - v*(np.sin(p2.h) + 2*np.sin(p1.h)), v*np.sin(p1.h), p1.y]
        else:
            k = (v/pVel.mag())**2
            self.coefX = [0, 0, pAccel.x*k, v*np.cos(p1.h), p1.x]
            self.coefX[0] = v*np.cos(p2.h) - 3*p2.x + self.coefX[2] + 2*self.coefX[3] + 3*self.coefX[4]
            self.coefX[1] = p2.x - self.coefX[0] - self.coefX[2] - self.coefX[3] - self.coefX[4]
            self.coefY = [0, 0, pAccel.y*k, v*np.sin(p1.h), p1.y]
            self.coefY[0] = v*np.sin(p2.h) - 3*p2.y + self.coefY[2] + 2*self.coefY[3] + 3*self.coefY[4]
            self.coefY[1] = p2.y - self.coefY[0] - self.coefY[2] - self.coefY[3] - self.coefY[4]

    def update(self, delta):
        self.coefX[4] += delta.x
        self.coefY[4] += delta.y

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
            4*self.coefX[0]*(t**3) + 3*self.coefX[1]*(t**2) + 2*self.coefX[2]*t + self.coefX[3],
            4*self.coefY[0]*(t**3) + 3*self.coefY[1]*(t**2) + 2*self.coefY[2]*t + self.coefY[3]
            )

    def get_accel(self, t):
        return Point.Point(
            12*self.coefX[0]*(t**2) + 6*self.coefX[1]*t + 2*self.coefX[2],
            12*self.coefY[0]*(t**2) + 6*self.coefY[1]*t + 2*self.coefY[2]
            )
    
    def get_curvature(self, t):
        v = self.get_vel(t)
        a = self.get_accel(t)
        return (a.y*v.x - a.x*v.y)/(v.mag()**3)

    def get_point(self, t):
        x = sum(c * t**i for i, c in enumerate(reversed(self.coefX)))
        y = sum(c * t**i for i, c in enumerate(reversed(self.coefY)))
        v = self.get_vel(t)
        return Point.Point(x, y, np.arctan2(v.y,v.x))