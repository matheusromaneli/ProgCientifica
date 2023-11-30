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

func = np.array([-1,-1,-1,-1,4])

A = np.zeros((16,16))
b = np.zeros(16)
for conn in connections:
    current_term = conn[-1]-1
    for i in range(len(func)):
        if conn[i] == 0:
            continue
        if i < 4 and known_temp[conn[i]-1] == 1:
            b[current_term] += temperatures[conn[i]-1]
            continue
        A[current_term][conn[i]-1] = func[i]

print(A)
print(b)
x = np.linalg.solve(A,b)
for i in range(4):
    for j in range(4):
        curr = i*4+j
        print(f'({curr+1})',x[curr], end=', ')
    print()