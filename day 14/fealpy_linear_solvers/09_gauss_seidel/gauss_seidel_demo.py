"""
gauss_seidel — Gauss-Seidel 迭代法演示
=======================================
手动实现 GS 迭代，展示「立即用最新值」的核心思想。
FEALPy 内置版依赖 MUMPS（当前环境不可用），此处用手动实现教学。
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

    # Gauss-Seidel: x_i^{(k+1)} = (b_i - Σ_{j<i} a_{ij} x_j^{(k+1)}
    #                                      - Σ_{j>i} a_{ij} x_j^{(k)}) / a_{ii}
    x = np.zeros(n)
    rho_jac = np.cos(np.pi / (n + 1))
    print("=" * 60)
    print("  Gauss-Seidel — 迭代法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} SPD (1D Poisson)")
    print(f"  ||b|| = {b_norm:.2f}")
    print(f"  谱半径 ρ_GS ≈ ρ_Jacobi² ≈ {rho_jac**2:.4f}  (vs Jacobi ρ ≈ {rho_jac:.4f})")
    print(f"  核心: x_i 更新后立即用于后续分量的计算")
    print()

    for k in range(1, 2001):
        x_old = x.copy()
        for i in range(n):
            s = b_np[i]
            for j in range(n):
                if j != i:
                    s -= A_dense[i, j] * x[j]  # 用当前最新值！
            x[i] = s / A_dense[i, i]
        r = b_np - A_dense @ x
        res = np.linalg.norm(r)
        if res < 1e-8 * b_norm:
            print(f"  迭代次数: {k}")
            print(f"  残差 ||b-Ax||₂ = {res:.2e}")
            print(f"  相对残差 = {res/b_norm:.2e}")
            print(f"  → GS 约为 Jacobi 收敛速度的 2 倍（谱半径取平方）。")
            print(f"  → 代价：不可直接并行化（分量间有顺序依赖）。")
            break
    else:
        res = np.linalg.norm(b_np - A_dense @ x)
        print(f"  迭代次数: 2000 (未收敛), 残差 = {res:.2e}")

    # 展示 FEALPy 接口（注意 MUMPS 依赖）
    print(f"\n  FEALPy 调用形式:")
    print(f"    from fealpy.solver import gauss_seidel")
    print(f"    x, info = gauss_seidel(A, b, rtol=1e-8, returninfo=True)")
    print(f"  ⚠ 需要 MUMPS (PyMUMPS + libmumps-dev)，当前环境不可用。")

if __name__ == "__main__":
    main()
