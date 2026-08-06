"""
综合对比 —— 同一 SPD 矩阵, 全部求解器
=====================================
50×50 SPD 矩阵，精确解含 2 个特征模态。
Krylov 方法 2 步收敛；平稳迭代方法展示谱半径决定的慢收敛。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.solver import (
    spsolve, cg, minres, gmres, lgmres, bicg, bicgstab,
)
from common import (
    make_spd_matrix, make_rhs, scipy_to_fealpy, residual
)

def main():
    n = 50
    h = 1.0 / (n + 1)
    A_scipy = make_spd_matrix(n)
    x_exact, b_np = make_rhs(A_scipy, n)
    A = scipy_to_fealpy(A_scipy)
    b = bm.tensor(b_np)
    b_norm_scalar = float(bm.linalg.norm(b))

    # 谱半径估计
    rho_jac = np.cos(np.pi * h)
    print("=" * 62)
    print("  综合对比: 同一 SPD 矩阵 (n=50), 全部求解器")
    print("=" * 62)
    print(f"  精确解: u(x)=sin(πx)+0.5sin(3πx)  [2 个特征模态]")
    print(f"  ||b||={b_norm_scalar:.1f},  谱半径 ρ(Jacobi)≈cos(πh)≈{rho_jac:.4f}")
    print(f"  ρ(GS)≈ρ²≈{rho_jac**2:.4f}")
    print()

    results = []

    # --- 直接法 ---
    x = spsolve(A, b, solver="scipy")
    results.append(("spsolve", "—", residual(A, x, b)))

    # --- 手动 Jacobi (FEALPy 内置版判据有问题) ---
    A_dense = A_scipy.toarray()
    D_inv = np.diag(1.0 / np.diag(A_dense))
    L_plus_U = A_dense - np.diag(np.diag(A_dense))
    x_jac = np.zeros(n)
    jac_niter = 0
    for k in range(1, 5001):
        x_jac = D_inv @ (b_np - L_plus_U @ x_jac)
        r = np.linalg.norm(b_np - A_dense @ x_jac)
        if r < 1e-8 * b_norm_scalar:
            jac_niter = k; break
    res_jac = float(np.linalg.norm(b_np - A_dense @ x_jac))
    results.append(("Jacobi", jac_niter if jac_niter else ">5000", res_jac))

    # --- 手动 Gauss-Seidel ---
    x_gs = np.zeros(n)
    gs_niter = 0
    for k in range(1, 5001):
        for i in range(n):
            s = b_np[i] - A_dense[i, :i] @ x_gs[:i] - A_dense[i, i+1:] @ x_gs[i+1:]
            x_gs[i] = s / A_dense[i, i]
        r = np.linalg.norm(b_np - A_dense @ x_gs)
        if r < 1e-8 * b_norm_scalar:
            gs_niter = k; break
    res_gs = float(np.linalg.norm(b_np - A_dense @ x_gs))
    results.append(("Gauss-Seidel", gs_niter if gs_niter else ">5000", res_gs))

    # --- Krylov 迭代 ---
    x, info = cg(A, b, rtol=1e-8, atol=1e-12, returninfo=True)
    results.append(("CG", info['niter'], residual(A, x, b)))

    for name, func in [("MINRES", minres), ("GMRES", gmres),
                       ("LGMRES", lgmres), ("BiCG", bicg), ("BiCGSTAB", bicgstab)]:
        x, info = func(A, b, rtol=1e-8, atol=1e-12)
        results.append((name, info.get('niter', '?'), residual(A, x, b)))

    # 打印
    print(f"  {'求解器':<16s} {'迭代':>6s}  {'残差':>14s}  {'相对残差':>12s}")
    print(f"  {'─'*16} {'─'*6}  {'─'*14}  {'─'*12}")
    for name, nit, res in results:
        ns = str(nit)
        rrel = res / b_norm_scalar if not np.isnan(res) else float('nan')
        print(f"  {name:<16s} {ns:>6s}  {res:>14.6e}  {rrel:>12.2e}")

    print(f"\n  ★ Krylov 方法 2~3 步收敛：精确解 = 2 个特征模态的线性组合。")
    print(f"  ★ Jacobi: 谱半径 ≈ {rho_jac:.4f} → 收敛极慢。")
    print(f"  ★ GS: 谱半径 ≈ {rho_jac**2:.4f} → 比 Jacobi 快约 1 倍，仍远慢于 Krylov。")
    print(f"  ★ 平稳迭代法在现代 FEM 中多用作多重网格光滑子。")

if __name__ == "__main__":
    main()
