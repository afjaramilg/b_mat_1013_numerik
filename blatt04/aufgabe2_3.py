import numpy as np
import math


A = np.array([[1, -2],
              [1, -1],
              [1,  0],
              [1,  1],
              [1,  2]])

b = np.array([1, 3, 6, 8, -4])


sqrt5 = math.sqrt(5)
sqrt10 = math.sqrt(10)

v1 = np.array([0, 1])
v2 = np.array([1, 0])

u1 = 1/sqrt10 * (A @ v1)
u2 = 1/sqrt5 * (A @ v2)
ui = np.zeros(5);

E = np.array([[sqrt10,     0],
              [0     , sqrt5],
              [0     ,     0],
              [0     ,     0],
              [0     ,     0]])

Ep = np.array([[1/sqrt10,       0, 0, 0, 0],
               [0       , 1/sqrt5, 0, 0, 0]])

V = np.array([[0, 1],
              [1, 0]]);


U = np.array([u1, u2, ui, ui, ui]).T

Ap = V @ Ep @ U.T

print(A.T @ A)
print("-----")
print(A.T @ b)
print("-----")
print(A @ v1)
print("-----")
print(U @ E @ V.T)
print("-----")
print(Ap @ A)
print("-----")
print(Ap)
print("-----")
print(U)
print("-----")
print(Ap @ b)
