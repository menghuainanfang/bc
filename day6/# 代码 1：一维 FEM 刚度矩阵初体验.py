# 代码 1：一维 FEM 刚度矩阵初体验
import numpy as np
import matplotlib.pyplot as plt

# 创建 N=5 的一维刚度矩阵
N = 5
h = 1.0 / (N - 1)
K = np.zeros((N, N))
for i in range(N - 1):
    Ke = np.array([[1, -1], [-1, 1]]) / h
    K[i:i+2, i:i+2] += Ke

print("刚度矩阵 K:\n", K)
print("对称?", np.allclose(K, K.T))
eigvals = np.linalg.eigvalsh(K)
print("特征值:", eigvals)
print("全部正定?", np.all(eigvals > 0))