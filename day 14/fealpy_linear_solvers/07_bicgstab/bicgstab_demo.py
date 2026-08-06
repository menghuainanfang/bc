"""
bicgstab —— 稳定双共轭梯度法演示
================================
非对称矩阵上展示 BiCGSTAB。对比 BiCG：不需要 Aᵀ，收敛更平滑。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fealpy.backend import backend_manager as bm
from fealpy.solver import bicgstab
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
    print("  BiCGSTAB — 稳定双共轭梯度法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} 非对称 (对流-扩散)")
    print(f"  特点: 短递推 + 平滑步 → 收敛稳定且不需要 Aᵀ")

    x_bs, info = bicgstab(A, b, rtol=1e-8, atol=1e-12)
    res = residual(A, x_bs, b)
    print(f"  迭代次数: {info['niter']}")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → BiCGSTAB 是非对称系统的实用首选。")

if __name__ == "__main__":
    main()
