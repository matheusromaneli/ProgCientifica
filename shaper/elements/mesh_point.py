from hetool.geometry.point import Point
from math import sqrt

class MeshPoint(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temperature = None
        self.is_fixed = 0
        self.force_value = 0
        self.force_direction = (0,0)
        self.default = True
        self.index = 0
        self.left = 0
        self.right = 0
        self.bottom = 0
        self.top = 0
    
    @property
    def connection(self):
        """connection struct"""
        return [self.left, self.right, self.bottom, self.top, self.index]
    
    @property
    def pos(self):
        return [self.getX(), self.getY()]

    @property
    def force(self):
        """derivative force based on direction"""
        fx,fy = self.normalize(self.force_direction[0], self.force_direction[1])
        return [fx*self.force_value, fy*self.force_value]

    @property
    def color(self):
        """color based on information inside point"""
        if self.isSelected():
            return (1.0,0.0,0.0)
        if self.default:
            return (1.0, 1.0, 1.0)
        return (abs(self.temperature/99), abs(self.force_value/99) ,1 if self.is_fixed else 0)

    def setAttrs(self, temp, is_fixed, force_value, force_direction):
        """Add attributes if different than default"""
        if not (temp or is_fixed or force_value or force_direction[0] or force_direction[1]):
            return 
        self.temperature = temp
        self.is_fixed = is_fixed
        self.force_value = force_value
        self.force_direction = force_direction
        self.default = False

    def normalize(self,x,y):
        dist = sqrt(x*x+y*y)
        if dist > 0.0:
            return x/dist, y/dist
        else:
            return 0,0