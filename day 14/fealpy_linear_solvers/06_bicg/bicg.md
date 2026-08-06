# bicg —— 双共轭梯度法 (BiConjugate Gradient)

## 数学原理

BiCG 同时维护**原始系统** $Ax=b$ 和**对偶系统** $A^T x^* = b^*$ 两组迭代。

使用 **双正交 Lanczos 过程**，在两个 Krylov 子空间上构造双正交基：

$$K(A, r_0) \quad \text{和} \quad K(A^T, \tilde{r}_0)$$

满足 $p_i^T A p_j = 0 \;(i \neq j)$（A-双正交）。

类似于 CG 的**短递推**，不需要像 GMRES 那样存储所有基向量。代价是每步需要一次 $A$ 乘和一次 $A^T$ 乘。

## 优缺点

| 优点 | 缺点 |
|------|------|
| 短递推（固定存储） | 收敛可能振荡 (irregular convergence) |
| 不需要像 GMRES 那样存储历史 | 可能发生 breakdown |
| 适用于一般非对称矩阵 | 需要 $A^T$ 乘法 |

> 实践中通常推荐 **BiCGSTAB** 替代，收敛更平滑且不需要 $A^T$。

## FEALPy 接口

```python
from fealpy.solver import bicg

x, info = bicg(A, b, rtol=1e-8, atol=1e-12)
# info: {'residual': ..., 'niter': ...}
```

## 数值算例

- **矩阵**：非对称对流-扩散，$20 \times 20$
- **精确解**：$u(x) = \sin(\pi x) + 0.5\sin(3\pi x)$

详见 [bicg_demo.py](bicg_demo.py)
