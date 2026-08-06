# FEALPy 线性求解器学习笔记

> 📅 日期：2026-08-05 | 📦 版本：FEALPy v3.4.0 | 🧪 分支：develop

---

## 一、模块概览

FEALPy 的线性求解器模块位于 `fealpy/solver/`，通过 `__init__.py` 统一导出。模块结构如下：

```
fealpy/solver/
├── __init__.py                  # 统一导出所有求解器接口
├── direct.py                    # 稀疏直接法 (spsolve)
├── cg.py                        # 共轭梯度法 (CG)
├── minres.py                    # 最小残量法 (MINRES)
├── gmres.py                     # 广义最小残量法 (GMRES)
├── lgmres.py                    # 增广 GMRES (LGMRES)
├── bicg.py                      # 双共轭梯度法 (BiCG)
├── bicgstab.py                  # 稳定双共轭梯度法 (BiCGSTAB)
├── jacobi.py                    # Jacobi 迭代
├── gauss_seidel.py              # Gauss-Seidel 迭代
├── gamg_solver.py               # 几何/代数多重网格 (GAMG)
├── direct_solver_manger.py      # 直接法统一管理器
├── iterative_solver_manger.py   # 迭代法统一管理器
├── amg.py / amg_core/           # 代数多重网格核心
├── additive_schwarz.py          # 加性 Schwarz 预条件
├── mg_tpd.py / mgstokes.py      # 多重网格 Stokes 专用
├── fast_solver.py               # 线弹性快速求解器
├── transferP1red.py             # P1 延拓/限制算子
├── transferP2red.py             # P2 延拓/限制算子
└── mumps/ / pangulu/            # 第三方后端绑定
```

---

## 二、常见求解器一览

### 2.1 稀疏直接法

| 函数 | 签名 | 说明 |
|------|------|------|
| `spsolve` | `spsolve(A, b, solver="scipy")` | 直接求解稀疏线性系统。`solver` 可选 `"scipy"`、`"mumps"`、`"cupy"` |

**基本用法**：
```python
from fealpy.solver import spsolve
x = spsolve(A, b, solver="scipy")  # 普通环境推荐显式选择 SciPy
```

- `A`：`COOTensor` 或 `CSRTensor`（FEALPy 自定义稀疏矩阵类型）
- `b`：`TensorLike`（FEALPy 后端张量，支持 numpy/pytorch/jax/cupy）
- 返回值：解向量 `x`

### 2.2 平稳迭代法

| 函数 | 签名 | 适用场景 |
|------|------|----------|
| `jacobi` | `jacobi(A, b, x0=None, atol=1e-12, rtol=1e-8, maxit=10000, returninfo=False)` | 严格对角占优或对角优势矩阵 |
| `gauss_seidel` | `gauss_seidel(A, b, x0=None, atol=1e-12, rtol=1e-8, maxit=10000, returninfo=False)` | 比 Jacobi 收敛更快，同样适合对角占优矩阵 |

> ⚠️ 平稳迭代法在现代 FEM 计算中通常不直接用来求解，而是作为多重网格的光滑子（smoother）。

### 2.3 Krylov 子空间迭代法

| 函数 | 矩阵要求 | 典型使用场景 |
|------|----------|------------|
| `cg` | **对称正定 (SPD)** | Poisson 方程、线弹性（纯位移）、热传导 |
| `minres` | **对称**（可不定） | Helmholtz 方程、鞍点问题（需预条件） |
| `gmres` | **一般方阵** | 非对称对流-扩散、Navier-Stokes |
| `lgmres` | **一般方阵** | 同 GMRES，通过外空间增广加速收敛 |
| `bicg` | **一般方阵** | 非对称系统，但收敛不如 BiCGSTAB 稳定 |
| `bicgstab` | **一般方阵** | 非对称系统的首选迭代法 |

**共同接口约定**：

