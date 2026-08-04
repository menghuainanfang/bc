# 示例分析：模拟测试用例

> 以下为 Skill 自测用的模拟样例。正式使用前请替换为真实 Bug 案例。

---

## 测试用例 1：数组广播错误

### 输入

**代码**：
```python
import numpy as np

def compute_residual(u, f, h):
    n = len(u)
    residual = np.zeros(n)
    for i in range(1, n-1):
        residual[i] = f[i] - (u[i+1] - 2*u[i] + u[i-1]) / h**2
    return residual

x = np.linspace(0, 1, 101)
u = np.sin(np.pi * x)
f = np.pi**2 * u

f_2d = f.reshape(1, -1)
result = u + f_2d
print(result)
```

**报错**：
```
Traceback (most recent call last):
  File "script.py", line 18, in <module>
    result = u + f_2d
ValueError: operands could not be broadcast together with shapes (101,) (1,101)
```

### 期望输出

- 定位到第 18 行
- 根因：`u` 是 (101,) 一维数组，`f_2d` 是 (1, 101) 二维数组，广播规则要求从右对齐，(101,) 与 (1,101) 不兼容
- 修复：`f_2d.ravel()` 或 `np.squeeze(f_2d)` 转回一维

---

## 测试用例 2：右端向量维度错误

### 输入

**代码**：
```python
import numpy as np

n = 10
A = np.zeros((n, n))
for i in range(n):
    A[i, i] = 2.0
    if i > 0:
        A[i, i-1] = -1.0
    if i < n-1:
        A[i, i+1] = -1.0

b = np.ones(11)

x = np.linalg.solve(A, b)
print(x)
```

**报错**：
```
Traceback (most recent call last):
  File "script.py", line 14, in <module>
    x = np.linalg.solve(A, b)
  File "<__array_function__ internals>", line 5, in solve
  File ".../numpy/linalg/linalg.py", line 393, in solve
    _assert_stacked_square(a)
  File ".../numpy/linalg/linalg.py", line 203, in _assert_stacked_square
    raise LinAlgError('Last 2 dimensions of the array must be square')
numpy.linalg.LinAlgError: Last 2 dimensions of the array must be square
```

### 期望输出

- 定位到第 14 行 `np.linalg.solve(A, b)`
- 穿透误导性报错：真正问题是 `b = np.ones(11)` 长度不匹配，而非矩阵 A 不是方阵
- 修复：`b = np.ones(n)` 使右端长度与 A 的阶数一致
