"""
lgmres —— 增广 GMRES 演示
=========================
同非对称矩阵，展示 LGMRES 的 outer_k 增广机制。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.solver import lgmres
from common import (
    make_nonsymmetric_matrix, make_rhs, scipy_to_fealpy, residual
)

def main():
    n = 20
    A_scipy = make_nonsymmetric_matrix(n, eps=0.1, v=1.0)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)

    print("=" * 60)
    print("  LGMRES — 增广 GMRES")
    print("=" * 60)
    print(f"  矩阵: {n}×{n} 非对称 (对流-扩散)")
    print(f"  参数: inner_m=20, outer_k=3")

    x_lg, info = lgmres(A, b, rtol=1e-8, atol=1e-12, inner_m=20, outer_k=3)
    res = residual(A, x_lg, b)
    print(f"  迭代次数: {info['niter']} (内部 Arnoldi 步累计)")
    print(f"  残差 ||b-Ax||₂ = {res:.2e}")
    print(f"  → LGMRES 通过 outer_k 个外部向量增广子空间，")
    print(f"    缓解了 GMRES 重启时的信息丢失。")

if __name__ == "__main__":
    main()
