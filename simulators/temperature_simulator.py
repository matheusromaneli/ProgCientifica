import numpy as np

'''
            25
        v  v  v  v
    > 13 14 15 16 <
100 >  9 10 11 12 < 0
    >  5  6  7  8 <
    >  1  2  3  4 <
       ^  ^  ^  ^
           75
'''

class TemperatureSimulator:
    def __init__(self, known_temp = None, temperatures = None, connections = None):
        self.known_temp = known_temp
        self.temperatures = temperatures
        self.connections = connections
    
    def setData(self, data):
        self.known_temp = data["known_temp"]
        self.temperatures = data["temperatures"]
        self.connections = data["connections"]

    def run(self):
        """Run Simulation and return values of points."""
        size = len(self.connections)
        A = np.zeros((size,size))
        b = np.zeros(size)
        func = np.array([-1,-1,-1,-1,4])
        for conn in self.connections:
            current_term = conn[-1]-1
            for i in range(len(func)):
                if conn[i] == 0:
                    continue
                if i < 4 and self.known_temp[conn[i]-1] == 1:
                    b[current_term] += self.temperatures[conn[i]-1]
                    continue
                A[current_term][conn[i]-1] = func[i]

        return np.linalg.solve(A,b)

if __name__ == "__main__":
    known_temp = np.array([
        1,1,1,1,
        1,0,0,1,
        1,0,0,1,
        1,1,1,1,
    ])

    temperatures = np.array([
        87 ,75,75,37,
        100, 0, 0, 0,
        100, 0, 0, 0,
        62 ,25,25,12
    ])

    ''' Stradil
            4
            |
    1 -- 5 -- 2
            |
            3
    '''
    connections = np.array([
        [0, 2, 0, 5, 1],
        [1, 3, 0, 6, 2],
        [2, 4, 0, 7, 3],
        [3, 0, 0, 8, 4],
        [0, 6, 1, 9, 5],
        [5, 7, 2, 10, 6],
        [6, 8, 3, 11, 7],
        [7, 0, 4, 12, 8],
        [0, 10, 5, 13, 9],
        [9, 11, 6, 14, 10],
        [10, 12, 7, 15, 11],
        [11, 0, 8, 16, 12],
        [0, 14, 9, 0, 13],
        [13, 15, 10, 0, 14],
        [14, 16, 11, 0, 15],
        [15, 0, 12, 0, 16],
    ])

    ts = TemperatureSimulator(known_temp, temperatures, connections)
    x = ts.run()
    for i in range(4):
        for j in range(4):
            curr = i*4+j
            print(f'({curr+1})',x[curr], end=', ')
        print()