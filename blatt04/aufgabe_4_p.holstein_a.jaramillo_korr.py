# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np


# %% [markdown]
# # Computation of Q and R

# %%
# Algorithmus 7.2 aus dem Skript
def qr_decomposition(A):
    if type(A) not in [np.matrix, np.array]:
        raise TypeError("Input A is not a numpy matrix or array")
    
    R = np.matrix(np.zeros(A.shape))

    Q = np.matrix(np.zeros(A.shape))

    # A.shape[0] ist die Laenge einer Zeile == Anzahl der Spalten
    for k in range(0,A.shape[0]):
        for i in range(0,k-1):
            R[i,k] = np.cross(Q[:,i].H, A[:,k])
        intermediate_result = np.zeros((Q.shape[0],1))
        for i in range(0, k-1):
            intermediate_result = intermediate_result + np.cross(A[:,k].H, Q[:,i]) * Q[:,i] 
        Q[:,k] = A[:,k] - intermediate_result
        R[k,k] = np.linalg.norm(Q[:,k], None)
        Q[:,k] = Q[:,k] / R[k,k]
    return Q,R


# %% [markdown]
# # Solve Rx = Q*A*b

# %%
def solve_by_backward_propagation(r, c):
    x = np.matrix(np.zeros((r.shape[1], 1)))

    for i in range(r.shape[0]-1,-1,-1):
        matrix_row_x = 0
        for j in range(i+1,r.shape[0]):
            matrix_row_x += r[i,j] * x[j]
        x[i] = (c[i] - matrix_row_x) / r[i,i]

    return x


# %% [markdown]
# # Inputs

# %%
A = np.matrix([[1, -2],
              [1, -1],
              [1,  0],
              [1,  1],
              [1,  2]])

b = np.matrix([1, 3, 6, 8, -4]).T

q_and_r = qr_decomposition(A.T @ A)

Q, R = q_and_r

x = solve_by_backward_propagation(R, Q.H @ A.H @b)

print("die Ausgleichsgerade, durch welche die Messwerte y^ mit dem kleinsten quadratischen Fehler aproximiert werden ist:")
if x[1,0] > 0:
    print(f"y = {x[0,0]} + {x[1,0]}x")
elif x[1,0] < 0:
    print(f"y = {x[0,0]} {x[1,0]}x")
else:
    print(f"y = {x[0,0]}")

# %%

# %% [markdown]
# # Korrekturanmerkungen
# + 
#
# 4/4

# %% [markdown]
#
