"""
Poisson 方程有限元求解 —— FEALPy v3.4.0 标准示例
方程: -Δu = f  on Ω=[0,1]×[0,1]
真解: u = cos(πx)·cos(πy)
Dirichlet 边界条件: u = cos(πx)·cos(πy) on ∂Ω
"""
import numpy as np
import os
from scipy.sparse.linalg import spsolve
import matplotlib
matplotlib.use('Agg')              # 非交互式后端，不弹窗
import matplotlib.pyplot as plt

from fealpy.mesh import TriangleMesh
from fealpy.functionspace import LagrangeFESpace
from fealpy.fem import (
    BilinearForm, LinearForm,
    ScalarDiffusionIntegrator, ScalarSourceIntegrator,
    DirichletBC
)
from fealpy.backend import backend_manager as bm
from fealpy.decorator import cartesian

# ──────────────────────────────────────────────
# 1. 定义 PDE 问题
# ──────────────────────────────────────────────
class Poisson2D:
    """-Δu = f in Ω=[0,1]², 真解 u = cos(πx)·cos(πy)"""
    @staticmethod
    def domain():
        return [0, 1, 0, 1]                # [xmin, xmax, ymin, ymax]

    @cartesian
    def solution(self, p):
        x, y = p[..., 0], p[..., 1]
        return bm.cos(bm.pi * x) * bm.cos(bm.pi * y)

    @cartesian
    def source(self, p):
        x, y = p[..., 0], p[..., 1]
        return 2 * bm.pi**2 * bm.cos(bm.pi * x) * bm.cos(bm.pi * y)

    @cartesian
    def gradient(self, p):
        x, y = p[..., 0], p[..., 1]
        return bm.stack((
            -bm.pi * bm.sin(bm.pi * x) * bm.cos(bm.pi * y),
            -bm.pi * bm.cos(bm.pi * x) * bm.sin(bm.pi * y)
        ), axis=-1)

pde = Poisson2D()

# ──────────────────────────────────────────────
# 2. 创建三角形网格
# ──────────────────────────────────────────────
nx, ny = 20, 20
mesh = TriangleMesh.from_box(pde.domain(), nx=nx, ny=ny)
NN = mesh.number_of_nodes()
NC = mesh.number_of_cells()
print(f"网格: {NN} 节点, {NC} 单元")

# ──────────────────────────────────────────────
# 3. 创建线性 Lagrange 有限元空间 (p=1)
# ──────────────────────────────────────────────
space = LagrangeFESpace(mesh, p=1)
gdof = space.number_of_global_dofs()
print(f"自由度: {gdof}")

# ──────────────────────────────────────────────
# 4. 组装刚度矩阵: ∫ ∇u·∇v dx
# ──────────────────────────────────────────────
bform = BilinearForm(space)
bform.add_integrator(ScalarDiffusionIntegrator(method='fast'))
A = bform.assembly()

# ──────────────────────────────────────────────
# 5. 组装载荷向量: ∫ f·v dx
# ──────────────────────────────────────────────
lform = LinearForm(space)
lform.add_integrator(ScalarSourceIntegrator(pde.source))
F = lform.assembly()

# ──────────────────────────────────────────────
# 6. 施加 Dirichlet 边界条件
# ──────────────────────────────────────────────
A, F = DirichletBC(space, gd=pde.solution).apply(A, F)

# ──────────────────────────────────────────────
# 7. 求解 Au = F
# ──────────────────────────────────────────────
uh = space.function()
uh[:] = spsolve(A.to_scipy(), bm.to_numpy(F))

# ──────────────────────────────────────────────
# 8. 误差计算
# ──────────────────────────────────────────────
l2_error = mesh.error(pde.solution, uh)        # L² 误差
print(f"\nL2 误差: {l2_error:.6e}")

# ──────────────────────────────────────────────
# 9. 可视化
# ──────────────────────────────────────────────
node = bm.to_numpy(mesh.entity('node'))
cell = bm.to_numpy(mesh.entity('cell'))
uh_vals = bm.to_numpy(uh)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图: 数值解颜色图
im = axes[0].tripcolor(node[:, 0], node[:, 1], cell, uh_vals,
                       cmap='rainbow', shading='gouraud')
axes[0].set_title('FE Solution $u_h$ (p=1)')
axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
axes[0].set_aspect('equal')
plt.colorbar(im, ax=axes[0])

# 右图: y=0.5 截面对比
mid_y = 0.5
x_line = np.linspace(0, 1, 201)
p_line = bm.tensor(np.c_[x_line, np.full_like(x_line, mid_y)])
u_exact = bm.to_numpy(pde.solution(p_line))
from scipy.interpolate import LinearNDInterpolator
interp = LinearNDInterpolator(node, uh_vals)
u_fem = interp(x_line, np.full_like(x_line, mid_y))

axes[1].plot(x_line, u_exact, 'b-', lw=2, label='Exact')
axes[1].plot(x_line, u_fem, 'ro--', ms=3, label='FE (interp)')
axes[1].set_title(f'Cross-section at y={mid_y}\nL2 error = {l2_error:.2e}')
axes[1].set_xlabel('x'); axes[1].set_ylabel('u')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poisson_result.png')
plt.tight_layout()
plt.savefig(out_path, dpi=150)
plt.close()
print(f"图片已保存至 {out_path}")
