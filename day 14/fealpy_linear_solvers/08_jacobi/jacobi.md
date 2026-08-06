# jacobi — Jacobi 迭代法

## 数学原理

将 A 分裂为 $A = D + L + U$（对角 + 严格下三角 + 严格上三角）：

$$x^{(k+1)} = D^{-1}\big(b - (L+U)x^{(k)}\big)$$

**分量形式**（每个分量独立更新）：

$$x_i^{(k+1)} = \frac{1}{a_{ii}}\Big(b_i - \sum_{j \neq i} a_{ij} x_j^{(k)}\Big)$$

### 收敛性

- 迭代矩阵：$G_J = -D^{-1}(L+U)$
- 收敛条件：$\rho(G_J) < 1$（A 严格对角占优 ⇒ 收敛）
- 对 1D Poisson：$\rho(G_J) = \cos(\pi h)$，随 $h \to 0$ 趋于 1 → 收敛极慢

## FEALPy 接口

```python
from fealpy.solver import jacobi

x = jacobi(A, b, rtol=1e-8, atol=1e-12, maxit=10000)
x, info = jacobi(A, b, returninfo=True)
```

> ⚠️ 当前 FEALPy 内置 `jacobi` 的收敛判据使用绝对值比较 (`res < rtol`)，对 FEM 量级矩阵（元素值 ~1/h²）需适当放宽 rtol 或转用相对判据。

## 数值算例

- **矩阵**：1D Poisson，$10 \times 10$ SPD 矩阵
- **观察**：收敛步数随网格加密急剧增长（谱半径 → 1）

详见 [jacobi_demo.py](jacobi_demo.py)
