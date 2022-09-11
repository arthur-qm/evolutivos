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
            return (self.x * const.x + self.y * const.y) * self.mag
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
    
    def __add__(self, vec : Vector):
        return Point(self.x+vec.x * vec.mag, self.y + vec.y * vec.mag)
    
    def __sub__(self, other):
        return Vector(self.y-other.y, self.x-other.x)

    def __iter__(self):
        yield self.x
        yield self.y

    def L(self) -> list:
        return list(self)
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'


class Line:
    def __init__(self, iniv, v : Vector):
        self.inipoint = iniv
        self.v = v.normalized()
    

class Circle:
    def __init__(self, center, R):
        self.center = center
        self.R = R
    
    def line_intersection(self, line : Line):
        point_to_center = self.center - line.inipoint
        dist_to_line = point_to_center * line.v.rot90anti()
        
        if abs(dist_to_line) > self.R:
            return []

        interdist = sqrt(self.R**2 - dist_to_line**2)
        projection = self.center - line.v.rot90anti() * dist_to_line

        return [projection - line.v * interdist, projection + line.v * interdist]