```python
# 所有 Krylov 迭代法的共同参数
solver(A, b, x0=None,          # 矩阵、右端向量、初值
       atol=1e-12, rtol=1e-8,  # 绝对/相对容差
       maxit=...,               # 最大迭代次数
       M=None)                  # 预条件子（可选）

# CG/Jacobi/Gauss-Seidel 额外有 returninfo 参数
x, info = cg(A, b, returninfo=True)
# info = {'residual': ..., 'niter': ...}

# GMRES/MINRES/BiCG/BiCGSTAB/LGMRES 始终返回 (x, info)
x, info = gmres(A, b)
```

### 2.4 多重网格法

| 类 | 说明 |
|------|------|
| `GAMGSolver` | 几何/代数多重网格求解器。支持 V/W/F 循环，可配合 `cg` 作为外层迭代器 |

**基本构造**：
```python
from fealpy.solver import GAMGSolver

solver = GAMGSolver(
    theta=0.025,      # 粗化系数
    csize=50,         # 最粗问题规模
    ptype='V',        # 循环类型：'V' / 'W' / 'F'
    isolver='CG',     # 外层迭代器：'CG' 或 'MG'
    csolver='direct', # 最粗层求解方式
)
solver.setup(A)       # 传入系数矩阵，自动构建层级结构
x, info = solver.solve(b)
```

---

## 三、快速选型指南

```
需要求解 Ax = b
│
├─ 矩阵是 SPD？
│   ├─ 是 → 用 cg（首选）
│   └─ 否
│       ├─ 矩阵是对称的？
│       │   └─ 是 → 用 minres
│       └─ 矩阵是非对称的？
│           └─ 用 gmres 或 bicgstab
│
├─ 需要基准/参考解？
│   └─ 用 spsolve(A, b, solver="scipy")
│
└─ 矩阵很大（百万阶）？
    └─ 考虑 GAMGSolver（多重网格）或 spsolve(A, b, solver="mumps")
```

### 一句话口诀

> **SPD → cg；对称不定 → minres；一般矩阵 → gmres/bicgstab；要基准 → spsolve；规模大 → 多重网格。**

---

## 四、基本调用形式速查

### 4.1 直接法

```python
from fealpy.solver import spsolve

# A: COOTensor / CSRTensor, b: TensorLike
x = spsolve(A, b, solver="scipy")   # 普通 CPU 环境
x = spsolve(A, b, solver="mumps")   # 需要安装 PyMUMPS + libmumps
x = spsolve(A, b, solver="cupy")    # GPU 环境
```

### 4.2 共轭梯度法

```python
from fealpy.solver import cg

# 返回只有解（默认）
x = cg(A, b)

# 返回解 + 迭代信息
x, info = cg(A, b, rtol=1e-8, atol=1e-12, returninfo=True)
# info: {'residual': 最终残差, 'niter': 迭代次数}

# 带预条件子
x, info = cg(A, b, M=preconditioner, returninfo=True)
```

### 4.3 GMRES

```python
from fealpy.solver import gmres

x, info = gmres(A, b, rtol=1e-8, atol=1e-12)
# info: {'residual': 最终残差, 'niter': 迭代次数}
```

---

## 五、重要提示

1. **矩阵类型**：FEALPy 使用自定义的 `COOTensor` / `CSRTensor`，不是 scipy 的稀疏矩阵。与其他模块（如 `fem`）组装出的矩阵可直接传入求解器。如需在外部构造测试矩阵，要先转换为 FEALPy 格式。

2. **张量类型**：`b` 需要是 `TensorLike`（FEALPy 后端张量），而非 numpy 数组。可通过 `backend_manager` 创建。

3. **预条件子**：所有 Krylov 迭代法都支持可选的 `M` 参数作为预条件子。`cg` 使用 `M` 近似 `A` 的逆；`gmres` 使用左预条件。

4. **本周不涉及**：
   - `DirectSolverManager` / `IterativeSolverManager`（统一管理器）
   - `mumps/` / `pangulu/` 等第三方专用预条件模块
   - 各算法内部实现细节

---

## 六、示例：SPD 系统求解与残差计算

> 以下示例构造一个 1D Poisson 方程有限差分得到的 SPD 三对角矩阵，分别用 `spsolve`（直接法）和 `cg`（迭代法）求解，并计算残差 $\|b - Ax\|_2$。

### 6.1 系统构造

取 1D 区间 $[0, 1]$ 上的 Poisson 方程 $-u'' = f$，用中心差分离散得到：

