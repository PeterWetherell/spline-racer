import numpy as np

class Point:
    def __init__(self, x, y, h=0):
        self.x = x
        self.y = y
        self.h = h

    def dist(self, p2 = None):
        if p2 is None:
            p2 = Point(0,0)
        return np.sqrt((self.x - p2.x)**2 + (self.y - p2.y)**2)

    def mag(self):
        return np.sqrt(self.x**2 + self.y**2)
    
    def add(self, p2 = None):
        if p2 is None:
            p2 = Point(0,0)
        return Point(self.x+p2.x, self.y+p2.y, self.h+p2.h)
    
    def dot(self, p2 = None):
        if p2 is None:
            p2 = Point(0,0)
        return self.x*p2.x + self.y*p2.y
    
    def sub(self, p2 = None):
        if p2 is None:
            p2 = Point(0,0)
        return Point(self.x-p2.x, self.y-p2.y, self.h-p2.h)
    
    def mult(self, m = 1):
        return Point(self.x*m, self.y*m, self.h*m)
    
    def clone(self):
        return Point(self.x, self.y, self.h)

    def rotate(self, h):
        nx = self.x*np.cos(h) - self.y*np.sin(h)
        ny = self.y*np.cos(h) + self.x*np.sin(h)
        return Point(nx,ny,self.h+h)