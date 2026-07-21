import numpy as np
from scipy.sparse import diags

# 用稀疏格式创建 N=100 的刚度矩阵
N = 100
h = 1.0 / (N - 1)
main_diag = 2 * np.ones(N) / h
off_diag = -np.ones(N - 1) / h
K_sparse = diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')

print("非零元素数:", K_sparse.nnz)
print("稠密存储元素数:", N * N)
print("稀疏比:", K_sparse.nnz / (N * N) * 100, "%")

# 观察条件数随 N 增长
for N_test in [10, 50, 100, 500]:
    h_t = 1.0 / (N_test - 1)
    K_t = diags([-np.ones(N_test-1)/h_t, 2*np.ones(N_test)/h_t, -np.ones(N_test-1)/h_t],
                [-1, 0, 1]).toarray()
    K_bc = K_t[1:-1, 1:-1]  # 施加 Dirichlet BC 后
    cond = np.linalg.cond(K_bc)
    print(f"N={N_test:4d}, cond(K)≈{cond:.2e}, N²={N_test**2}")