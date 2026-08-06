# gauss_seidel — Gauss-Seidel 迭代法

## 数学原理

将 A 分裂为 $A = (D+L) + U$，**用最新值更新**：

$$x^{(k+1)} = (D+L)^{-1}\big(b - U x^{(k)}\big)$$

**分量形式**（注意 $x_j^{(k+1)}$ 用于 $j<i$ 的求和）：

$$x_i^{(k+1)} = \frac{1}{a_{ii}}\Big(b_i - \sum_{j<i} a_{ij} {\color{red}x_j^{(k+1)}} - \sum_{j>i} a_{ij} x_j^{(k)}\Big)$$

## GS vs Jacobi

| | Jacobi | Gauss-Seidel |
|------|--------|-------------|
| 更新方式 | 全用旧值 $x^{(k)}$ | 立即使用最新值 |
| 矩阵分裂 | $D + (L+U)$ | $(D+L) + U$ |
| 收敛速度 | $\rho_J$ | $\rho_{GS} \approx \rho_J^2$（约快一倍） |
| 并行可行性 | ✓ 天然可并行 | ✗ 顺序依赖 |

对 1D Poisson：$\rho_{GS} = \cos^2(\pi h)$，恰好是 Jacobi 谱半径的平方。

## FEALPy 接口

```python
from fealpy.solver import gauss_seidel

x = gauss_seidel(A, b, rtol=1e-8, atol=1e-12, maxit=10000)
x, info = gauss_seidel(A, b, returninfo=True)
```

> ⚠️ 当前 FEALPy 的 `gauss_seidel` 依赖 MUMPS（`spsolve_triangular`）。若环境未安装 PyMUMPS + libmumps-dev，导入会失败。数学接口与 Jacobi 完全一致。

## 数值算例

- **矩阵**：1D Poisson，$10 \times 10$ SPD
- **对比 Jacobi**：收敛步数约为 Jacobi 的一半

详见 [gauss_seidel_demo.py](gauss_seidel_demo.py)
