import numpy as np 
import matplotlib.pyplot as plt 
import scipy.sparse.linalg

P = np.array([
    [0, 0.75, 0.35, 0.25, 0.85],
    [0.15, 0 , 0.35, 0.25, 0.05],
    [0.15, 0.15, 0, 0.25, 0.05],
    [0.15, 0.05, 0.05, 0, 0.05],
    [0.55, 0.05, 0.25, 0.25, 0]
    ])

X0 = np.array([[0], [0], [0], [1], [0]])

X1 = P @ X0

print(f'Sum of columns of P: {sum(P)}')
print(f'X1:\n{X1}')

X = np.array([[0],[0],[0],[0],[0]])
m = 20

for t in range(m):
    X = P @ X 

print(X)

eigenvalues, eigenvecs = np.linalg.eig(P)
print(f'Eigenvalues of P:\n{eigenvalues}\n\nEigenvectors of P\n{eigenvecs}')

X_inf = eigenvecs[:,0]
print(f"Eigenvector corresponding to the eigenvalue 1:\n{X_inf[:,np.newaxis]}")

X_inf = X_inf/sum(X_inf)
print(f"Long-run probabilities of being at each webpage:\n{X_inf[:,np.newaxis]}")


