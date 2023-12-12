import numpy as np
from math import sqrt

class ParticleSimulator:
    def __init__(
        self, 
        positions = [],
        connections = [],
        forces = [],
        restrictions = [],
        iterations = 600,
        step = 0.00004,
        particle_radius = 1.0,
        mass = 7800.0,
        k_constant = 210000000000.0,
    ):
         
        positions = np.array(positions)
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
        self.positions = np.transpose(positions)  
        self.forces = np.reshape(np.transpose(forces),(self.total_size, 1))
        self.restrictions = np.reshape(np.transpose(restrictions),(self.total_size, 1))
        self.u = np.zeros(self.total_size, 1)
        self.v = np.zeros(self.total_size, 1)
        self.a = np.zeros(self.total_size, 1)
        self.fi = np.zeros(self.total_size,1)

    def setData(self, data):
        positions = data["positions"]
        connections = data["connections"]
        forces = data["forces"]
        restrictions = data["restrictions"]
        self.__init__(positions, connections, forces, restrictions)

    def run(self):
        response = np.zeros(self.iterations)

        for _ in range(self.iterations):
            self.iteration()
            response.append(np.copy(self.u))
        return response

    def iteration(self):
        self.a = (self.forces-self.fi)/self.mass
        self.v += self.a * (0.5 * self.step)
        self.u += self.v * self.step

        self.fi = np.zeros(self.total_size, 1)
        for j in self.n_particles:
            # pos index (x,y) of particle j
            jx = 2*j-1
            jy = 2*j
            if self.restrictions[jx] == 1:
                self.u[jx] = 0.0
            if self.restrictions[jy] == 1:
                self.u[jy] = 0.0

            # real position of particle j
            xj = self.positions[j][0] + self.u[jx]
            yj = self.positions[j][1] + self.u[jy]
            for connection_i in self.connections[j]:
                # pos index of particle i
                ix = 2*connection_i-1
                iy = 2*connection_i

                # real pos of particle i
                xi = self.positions[connection_i][0] + self.u[ix]
                yi = self.positions[connection_i][1] + self.u[iy]
                # Diference between center of particles
                dX = xj-xi
                dY = yj-yi
                # Distance between center of particles
                dist = sqrt(dX*dX + dY*dY)
                # Real distance between particles
                real_dist = dist - 2*self.particle_radius
                # Real diference between particles
                dx = dX * real_dist/dist
                dy = dY * real_dist/dist

                self.fi[jx] += dx * self.k_constant
                self.fi[jy] += dy * self.k_constant
        return self.u