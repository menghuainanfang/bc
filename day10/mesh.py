import numpy as np
import matplotlib.pyplot as plt
from fealpy.mesh import TriangleMesh

# 解决 matplotlib 中文显示为方框的问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False  # 避免负号显示异常

mesh = TriangleMesh.from_box([0, 1, 0, 1], nx=3, ny=3)

node = mesh.entity('node')
cell = mesh.entity('cell')

print("= 节点坐标 (node) =")
print(f"形状: {node.shape}  含义: ({mesh.number_of_nodes()} 个节点, 每个有 x,y 坐标)")
print(node)

print("\n= 单元信息 (cell) =")
print(f"形状: {cell.shape}  含义: ({mesh.number_of_cells()} 个三角形, 每个由 3 个节点组成)")
print("前 5 个单元（每行 3 个数字 = 该三角形的 3 个节点编号）:")
print(cell[:5])

print(f"\n节点数 NN = {mesh.number_of_nodes()}")
print(f"单元数 NC = {mesh.number_of_cells()}")
print(f"边数   NE = {mesh.number_of_edges()}")

area = mesh.entity_measure('cell')
print(f"\n前 5 个单元的面积: {area[:5]}")

barycenter = mesh.entity_barycenter('cell')
print(f"前 5 个单元的重心:\n{barycenter[:5]}")

fig = plt.figure(figsize=(10, 4))

ax1 = fig.add_subplot(1, 2, 1)
mesh.add_plot(ax1)
mesh.find_node(ax1, showindex=True)   # 显示节点编号
ax1.set_title("节点编号")

ax2 = fig.add_subplot(1, 2, 2)
mesh.add_plot(ax2)
mesh.find_cell(ax2, showindex=True)   # 显示单元编号
ax2.set_title("单元编号")

plt.tight_layout()
plt.savefig("mesh_exploration.png", dpi=150, bbox_inches='tight')
plt.show()
