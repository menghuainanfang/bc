"""
cg —— 共轭梯度法演示
====================
构造 SPD 矩阵，用 cg 求解。精确解含 2 个特征模态，
恰好展示"Krylov 子空间维数 = 收敛步数"的理论性质。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import make_spd_matrix, make_rhs, scipy_to_fealpy, residual
from fealpy.backend import backend_manager as bm
from fealpy.solver import cg

def main():
    n = 10
    A_scipy = make_spd_matrix(n)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    x_cg, info = cg(A, b, rtol=1e-8, atol=1e-12, returninfo=True)
    res = residual(A, x_cg, b)

    print("=" * 60)
    print("  CG — 共轭梯度法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} SPD (1D Poisson)")
    print(f"  精确解: u(x)=sin(πx)+0.5sin(3πx)  [含 2 个特征模态]")
    print(f"  迭代次数: {info['niter']}")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → 恰好 {info['niter']} 步收敛：Krylov 子空间维数 = 固有模态数。")
    print(f"  → CG 是 SPD 系统的首选迭代法。")

if __name__ == "__main__":
    main()
