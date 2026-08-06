# spsolve —— 稀疏直接法

## 数学原理

对稀疏矩阵 A 做 LU 分解：

$$PAQ = LU$$

其中 P、Q 是置换矩阵，L 是下三角，U 是上三角。然后通过三步求解：

1. 前代：$Ly = Pb$
2. 回代：$Uz = y$
3. 置换：$x = Qz$

本质是高斯消去法的稀疏优化实现。对小规模矩阵可得到**机器精度**的解。

## 适用条件

- 任意非奇异方阵
- 不要求对称、正定
- 时间复杂度：对稀疏矩阵远优于稠密 $O(n^3)$，但仍随规模增长

## FEALPy 接口

```python
from fealpy.solver import spsolve

x = spsolve(A, b, solver="scipy")   # 普通 CPU 环境（推荐）
x = spsolve(A, b, solver="mumps")   # 需要 PyMUMPS + libmumps
x = spsolve(A, b, solver="cupy")    # GPU 环境
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `A` | `COOTensor` / `CSRTensor` | 系数矩阵 |
| `b` | `TensorLike` | 右端向量 |
| `solver` | `str` | `"scipy"` / `"mumps"` / `"cupy"` |

**返回值**：解向量 `x`（无 info 字典）

## 数值算例

- **矩阵**：1D Poisson 的 $100 \times 100$ SPD 矩阵
- **精确解**：$u(x) = \sin(\pi x) + 0.5\sin(3\pi x)$
- **预期**：残差 $\approx 10^{-14}$ 量级（机器精度）

详见 [spsolve_demo.py](spsolve_demo.py)
