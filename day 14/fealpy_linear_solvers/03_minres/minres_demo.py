"""
minres —— 最小残量法演示
========================
构造对称不定矩阵 (Helmholtz)，minres 正常求解。
CG 在同矩阵上会崩溃（不满足正定性）。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.solver import minres
from common import (
    make_sym_indefinite_matrix, make_rhs, scipy_to_fealpy, residual
)

def main():
    n = 20
    A_scipy = make_sym_indefinite_matrix(n, k=5.0)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    # 验证不定性
    ew = np.linalg.eigvalsh(A_scipy.toarray())
    n_neg, n_pos = np.sum(ew < 0), np.sum(ew > 0)
    print("=" * 60)
    print("  MINRES — 最小残量法")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} 对称不定 (1D Helmholtz, k=5)")
    print(f"  特征值: {n_pos} 正, {n_neg} 负, min={ew[0]:.1f}, max={ew[-1]:.1f}")
    print(f"  → CG 在此矩阵上会崩溃！")

    x_mr, info = minres(A, b, rtol=1e-8, atol=1e-12)
    res = residual(A, x_mr, b)
    print(f"  迭代次数: {info['niter']}")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → MINRES 成功求解了对称不定系统。")

if __name__ == "__main__":
    main()
