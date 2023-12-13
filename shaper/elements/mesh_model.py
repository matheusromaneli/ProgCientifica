import json
from .mesh_point import MeshPoint
from simulators.temperature_simulator import TemperatureSimulator
from simulators.particle_simulator import ParticleSimulator

class MeshModel:
    temp_simulator = TemperatureSimulator()
    part_simulator = ParticleSimulator()
    def __init__(self):
        self.points: list[MeshPoint] = []
        self.curr_index = 1
        self.data = None

    def reset(self):
        """return to default values"""
        self.curr_index = 1
        self.points = []
        self.data = None

    def getSelectedPoints(self):
        """get selected points in mesh"""
        selected = []
        for pt in self.points:
            if pt.isSelected():
                selected.append(pt)
        return selected

    def setAttrs(self, temp, is_fixed, force_value, force_direction):
        """Set attrs on selected points"""
        for point in self.getSelectedPoints():
            point.setAttrs(temp,is_fixed,force_value,force_direction)

    def setSelected(self, moved, x1,y1,x2,y2):
        """
            If not moved: unselect all
            Else: select every point inside square x1,y1 to x2,y2
        """
        if not moved:
            for point in self.points:
                point.setSelected(False)
        else:
            for point in self.points:
                point.setSelected(point.isInside(x1, y1, x2, y2))

    def findPoint(self, _x, _y):
        """Find point based on position"""
        for point in self.points:
            if point.getX() == _x and point.getY() == _y:
                return point
        return None

    def append(self, point: MeshPoint):
        """Add point and increment index"""
        point.index = self.curr_index
        self.curr_index += 1
        self.points.append(point)

    def run_temperature(self):
        """run temperature simulator and update temperatures on points"""
        self.temp_simulator.setData(self.data)
        result = self.temp_simulator.run()
        for i in range(len(self.points)):
            self.points[i].temperature = result[i]
            self.points[i].default = False

    def run_particle(self):
        self.part_simulator.setData(self.data)
        result = self.part_simulator.run(3600)
        for i in range(0,len(result),2):
            cur_point = self.points[int(i/2)]
            res_x = cur_point.getX() + result[i][0]
            res_y = cur_point.getY() + result[i+1][0]
            cur_point.setX(res_x)
            cur_point.setY(res_y)


    def export_particle(self, size, file_name="data"):
        """export particle data to <file_name>.json"""
        positions = []
        connections = []
        forces = []
        restrictions = []

        for pt in self.points:
            positions.append(pt.pos)
            connections.append(pt.connection)
            forces += pt.force
            restrictions += [pt.is_fixed, pt.is_fixed]

        self.data = {
            "particle_size": size,
            "positions": positions,
            "connections": connections,
            "forces": forces,
            "restrictions": restrictions,
        }

        with open(f"{file_name}.json", "w") as file:
            json.dump(self.data, file)

    def export_temperature(self, file_name="data"):
        """export temperature data to <file_name>.json"""
        known_temp = []
        temperatures = []
        connections = []
        for pt in self.points:
            known_temp.append(1 if pt.temperature is not None else 0)
            temperatures.append(pt.temperature)
            connections.append(pt.connection)
            
        self.data = {
            "known_temp": known_temp,
            "temperatures": temperatures,
            "connections": connections,
        }

        with open(f"{file_name}.json", "w") as file:
            json.dump(self.data,file)
        
