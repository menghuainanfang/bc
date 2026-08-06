"""
spsolve —— 稀疏直接法演示
=========================
构造 SPD 矩阵，用 spsolve 直接求解，验证机器精度残差。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.solver import spsolve
from common import make_spd_matrix, make_rhs, scipy_to_fealpy, residual

def main():
    n = 100
    A_scipy = make_spd_matrix(n)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    x = spsolve(A, b, solver="scipy")
    res = residual(A, x, b)
    err = float(np.linalg.norm(bm.to_numpy(x) - x_exact))

    print("=" * 60)
    print("  spsolve — 稀疏直接法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} SPD (1D Poisson)")
    print(f"  后端: scipy")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  误差 ||x-x*||₂  = {err:.2e}")
    print(f"  → 直接法给出机器精度级别结果。")

if __name__ == "__main__":
    main()
