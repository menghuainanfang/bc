# minres —— 最小残量法 (MINimum RESidual)

## 数学原理

MINRES 在 Krylov 子空间上**直接极小化残差 2-范数**：

$$x_k = \arg\min_{x \in K_k(A, r_0)} \|b - Ax\|_2$$

利用 **Lanczos 过程**（A 对称，只需三步递推）生成标准正交基 $Q_k$，使得：

$$A Q_k = Q_{k+1} \bar{T}_k$$

其中 $\bar{T}_k$ 是对称三对角矩阵。子问题化为：

$$\min_y \|\;\|r_0\|e_1 - \bar{T}_k y\;\|_2$$

用 Givens 旋转对 $\bar{T}_k$ 做 QR 分解即可求解。

## 与 CG 的区别

| | CG | MINRES |
|------|----|--------|
| 极小化目标 | $\phi(x) = \frac{1}{2}x^T A x - b^T x$ | $\|b - Ax\|_2$ |
| 矩阵要求 | **对称正定 (SPD)** | **对称**（可不定） |
| 负特征值 | 崩溃（$\alpha_k$ 分母为零） | 正常工作 |
| 递推长度 | 三步 | 三步（都短） |

## 适用条件

- **A 必须对称**（$A = A^T$）
- 可以是不定矩阵（同时有正负特征值）
- 典型场景：Helmholtz 方程、鞍点问题

## FEALPy 接口

```python
from fealpy.solver import minres

x, info = minres(A, b, rtol=1e-8, atol=1e-12)
# info: {'residual': ..., 'niter': ..., 'relative tolerance': ...}
```

| 参数 | 说明 |
|------|------|
| `A` | 对称矩阵（任意正定性） |
| `M` | 预条件子（也须对称） |

FEALPy 实现中包含对称性检查：若 $|r^T(Aw) - w^T(Ar)|$ 过大则抛出 `ValueError("A must be symmetric matrix")`。

## 数值算例

- **矩阵**：1D Helmholtz，$k=5$，$20 \times 20$，含 19 正 + 1 负特征值
- **精确解**：$u(x) = \sin(\pi x) + 0.5\sin(3\pi x)$
- **对比**：CG 在此矩阵上会崩溃

详见 [minres_demo.py](minres_demo.py)
