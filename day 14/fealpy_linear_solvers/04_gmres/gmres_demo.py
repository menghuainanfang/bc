"""
gmres —— 广义最小残量法演示
===========================
构造非对称矩阵 (对流-扩散)，GMRES 成功求解。
展示 restart 参数对收敛的影响。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.solver import gmres
from common import (
    make_nonsymmetric_matrix, make_rhs, scipy_to_fealpy, residual
)

def main():
    n = 20
    A_scipy = make_nonsymmetric_matrix(n, eps=0.1, v=1.0)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    # 验证非对称性
    asym = np.linalg.norm((A_scipy - A_scipy.T).data)
    print("=" * 60)
    print("  GMRES — 广义最小残量法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} 非对称 (对流-扩散, ε=0.1, v=1.0)")
    print(f"  ||A-Aᵀ|| = {asym:.2e}")

    x_gm, info = gmres(A, b, rtol=1e-8, atol=1e-12, restart=20)
    res = residual(A, x_gm, b)
    print(f"  迭代次数: {info['niter']} (内部 Arnoldi 步累计)")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → GMRES 是求解非对称系统的「黄金标准」。")
    print(f"  → 注意：内存 O(restart·n)，长迭代需权衡重启间隔。")

if __name__ == "__main__":
    main()
