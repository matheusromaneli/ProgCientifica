import json
from .mesh_point import MeshPoint
from simulators.temperature_simulator import TemperatureSimulator

class MeshModel:
    temp_simulator = TemperatureSimulator()
    def __init__(self):
        self.points: list[MeshPoint] = []
        self.curr_index = 1
        self.data = None

    def reset(self):
        self.curr_index = 1
        self.points = []
        self.data = None

    def getSelectedPoints(self):
        selected = []
        for pt in self.mesh.points:
            if pt.isSelected():
                selected.append(pt)
        return selected

    def findPoint(self, _x,_y):
        for point in self.points:
            if point.getX() == _x and point.getY() == _y:
                return point
        return None

    def append(self, point: MeshPoint):
        point.index = self.curr_index
        self.curr_index += 1
        self.points.append(point)

    def run_temperature(self):
        self.temp_simulator.setData(self.data)
        result = self.temp_simulator.run()
        for i in range(len(self.points)):
            self.points[i].temperature = result[i]
            self.points[i].default = False

    def export_temperature(self):
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

        with open("data.json", "w") as file:
            json.dump(self.data,file)
        
