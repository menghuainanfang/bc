"""
jacobi — Jacobi 迭代法演示
===========================
手动实现 Jacobi 迭代，展示分量更新公式和收敛行为。
FEALPy 内置版因 MUMPS 判据适配问题，此处用手动实现教学。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from common import make_spd_matrix, make_rhs

def main():
    n = 10
    A_scipy = make_spd_matrix(n)
    x_exact, b_np = make_rhs(A_scipy, n)
    A_dense = A_scipy.toarray()
    b_norm = np.linalg.norm(b_np)

    # Jacobi: x_new = D^{-1} (b - (L+U) x_old)
    D = np.diag(np.diag(A_dense))
    D_inv = np.diag(1.0 / np.diag(A_dense))
    L_plus_U = A_dense - D

    x = np.zeros(n)
    print("=" * 60)
    print("  Jacobi — 迭代法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} SPD (1D Poisson)")
    print(f"  ||b|| = {b_norm:.2f},  谱半径 ρ ≈ cos(πh) ≈ {np.cos(np.pi/(n+1)):.4f}")
    print("  公式: x_i^(k+1) = (b_i - sum_{j!=i} a_ij x_j^(k)) / a_ii")
    print()

    for k in range(1, 2001):
        x_new = D_inv @ (b_np - L_plus_U @ x)
        r = b_np - A_dense @ x_new
        res = np.linalg.norm(r)
        x = x_new
        if res < 1e-8 * b_norm:
            print(f"  迭代次数: {k}")
            print(f"  残差 ||b-Ax||₂ = {res:.2e}")
            print(f"  相对残差 = {res/b_norm:.2e}")
            print(f"  → Jacobi 实现简单、天然可并行，但收敛慢。")
            break
    else:
        res = np.linalg.norm(b_np - A_dense @ x)
        print(f"  迭代次数: 2000 (未收敛)")
        print(f"  残差 = {res:.2e}")
        print(f"  → 谱半径接近 1 导致收敛极慢。")

    # 展示 FEALPy 调用形式
    print(f"\n  FEALPy 调用形式:")
    print(f"    from fealpy.solver import jacobi")
    print(f"    x, info = jacobi(A, b, rtol=1e-8, returninfo=True)")

if __name__ == "__main__":
    main()
