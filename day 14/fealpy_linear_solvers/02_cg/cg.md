# cg —— 共轭梯度法 (Conjugate Gradient)

## 数学原理

将求解 $Ax=b$ 转化为极小化二次泛函：

$$\phi(x) = \frac{1}{2}x^T A x - b^T x, \quad \nabla\phi(x) = Ax - b = -r$$

在第 k 步，在 Krylov 子空间 $K_k = \text{span}\{b, Ab, A^2b, \ldots, A^{k-1}b\}$ 中极小化 $\phi(x)$。

利用 **A-共轭方向** $\{p_0, p_1, \ldots\}$（即 $p_i^T A p_j = 0, i \neq j$）：

$$\begin{aligned}
\alpha_k &= \frac{r_k^T r_k}{p_k^T A p_k} \\
x_{k+1} &= x_k + \alpha_k p_k \\
r_{k+1} &= r_k - \alpha_k A p_k \\
\beta_k &= \frac{r_{k+1}^T r_{k+1}}{r_k^T r_k} \\
p_{k+1} &= r_{k+1} + \beta_k p_k
\end{aligned}$$

**核心性质**：
- 三步递推，存储 $O(n)$，每步仅一次矩阵-向量乘
- $n$ 步内精确收敛（忽略舍入误差）
- 误差按 $(\sqrt{\kappa}-1)/(\sqrt{\kappa}+1)$ 每步衰减（$\kappa = \lambda_{\max}/\lambda_{\min}$）

## 适用条件

- **A 必须对称正定 (SPD)**
- 非 SPD 矩阵会导致 $\alpha_k$ 分母为零（崩溃）

## FEALPy 接口

```python
from fealpy.solver import cg

# 仅返回解
x = cg(A, b)

# 返回解 + 迭代信息
x, info = cg(A, b, rtol=1e-8, atol=1e-12, maxit=10000, returninfo=True)
# info: {'residual': ..., 'niter': ...}

# 带预条件子
x, info = cg(A, b, M=preconditioner, returninfo=True)
```

## 数值算例

- **矩阵**：1D Poisson 的 $10 \times 10$ SPD 矩阵
- **精确解**：$u(x) = \sin(\pi x) + 0.5\sin(3\pi x)$（含 2 个特征模态）
- **预期**：2 步收敛（恰好需要 2 维 Krylov 子空间）

详见 [cg_demo.py](cg_demo.py)
