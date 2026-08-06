# bicgstab —— 稳定双共轭梯度法 (BiCGSTABilized)

## 数学原理

BiCGSTAB 在 BiCG 的基础上引入「**平滑步骤**」，消除 BiCG 的振荡行为：

$$\begin{aligned}
\text{BiCG 步:} \quad \hat{x} &= x_k + \alpha_k p_k \quad (\text{与 BiCG 相同}) \\
\text{平滑步:} \quad r &= \hat{r} - \omega_k A \hat{s} \\
x_{k+1} &= \hat{x} + \omega_k \hat{s}
\end{aligned}$$

其中 $\hat{s}$ 和 $\omega_k$ 的选择**极小化** $\|r\|_2$（类似于 GMRES 对 1 维子空间做最小二乘）。

## 为什么选 BiCGSTAB？

| 对比 | BiCG | GMRES | **BiCGSTAB** |
|------|------|-------|-------------|
| 存储 | $O(n)$ ✓ | $O(mn)$ ✗ | $O(n)$ ✓ |
| 需要 $A^T$ | 需要 ✗ | 不需要 ✓ | 不需要 ✓ |
| 收敛平滑性 | 振荡 ✗ | 单调 ✓ | 平滑 ✓ |
| 适用性 | 一般 | 一般 | 一般 |

> BiCGSTAB 是**实际应用中最流行的非对称系统迭代法之一**。

## 适用条件

- 任意非奇异方阵
- 不要求对称、正定

## FEALPy 接口

```python
from fealpy.solver import bicgstab

x, info = bicgstab(A, b, rtol=1e-8, atol=1e-12)
# info: {'residual': ..., 'niter': ...}
```

## 数值算例

- **矩阵**：非对称对流-扩散，$20 \times 20$
- **对比**：收敛曲线比 BiCG 平滑

详见 [bicgstab_demo.py](bicgstab_demo.py)
