"""
FEALPy 线性求解器演示 —— 共享工具模块
======================================
提供三类测试矩阵的构造函数和辅助函数。
每个求解器 demo 可通过 `from common import ...` 引入。
"""
import numpy as np
from scipy.sparse import diags, csr_matrix, eye as speye

from fealpy.backend import backend_manager as bm
from fealpy.sparse import CSRTensor

# ============================================================
# 矩阵构造函数
# ============================================================

def make_spd_matrix(n: int = 10):
    """
    对称正定 (SPD) 矩阵 —— 1D Poisson 方程 -u'' = f 的中心差分离散

        A = (1/h²) · tridiag(-1, 2, -1)

    适用求解器：spsolve, cg, jacobi, gauss_seidel
    """
    h = 1.0 / (n + 1)
    main = (2.0 / h**2) * np.ones(n)
    off  = (-1.0 / h**2) * np.ones(n - 1)
    return diags([off, main, off], [-1, 0, 1], format='csr')


def make_sym_indefinite_matrix(n: int = 10, k: float = 5.0):
    """
    对称不定矩阵 —— 1D Helmholtz 方程 -u'' - k²u = f

        A = A_poisson - k²·I

    k 足够大时部分特征值变负。对称但不定 → CG 不适用，minres 适用。
    """
    A_poisson = make_spd_matrix(n)
    return A_poisson - (k**2) * speye(n, format='csr')


def make_nonsymmetric_matrix(n: int = 10, eps: float = 0.1, v: float = 1.0):
    """
    非对称矩阵 —— 1D 对流-扩散方程 -ε u'' + v u' = f 的迎风差分离散

        A = ε·A_poisson + A_advection (迎风，非对称)

    适用求解器：gmres, lgmres, bicg, bicgstab
    """
    h = 1.0 / (n + 1)

    # 扩散 (对称)
    main_d = (2.0 * eps / h**2) * np.ones(n)
    off_d  = (-eps / h**2) * np.ones(n - 1)
    A_diff = diags([off_d, main_d, off_d], [-1, 0, 1], format='csr')

    # 对流 (非对称 —— 迎风)
    main_a = (v / h) * np.ones(n)
    low_a  = (-v / h) * np.ones(n - 1)
    A_adv  = diags([low_a, main_a], [-1, 0], format='csr')

    return A_diff + A_adv


# ============================================================
# 精确解 & 右端向量
# ============================================================

def exact_solution_sinsum(x):
    """u(x) = sin(πx) + 0.5 sin(3πx) —— 含 2 个特征模态，非单一特征向量"""
    return np.sin(np.pi * x) + 0.5 * np.sin(3.0 * np.pi * x)


def make_rhs(A_scipy, n, solution_func=exact_solution_sinsum):
    """给定矩阵和精确解函数，构造右端向量 b = A·x_exact"""
    h = 1.0 / (n + 1)
    x_nodes = np.linspace(h, 1 - h, n)
    x_exact = solution_func(x_nodes)
    return x_exact, A_scipy @ x_exact


# ============================================================
# FEALPy 格式转换 & 残差
# ============================================================

def scipy_to_fealpy(A_scipy: csr_matrix) -> CSRTensor:
    """scipy CSR → FEALPy CSRTensor"""
    return CSRTensor(A_scipy.indptr, A_scipy.indices, A_scipy.data, A_scipy.shape)


def residual(A_fe, x, b):
    """||b - Ax||_2"""
    return float(bm.linalg.norm(b - A_fe @ x))
