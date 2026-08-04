# 科学计算常见错误速查手册

> 本手册供 Skill 在分析科学计算报错时参考，覆盖 NumPy、SciPy、FEALPy 等常用库的高频错误模式。

---

## 一、NumPy 数组操作

### 1.1 广播错误 (Broadcasting Error)

**典型报错**：`ValueError: operands could not be broadcast together with shapes (m,) (n,)`

**常见原因**：
- 两个数组 shape 不兼容，且无法按 NumPy 广播规则对齐
- 从 (n,1) 减 (m,) 时维度混乱

**诊断思路**：
1. 打印两个操作数的 `.shape`
2. 检查广播规则：从右往左对齐维度，每个维度要么相等，要么其中一个为 1
3. 检查是否需要显式 reshape 或使用 `np.newaxis`

**常见修复**：
- `a.reshape(-1, 1)` 或 `a[:, np.newaxis]` 增加维度
- `np.squeeze()` 删除大小为 1 的维度
- `b.reshape(a.shape)` 显式对齐

### 1.2 矩阵乘法维度不匹配

**典型报错**：`ValueError: shapes (m,n) and (p,q) not aligned: n (dim 1) != p (dim 0)`

**常见原因**：
- 忘记转置：`A @ B` 时 A 的列数 != B 的行数
- 向量被当作 1D 数组处理，`@` 运算符行为与预期不同

**诊断思路**：
1. 打印 `A.shape` 和 `B.shape`
2. 确认是否需要对 B 转置
3. 考虑使用 `np.dot(A, B)` vs `A @ B` vs `np.matmul(A, B)` 的行为差异

### 1.3 数组当标量用

**典型报错**：`TypeError: only size-1 arrays can be converted to Python scalars`

**常见原因**：
- 对数组调用了 `float()`、`int()` 等标量转换
- 在多值数组上使用 `math.sqrt()` 而非 `np.sqrt()`

**常见修复**：
- 用 `np.sqrt()` 替代 `math.sqrt()`
- 用 `.item()` 提取单个元素
- 用索引 `arr[i]` 取出标量

### 1.4 NaN/Inf 传播

**典型报错**：`RuntimeWarning: invalid value encountered in ...`

**常见原因**：
- 除零：`1/x` 当 `x` 中有 0
- 负数开方：`np.sqrt(negative)`
- 对数取零：`np.log(0)`

**诊断思路**：
1. 在可疑运算前打印 `np.isnan(x).any()` 和 `np.isinf(x).any()`
2. 用 `np.errstate` 上下文管理器提升 warning 为 error 来定位精确位置

---

## 二、线性代数 (NumPy/SciPy linalg)

### 2.1 奇异矩阵

**典型报错**：`numpy.linalg.LinAlgError: Singular matrix`

**常见原因（数值计算领域）**：
- PDE 离散化后未施加足够的 Dirichlet 边界条件，导致刚度矩阵奇异
- 网格中有孤立节点
- 材料参数为零或负值

**诊断思路**：
1. 检查矩阵条件数：`np.linalg.cond(A)`，如果远大于 1e15 则数值奇异
2. 检查行列式：`np.linalg.det(A)` 是否接近 0
3. 对于 FEALPy：检查 `DirichletBC` 是否正确施加，边界自由度是否覆盖足够

**常见修复**：
- 补全边界条件约束
- 使用伪逆：`np.linalg.pinv(A)`（仅用于诊断，不建议作为最终方案）
- 使用最小二乘：`np.linalg.lstsq(A, b)` 处理欠定系统

### 2.2 非正定矩阵

**典型报错**：`numpy.linalg.LinAlgError: Matrix is not positive definite`

**常见原因**：
- Cholesky 分解要求矩阵正定，但刚度矩阵可能因边界条件缺失而半正定
- 材料参数设置错误（如负的弹性模量）

**诊断思路**：
1. 检查特征值：`np.linalg.eigvalsh(A)`，看是否有非正特征值
2. 确认物理参数是否合理

---

## 三、迭代求解器 (SciPy sparse.linalg / FEALPy)

### 3.1 不收敛

**典型报错**：`ConvergenceWarning` 或达到 `max_iter` 仍不收敛

**常见原因**：
- 最大迭代次数 `max_iter` 太小
- 收敛容差 `tol` 太严格
- 初值猜测离解太远
- 系统本身病态（条件数大）
- 缺少合适的预处理器（preconditioner）

**诊断思路**：
1. 打印每步残差：检查是缓慢下降还是震荡/发散
2. 尝试直接求解器（如 `spsolve`）对比，确认系统是否有解
3. 检查矩阵条件数
4. 对 FEALPy：确认网格质量，畸形单元可能导致病态刚度矩阵

**常见修复**：
- 增大 `max_iter`
- 放宽 `tol`
- 使用更好的初值（如先用粗网格求解再插值到细网格）
- 换用预条件共轭梯度法或 GMRES
- 对 FEALPy 场景：使用多重网格预处理器

---

## 四、FEALPy 专项

### 4.1 网格自由度不匹配

**典型报错**：`IndexError: index X is out of bounds` 或 `ValueError` 有关 size

**常见原因**：
- 在一种网格上定义了自由度，但在另一种网格上做插值/投影
- `space.function()` 返回的数组长度与预期不一致

**诊断思路**：
1. 打印 `space.number_of_global_dofs()` 确认自由度总数
2. 检查 `mesh.entity('node')` 的 shape
3. 确认插值/投影操作中源空间和目标空间的对应关系

### 4.2 边界条件未正确施加

**典型表现**：求解结果全零或物理上不合理（不是报错，而是静默错误）

**诊断思路**：
1. 确认 `DirichletBC` 的 `gdof` 参数是否正确
2. 打印被约束的自由度编号，检查是否覆盖了预期的边界节点
3. 可视化边界条件施加前后的解，检查边界处是否满足约束

---

## 五、通用诊断技巧

1. **二分定位法**：注释掉一半代码 → 运行 → 如果还报错，问题在前一半；如果不报错，问题在后一半。反复二分。
2. **最小复现用例**：从完整脚本中逐步删减直到只剩最小报错代码。能复现的最短代码往往就是答案。
3. **打印 shape/dtype**：科学计算 Bug 中 60% 以上与数组形状和类型有关。在每一步可疑操作前加 `print(x.shape, x.dtype)`。
4. **版本检查**：`print(np.__version__)` 确认版本，某些 API 在不同版本间行为有变化。
5. **开启 full traceback**：`np.seterr(all='raise')` 将浮点警告转为异常，在最早出问题的地方就中断。
