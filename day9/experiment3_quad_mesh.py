"""
实验 3: 四边形网格 (QuadrangleMesh) 求解 Poisson 方程

修改要点 vs 原 poisson.py:
  1. TriangleMesh     →  QuadrangleMesh
  2. LagrangeFESpace   →  ParametricLagrangeFESpace  (四边形必须用参数化空间)
  3. method='fast'     →  method=None  (fast 硬编码假设了三角形梯度为常数)
  4. 新增 QuadrangleMesh.from_box() 参数
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import spsolve

# ── 独立的 PDE 定义 (不用 CosCosData，把方程亮出来) ──
from fealpy.decorator import cartesian

@cartesian
def solution(p):
    """真解 u = cos(πx)·cos(πy)"""
    return np.cos(np.pi * p[..., 0]) * np.cos(np.pi * p[..., 1])

@cartesian
def source(p):
    """源项 f = 2π²·cos(πx)·cos(πy)"""
    return 2 * np.pi**2 * np.cos(np.pi * p[..., 0]) * np.cos(np.pi * p[..., 1])

@cartesian
def gradient(p):
    """真解梯度"""
    x, y = p[..., 0], p[..., 1]
    return np.stack([
        -np.pi * np.sin(np.pi * x) * np.cos(np.pi * y),
        -np.pi * np.cos(np.pi * x) * np.sin(np.pi * y),
    ], axis=-1)


# ── 改动 1: QuadrangleMesh 替代 TriangleMesh ──
from fealpy.mesh import QuadrangleMesh

mesh = QuadrangleMesh.from_box([0, 1, 0, 1], nx=10, ny=10)
print(f"四边形网格: {mesh.number_of_nodes()} 节点, {mesh.number_of_cells()} 单元")

# ── 改动 2: ParametricLagrangeFESpace 替代 LagrangeFESpace ──
# 原因: LagrangeFESpace 是为单纯形(三角形/四面体)设计的,
#       四边形需要 ParametricLagrangeFESpace 来定义等参映射
from fealpy.functionspace import ParametricLagrangeFESpace

space = ParametricLagrangeFESpace(mesh, p=1)
uh = space.function()
print(f"自由度: {space.number_of_global_dofs()}")

# ── 改动 3: method 不能是 'fast' ──
# 'fast' 模式利用"线性三角形梯度为常数"来加速, 四边形不满足此条件
from fealpy.fem import (BilinearForm, LinearForm,
                        ScalarDiffusionIntegrator, ScalarSourceIntegrator,
                        DirichletBC)

bform = BilinearForm(space)
bform.add_integrator(ScalarDiffusionIntegrator())   # ← 去掉 method='fast'
A = bform.assembly()

lform = LinearForm(space)
lform.add_integrator(ScalarSourceIntegrator(source))
F = lform.assembly()

A, F = DirichletBC(space, gd=solution).apply(A, F)

uh[:] = spsolve(A.to_scipy(), F)

# ── 误差 ──
l2 = mesh.error(solution, uh)
h1 = mesh.error(gradient, uh.grad_value)
print(f"L2 误差: {l2:.6e}")
print(f"H1 误差: {h1:.6e}")

# ── 画图 ──
# 注意: 四边形的参考坐标是 (ξ,η) 而非三角形重心坐标 (1/3,1/3,1/3)
# 这里改用节点插值方式直接获得每个单元中心的值
node = mesh.entity('node')
cell = mesh.entity('cell')

# 四边形单元中心 (4 个顶点平均)
cell_centers = node[cell].mean(axis=1)

# FE 解在物理节点上的值
uh_nodal = uh[:]  # uh 的底层数组就是节点值

# 单元中心处的 FE 解 (4 个顶点值取平均, 对线性元精确)
uh_cell_vals = uh_nodal[cell].mean(axis=1)

# 精确解在单元中心的值
u_exact = solution(cell_centers)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

mesh.add_plot(axes[0], cellcolor=uh_cell_vals, linewidths=0, colorbar=True)
axes[0].set_title('Quadrilateral FEM Solution')

mesh.add_plot(axes[1], cellcolor=np.abs(uh_cell_vals - u_exact), linewidths=0,
              colorbar=True, cmap='hot')
axes[1].set_title('Pointwise Error')

plt.tight_layout()
plt.savefig('experiment3_quad_result.png', dpi=150)
print("图片已保存至 experiment3_quad_result.png")
plt.show()
