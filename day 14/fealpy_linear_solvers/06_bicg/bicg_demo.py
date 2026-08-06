"""
bicg —— 双共轭梯度法演示
========================
非对称矩阵上展示 BiCG 的短递推特性。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fealpy.backend import backend_manager as bm
from fealpy.solver import bicg
from common import (
    make_nonsymmetric_matrix, make_rhs, scipy_to_fealpy, residual
)

def main():
    n = 20
    A_scipy = make_nonsymmetric_matrix(n)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    print("=" * 60)
    print("  BiCG — 双共轭梯度法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} 非对称 (对流-扩散)")
    print(f"  特点: 短递推 (O(n) 存储), 需要 Aᵀ 乘法")

    x_bi, info = bicg(A, b, rtol=1e-8, atol=1e-12)
    res = residual(A, x_bi, b)
    print(f"  迭代次数: {info['niter']}")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → BiCG 短递推，适合存储受限场景，但稳定性不如 BiCGSTAB。")

if __name__ == "__main__":
    main()
