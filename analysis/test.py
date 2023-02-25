import numpy as np
import math
# from numpy import matrix
#from numpy import linalg


def matrix_invmod(input_matrix, mod):  # Finds the inverse of matrix A by mod p
    def minor(matrix, i, j):  # caclulate minor
        matrix = np.array(matrix)
        minor = np.zeros(shape=(len(matrix) - 1, len(matrix) - 1))
        p = 0
        for s in range(0, len(minor)):
            if p == i:
                p = p + 1
            q = 0
            for t in range(0, len(minor)):
                if q == j:
                    q = q + 1
                minor[s][t] = matrix[p][q]
                q = q + 1
            p = p + 1
        return minor

    n = len(input_matrix)
    input_matrix = np.matrix(input_matrix)
    adj = np.zeros(shape=(n, n))
    for i in range(0, n):
        for j in range(0, n):
            adj[i][j] = ((-1) ** (i + j) * int(round(np.linalg.det(minor(input_matrix, j, i))))) % mod
    return (pow(int(round(np.linalg.det(input_matrix))), -1, mod) * adj) % mod



M3 = np.array([[2., 1., 1.], [1., -1., 0.]]) # Матрица (левая часть системы)
v3 = np.array([2., -2., 2.]) # Вектор (правая часть системы)

print(np.linalg.solve(M3, v3))