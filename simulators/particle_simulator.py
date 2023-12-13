import numpy as np
import json
from math import sqrt
import matplotlib.pyplot as plt

class ParticleSimulator:
    def __init__(
        self, 
        positions = [],
        connections = [],
        forces = [],
        restrictions = [],
        iterations = 600,
        step = 0.00004,
        particle_radius = 40.0,
        mass = 7850.0,
        k_constant = 21000000000.0,
    ):
        forces = np.array(forces)
        restrictions = np.array(restrictions)

        self.iterations = iterations  
        self.step = step  
        self.particle_radius = particle_radius
        self.mass = mass  
        self.k_constant = k_constant  
        self.connections = connections  
        self.total_size = len(connections) * 2
        self.n_particles = len(connections)
        self.positions = positions
        self.forces = np.reshape(np.transpose(forces),(self.total_size, 1))
        self.restrictions = np.reshape(np.transpose(restrictions),(self.total_size, 1))
        self.u = np.zeros((self.total_size, 1))
        self.v = np.zeros((self.total_size, 1))
        self.a = self.forces/self.mass
        self.fi = np.zeros((self.total_size, 1))

    def setData(self, data):

        positions = data["positions"]
        connections = data["connections"]
        forces = data["forces"]
        restrictions = data["restrictions"]
        self.__init__(positions, connections, forces, restrictions)

    def run(self, iterations):
        for _ in range(iterations):
            self.iteration()
        return self.u

    def iteration(self):        
        self.v += self.a * 0.5 * self.step
        self.u += self.v * self.step

        self.fi = np.zeros((self.total_size, 1))
        for j in range(self.n_particles):
            # pos index (x,y) of particle j
            jx = 2*j
            jy = 2*j+1
            if self.restrictions[jx] == 1:
                self.u[jx] = 0.0
            if self.restrictions[jy] == 1:
                self.u[jy] = 0.0

            # real position of particle j
            xj = self.positions[j][0] + self.u[jx][0]
            yj = self.positions[j][1] + self.u[jy][0]
            for connection_i in self.connections[j][:-1]:
                if connection_i == 0:
                    continue
                conn_index = connection_i - 1
                # pos index of particle i
                ix = 2*conn_index
                iy = 2*conn_index+1
                # real pos of particle i
                xi = self.positions[conn_index][0] + self.u[ix][0]
                yi = self.positions[conn_index][1] + self.u[iy][0]
                # Diference between center of particles
                dX = xj-xi
                dY = yj-yi
                # Distance between center of particles
                dist = sqrt(dX*dX + dY*dY)
                # Real distance between particles
                real_dist = dist - 2*self.particle_radius
                if real_dist < 0.001 and real_dist > -0.001:
                    continue
                # Real diference between particles
                dx = dX * real_dist/dist
                dy = dY * real_dist/dist
                if self.restrictions[jx] == 0:
                    self.fi[jx] += dx * self.k_constant
                if self.restrictions[jy] == 0:
                    self.fi[jy] += dy * self.k_constant
        self.a = (self.forces-self.fi)/self.mass
        self.v += self.a * 0.5 * self.step
        return self.u
    

if __name__ == "__main__":
    data = None
    with open("particle_test.json", "r") as file:
        data = json.load(file)
    p = ParticleSimulator()
    p.setData(data)
    px = []
    py = []
    for x in range(10000):
        p.iteration()
        px.append(x)
        py.append(p.u[0][0])
    
    plt.plot(px, py)
    plt.show()