# lgmres —— 增广 GMRES (LGMRES)

## 数学原理

标准 GMRES(m) 重启时会**丢弃所有之前积累的 Krylov 子空间信息**，可能导致收敛停滞。

LGMRES 在重启时保留 `outer_k` 个来自先前周期的**近似误差向量**作为增广子空间：

$$\text{搜索空间} = \underbrace{K_m(A, r_0)}_{\text{Arnoldi 子空间}} \;\oplus\; \underbrace{\text{span}\{z_1, z_2, \ldots, z_{outer\_k}\}}_{\text{增广向量}}$$

其中 $z_j$ 是先前重启周期中解的变化方向（近似误差向量）。这些向量"记住"了之前的进展，缓解了重启带来的信息丢失。

**参数含义**：

| 参数 | 默认值 | 含义 |
|------|--------|------|
| `inner_m` | 20 | 每次重启内的 Arnoldi 步数 |
| `outer_k` | 3 | 保留的外部向量数 |

## 适用条件

- 任意非奇异方阵
- 特别适合 GMRES 重启后收敛慢的问题

## FEALPy 接口

```python
from fealpy.solver import lgmres

x, info = lgmres(A, b, rtol=1e-8, atol=1e-12,
                 inner_m=20, outer_k=3)
# info: {'residual': ..., 'niter': ...}
```

## 数值算例

- **矩阵**：同 GMRES 的非对称对流-扩散矩阵，$20 \times 20$
- **目的**：展示 LGMRES 接口，与 GMRES 对比

详见 [lgmres_demo.py](lgmres_demo.py)
