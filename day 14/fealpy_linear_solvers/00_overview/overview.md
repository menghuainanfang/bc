# FEALPy 线性求解器 —— 学习笔记

> 2026-08-05 | FEALPy v3.4.0 | 模块：`fealpy.solver`

---

## 一、模块概览

`fealpy/solver/__init__.py` 导出的顶层求解接口：

| 类别 | 接口 | 矩阵要求 |
|------|------|----------|
| 稀疏直接法 | `spsolve` | 任意非奇异方阵 |
| 平稳迭代法 | `jacobi` | 对角占优 / SPD |
| | `gauss_seidel` | 对角占优 / SPD |
| Krylov 子空间法 | `cg` | **对称正定 (SPD)** |
| | `minres` | **对称**（可不定） |
| | `gmres` | 一般方阵 |
| | `lgmres` | 一般方阵（增广） |
| | `bicg` | 一般方阵 |
| | `bicgstab` | 一般方阵 |
| 多重网格 | `GAMGSolver` | 大规模稀疏（面向后续学习） |

---

## 二、快速选型指南

```
需要求解 Ax = b
│
├─ 矩阵是 SPD？
│   ├─ 是 → 用 cg（首选）
│   └─ 否 → 矩阵是对称的？ → 用 minres
│           矩阵是非对称的？ → 用 gmres 或 bicgstab
│
├─ 需要基准/参考解？ → 用 spsolve(solver="scipy")
│
└─ 矩阵很大（百万阶）？
    └─ 考虑 GAMGSolver（后续学习）
```

**口诀**：SPD → CG；对称不定 → MINRES；一般 → GMRES/BiCGSTAB；基准 → spsolve。

---

## 三、各求解器详解目录

| 编号 | 求解器 | 文档 | 程序 |
|------|--------|------|------|
| 01 | `spsolve` | [spsolve.md](../01_spsolve/spsolve.md) | [spsolve_demo.py](../01_spsolve/spsolve_demo.py) |
| 02 | `cg` | [cg.md](../02_cg/cg.md) | [cg_demo.py](../02_cg/cg_demo.py) |
| 03 | `minres` | [minres.md](../03_minres/minres.md) | [minres_demo.py](../03_minres/minres_demo.py) |
| 04 | `gmres` | [gmres.md](../04_gmres/gmres.md) | [gmres_demo.py](../04_gmres/gmres_demo.py) |
| 05 | `lgmres` | [lgmres.md](../05_lgmres/lgmres.md) | [lgmres_demo.py](../05_lgmres/lgmres_demo.py) |
| 06 | `bicg` | [bicg.md](../06_bicg/bicg.md) | [bicg_demo.py](../06_bicg/bicg_demo.py) |
| 07 | `bicgstab` | [bicgstab.md](../07_bicgstab/bicgstab.md) | [bicgstab_demo.py](../07_bicgstab/bicgstab_demo.py) |
| 08 | `jacobi` | [jacobi.md](../08_jacobi/jacobi.md) | [jacobi_demo.py](../08_jacobi/jacobi_demo.py) |
| 09 | `gauss_seidel` | [gauss_seidel.md](../09_gauss_seidel/gauss_seidel.md) | [gauss_seidel_demo.py](../09_gauss_seidel/gauss_seidel_demo.py) |
| 10 | 综合对比 | [comparison.md](../10_comparison/comparison.md) | [comparison_demo.py](../10_comparison/comparison_demo.py) |

---

## 四、基本调用形式

### 直接法
```python
from fealpy.solver import spsolve
x = spsolve(A, b, solver="scipy")   # solver: "scipy" | "mumps" | "cupy"
```

### 迭代法（共同参数约定）
```python
# A: COOTensor/CSRTensor,  b: TensorLike
solver(A, b, x0=None, atol=1e-12, rtol=1e-8, maxit=..., M=None)

# CG / Jacobi / Gauss-Seidel: returninfo 控制是否返回 info 字典
x, info = cg(A, b, returninfo=True)          # info = {'residual': ..., 'niter': ...}

# GMRES / MINRES / BiCG / BiCGSTAB / LGMRES: 始终返回 (x, info)
x, info = gmres(A, b)
```

---

## 五、重要提示

1. **矩阵类型**：FEALPy 使用自定义 `COOTensor` / `CSRTensor`，与 scipy 稀疏矩阵不同
2. **张量类型**：右端向量 `b` 需为 `TensorLike`（FEALPy 后端张量）
3. **预条件子**：所有 Krylov 迭代法支持可选 `M` 参数
4. **本周不涉及**：`DirectSolverManager` / `IterativeSolverManager`（统一管理器）、`GAMGSolver` 内部实现、MUMPS 等第三方后端
