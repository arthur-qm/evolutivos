from math import sqrt, cos, sin, pi
from random import random

"""
Creates a vector in which there's relative independence
in the relation between the components and the magnetude
because the componentes (x, y) are always equal to (costheta, 
sin theta)
"""

class Vector:
    # If mag is negative, it will be deduced
    # If it is positive, I am trying to create a vector
    # with this given magnetude and this relation between
    # x and y
    def __init__(self, x, y, mag=-1):
        
        # If the magnetude is zero, set arbitrary direction
        self.mag = sqrt(x**2+y**2)

        if self.mag == 0:
            self.x = 1
            self.y = 0
            return
        
        self.x = x / self.mag
        self.y = y / self.mag
        
        if mag > 0:
            self.mag = mag

    @staticmethod
    def gencis(frac):
        return Vector(cos(frac * pi), sin(frac * pi))
    
    @staticmethod
    def randomunit(mag=1):
        v = Vector(2*random()-1, 2*random()-1).normalized()
        
        if mag != 1:
            v.setmag(mag)
        
        return v
    
    @staticmethod
    def from_direction_and_val(direction, val):
        if val > 0:
            v = direction.clone()
            v.setmag(val)
        elif val == 0:
            return Vector(0, 0)
        else:
            v = direction.rotatedby(1)
            v.setmag(-val)
        return v

    def setmag(self, newmag):
        self.mag = newmag

    def distance(self, other):
        return (self-other).mag

    def normalized(self):
        return Vector(self.x, self.y)

    def rot90anti(self):
        return Vector(-self.y, self.x, self.mag)
    
    def rot90posl(self):
        return Vector(self.y, -self.x, self.mag)
    
    def rotatedby(self, anglefrac):
        return self ** Vector.gencis(anglefrac)
    
    def __eq__(self, other):
        self.x = other.x
        self.y = other.y
        self.mag = other.mag

    def __add__(self, other):
        return Vector(self.x*self.mag+other.x*other.mag, 
                      self.y*self.mag+other.y*other.mag)
    
    def __sub__(self, other):
        return Vector(self.x*self.mag-other.x*other.mag, 
                      self.y*self.mag-other.y*other.mag)
    
    # Multiplying by a vector means dot product
    # Multiplying by a number means scaling
    def __mul__(self, const):
        if type(const) == type(self):
            return (self.x * const.x + self.y * const.y) * self.mag * const.mag
        else:
            if const < 0:
                return Vector(-self.x, -self.y, self.mag*(-const))
            else:
                return Vector(self.x, self.y, self.mag*const)
    
    # Complex number product
    def __pow__(self, other):
        return Vector(self.x * other.x - self.y * other.y,
                      self.x * other.y + self.y * other.x,
                      self.mag * other.mag)
    
    def __xor__(self, other):
        # only sign matters
        return (self.x * other.y - self.y * other.x) * self.mag * other.mag 
    
    def __repr__(self):
        return f'Vector(({self.x}, {self.y}); {self.mag} --> ({self.x * self.mag}, {self.y * self.mag}))'
    
    def __iter__(self):
        yield self.x * self.mag
        yield self.y * self.mag
    
    def L(self):
        return list(self)
    
    def clone(self):
        v = Vector(0, 0)
        v.x = self.x
        v.y = self.y
        v.mag = self.mag
        return v


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return sqrt((self.x-other.x)**2+(self.y-other.y)**2)

    def __add__(self, vec : Vector):
        return Point(self.x+vec.x * vec.mag, self.y + vec.y * vec.mag)
    
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def L(self) -> list:
        return list(self)
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'


class LineSegment:
    def __init__(self, inip : Point, v : Vector):
        self.inip = inip
        self.v = v
    
    def dist(self, other):
        
        # self : p to p+r
        # other: q to q+ s

        pminusq = self.inip - other.inip # p - q
    
        r_cross_s = self.v ^ other.v
        qminusp_cross_r = self.v ^ pminusq
        # print('a')
        if abs(r_cross_s) < 0.000001:
            if abs(qminusp_cross_r) < 0.000001:
                
                # the two lines are collinear
                
                t0 = -(pminusq * self.v) / self.v.mag**2 # (q-p) dot r / |r|^2
                t1 = t0 + (other.v * self.v) / self.v.mag**2 # t0 + s dot r / |r|^2

                # print(t0)
                # print(t1)

                # we check
                if min(t0, t1) > 1 or max(t0, t1) < 0:
                    # no intersection with [0, 1] --> collinear and disjoint segments
                    return -1
                else:
                    # collinear and overlapping segments
                    if min(t0, t1) > 0:
                        return min(t0, t1) * self.v.mag
                    else:
                        return 0
            else:
                # the lines are parallel and not intersecting
                return -1
        else:
            t = (other.v ^ pminusq) / r_cross_s # (q-p) cross s / (r cross s)
            u = qminusp_cross_r / (r_cross_s)

            if 0 <= t <= 1 and 0 <= u <= 1:
                return t * self.v.mag
            else:
                return -1



