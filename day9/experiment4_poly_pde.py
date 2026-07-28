"""
实验 4: 换一个不同的 PDE 精确解

原代码使用 CosCosData (三角函数解), 这里换成多项式解:
  真解:  u(x,y) = x(1-x)·y(1-y)
  源项:  f = -Δu = 2[x(1-x) + y(1-y)]

为什么 PolynomialData 不存在?
  - fealpy v3.4.0 的 poisson_2d.py 里只有 CosCosData 和 LShapeRSinData
  - 多项式 PDE 需要自己定义 (见下方 PolyData 类)

对比两个 PDE 的特点:
                     CosCosData (原)        PolyData (新)
  ────────────────  ─────────────────────  ─────────────────────
  真解 u             cos(πx)·cos(πy)        x(1-x)·y(1-y)
  边界值             非零 (Robin 型)         全零 (齐次 Dirichlet)
  解的光滑性          C∞                      C∞ (多项式)
  梯度               三角函数                低次多项式
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import spsolve

from fealpy.mesh import TriangleMesh
from fealpy.functionspace import LagrangeFESpace
from fealpy.fem import (BilinearForm, LinearForm,
                        ScalarDiffusionIntegrator, ScalarSourceIntegrator,
                        DirichletBC)
from fealpy.decorator import cartesian


# ═══════════════════════════════════════════════════════════════
# 自己定义的多项式 PDE (替代不存在的 PolynomialData)
# ═══════════════════════════════════════════════════════════════

class PolyData:
    """
    Poisson 方程: -Δu = f

    真解:  u(x,y) = x(1-x)·y(1-y)
    源项:  f = -Δu = -(∂²u/∂x² + ∂²u/∂y²)

    推导:
      u     = (x - x²)·(y - y²)
      ∂u/∂x = (1 - 2x)·y·(1-y)
      ∂²u/∂x² = -2·y·(1-y)
      ∂²u/∂y² = -2·x·(1-x)
      Δu   = -2[y(1-y) + x(1-x)]
      f    = -Δu = 2[x(1-x) + y(1-y)]
    """
    def domain(self):
        return [0, 1, 0, 1]

    @cartesian
    def solution(self, p):
        """真解 u = x(1-x)·y(1-y)"""
        x, y = p[..., 0], p[..., 1]
        return x * (1 - x) * y * (1 - y)

    @cartesian
    def source(self, p):
        """源项 f = 2[x(1-x) + y(1-y)]"""
        x, y = p[..., 0], p[..., 1]
        return 2 * (x * (1 - x) + y * (1 - y))

    @cartesian
    def gradient(self, p):
        """真解梯度 ∇u"""
        x, y = p[..., 0], p[..., 1]
        du_dx = (1 - 2*x) * y * (1 - y)
        du_dy = x * (1 - x) * (1 - 2*y)
        return np.stack([du_dx, du_dy], axis=-1)


# ── 使用新 PDE ──
pde = PolyData()

# ── 网格和求解 (和原 poisson.py 流程相同) ──
mesh = TriangleMesh.from_box(pde.domain(), nx=20, ny=20)
space = LagrangeFESpace(mesh, p=1)
uh = space.function()

bform = BilinearForm(space)
bform.add_integrator(ScalarDiffusionIntegrator(method='fast'))
A = bform.assembly()

lform = LinearForm(space)
lform.add_integrator(ScalarSourceIntegrator(pde.source))
F = lform.assembly()

A, F = DirichletBC(space, gd=pde.solution).apply(A, F)
uh[:] = spsolve(A.to_scipy(), F)

# ── 误差 ──
l2 = mesh.error(pde.solution, uh)
h1 = mesh.error(pde.gradient, uh.grad_value)
print(f"L2 误差: {l2:.6e}")
print(f"H1 误差: {h1:.6e}")

# ── 画图 ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
bc = np.array([[1/3, 1/3, 1/3]], dtype=np.float64)
uh_cell = uh(bc)
u_exact = pde.solution(mesh.bc_to_point(bc))

mesh.add_plot(axes[0], cellcolor=uh_cell, linewidths=0, colorbar=True)
axes[0].set_title('FE Solution (Polynomial PDE)')

mesh.add_plot(axes[1], cellcolor=u_exact, linewidths=0, colorbar=True)
axes[1].set_title('Exact Solution')

plt.tight_layout()
plt.savefig('experiment4_poly_result.png', dpi=150)
plt.show()
