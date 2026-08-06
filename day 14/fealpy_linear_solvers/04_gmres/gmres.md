# gmres —— 广义最小残量法 (Generalized Minimal RESidual)

## 数学原理

GMRES 同 MINRES 一样极小化 $\|b-Ax\|_2$，但**不要求 A 对称**。

用 **Arnoldi 过程**（而非 Lanczos）生成 Krylov 子空间的正交基：

$$A Q_k = Q_{k+1} \bar{H}_k$$

其中 $\bar{H}_k$ 是 $(k+1) \times k$ **上 Hessenberg 矩阵**（不再是对称三对角）。

子问题：
$$\min_y \|\;\|r_0\|e_1 - \bar{H}_k y\;\|_2$$

用 Givens 旋转求解。

### 重启机制

Arnoldi 过程需要存储所有 $Q_k$ 列（$O(kn)$ 内存），k 大时不堪重负。

**GMRES(m)**：每隔 m 步重启一次，丢弃旧基重新开始。
- 默认 `restart=20`
- 重启过小 → 可能停滞 (stagnation)
- 重启过大 → 内存开销大

## 适用条件

- 任意非奇异方阵
- **不要求**对称、正定

## FEALPy 接口

```python
from fealpy.solver import gmres

x, info = gmres(A, b, rtol=1e-8, atol=1e-12, restart=20)
# info: {'residual': ..., 'niter': ...}
```

| 参数 | 说明 |
|------|------|
| `restart` | 重启间隔（默认 20），`None` = 不重启 |
| `maxit` | 最大迭代次数（默认 5×n） |
| `M` | 预条件子（左预条件） |

## 数值算例

- **矩阵**：1D 对流-扩散，$\varepsilon=0.1, v=1.0$，$20 \times 20$，非对称
- **精确解**：$u(x) = \sin(\pi x) + 0.5\sin(3\pi x)$

详见 [gmres_demo.py](gmres_demo.py)