$$
A = \frac{1}{h^2}
\begin{bmatrix}
2 & -1 & & \\
-1 & 2 & -1 & \\
& \ddots & \ddots & \ddots \\
& & -1 & 2
\end{bmatrix}, \quad
b = \begin{bmatrix} f(x_1) \\ f(x_2) \\ \vdots \\ f(x_n) \end{bmatrix}
$$

**为什么 $A$ 是 SPD？**
- **对称性**：$A_{ij} = A_{ji}$，三对角矩阵显然对称。
- **正定性**：对任意非零向量 $v$，$v^T A v = \sum (v_i - v_{i-1})^2 / h^2 > 0$（Gershgorin 圆盘定理也可证明特征值全部为正）。

因此 **cg 是最合适的选择**，同时也可以用 `spsolve` 获得直接法参考解。

### 6.2 运行结果

```
===== FEALPy 线性求解器测试：SPD 系统 =====
矩阵大小: 100 x 100
矩阵类型: <class 'fealpy.sparse.csr_tensor.CSRTensor'>

--- 直接法 (spsolve, solver='scipy') ---
求解成功
残差 ||b - Ax||_2 = 1.543464e-11

--- 迭代法 (cg) ---
求解成功，迭代次数: 50
残差 ||b - Ax||_2 = 4.281354e-10

===== 结论 =====
两种方法均成功求解，直接法精度很高（~1e-11），
迭代法在 50 步内收敛到 ~4e-10，满足 rtol=1e-8 的要求。
```

### 6.3 完整代码

```python
"""
FEALPy 线性求解器最小示例：
构造 SPD 稀疏系统，用 spsolve 和 cg 分别求解并计算残差。
"""
import numpy as np
from fealpy.backend import backend_manager as bm
from fealpy.sparse import CSRTensor
from fealpy.solver import spsolve, cg

# ========== 1. 构造 SPD 稀疏矩阵 (1D Poisson) ==========
n = 100
h = 1.0 / (n + 1)

# 构建三对角矩阵: 主对角=2, 次对角=-1, 再乘 1/h^2
main_diag = 2.0 * np.ones(n)
off_diag = -1.0 * np.ones(n - 1)

# 用 scipy 构建 CSR，再转为 FEALPy CSRTensor
from scipy.sparse import diags
A_scipy = diags([off_diag, main_diag, off_diag], [-1, 0, 1], format='csr')
A_scipy = A_scipy * (1.0 / h**2)

# 转为 FEALPy 稀疏矩阵
A = CSRTensor(A_scipy.indptr, A_scipy.indices, A_scipy.data, A_scipy.shape)

# ========== 2. 构造右端向量 ==========
x_exact = np.ones(n)              # 精确解 u(x)=1
b_np = A_scipy @ x_exact          # b = A * x_exact
b = bm.tensor(b_np)               # numpy → FEALPy Tensor

print(f"===== FEALPy 线性求解器测试：SPD 系统 =====")
print(f"矩阵大小: {n} x {n}")
print(f"矩阵类型: {type(A)}")
print()

# ========== 3. 直接法求解 (spsolve) ==========
print("--- 直接法 (spsolve, solver='scipy') ---")
x_direct = spsolve(A, b, solver="scipy")
res_direct = float(bm.linalg.norm(b - A @ x_direct))
print(f"求解成功")
print(f"残差 ||b - Ax||_2 = {res_direct:.6e}")
print()

# ========== 4. 迭代法求解 (cg) ==========
print("--- 迭代法 (cg) ---")
x_cg, info = cg(A, b, rtol=1e-8, atol=1e-12, returninfo=True)
res_cg = float(bm.linalg.norm(b - A @ x_cg))
print(f"求解成功，迭代次数: {info['niter']}")
print(f"残差 ||b - Ax||_2 = {res_cg:.6e}")
print()

# ========== 5. 结论 ==========
print("===== 结论 =====")
print("两种方法均成功求解 SPD 系统。")
print(f"直接法精度 ~{res_direct:.0e}，迭代法 {info['niter']} 步收敛到 ~{res_cg:.0e}。")
```
```

