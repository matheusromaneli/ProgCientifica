from hetool.geometry.point import Point

class MeshPoint(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temperature = None
        self.is_fixed = False
        self.force_value = 0
        self.force_direction = (0,0)
        self.default = True
        self.pos = [0,0]
        self.index = 0
        self.left = 0
        self.right = 0
        self.bottom = 0
        self.top = 0
    
    @property
    def connection(self):
        return [self.left, self.right, self.bottom, self.top, self.index]
    
    @property
    def color(self):
        if self.isSelected():
            return (1.0,0.0,0.0)
        if self.default:
            return (1.0, 1.0, 1.0)
        return (abs(self.temperature/99), abs(self.force_value/99) ,1 if self.is_fixed else 0)

    def setAttrs(self, temp, is_fixed, force_value, force_direction):
        if not (temp or is_fixed or force_value or force_direction[0] or force_direction[1]):
            return 
        self.temperature = temp
        self.is_fixed = is_fixed
        self.force_value = force_value
        self.force_direction = force_direction
        self.default = False