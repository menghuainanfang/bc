import numpy as np
# ============================================================
# 0. 辅助工具：Levi-Civita 符号（三维）
# ============================================================
def levi_civita(i, j, k):
    """返回三维 Levi-Civita 符号 ε_{ijk} 的值 (+1, -1 或 0)"""
    if {i, j, k} != {0, 1, 2}:  # 有重复指标
        return 0
    # 判断奇偶排列
    if (i, j, k) in [(0,1,2), (1,2,0), (2,0,1)]:
        return 1
    else:
        return -1

# 也可以预先生成一个 3×3×3 的数组，方便后面用
epsilon = np.zeros((3, 3, 3), dtype=int)
for i in range(3):
    for j in range(3):
        for k in range(3):
            epsilon[i, j, k] = levi_civita(i, j, k)

# ============================================================
# 1. 向量基本运算
# ============================================================
def vec_add(a, b):
    """向量加法"""
    return a + b

def vec_scale(lam, a):
    """数乘"""
    return lam * a

def dot_product(a, b):
    """点积 (内积)：对应分量相乘再求和（缩并）"""
    result = 0.0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

def cross_product(a, b):
    """叉积 (向量积)：用 Levi-Civita 符号显式计算"""
    c = np.zeros(3)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # ε_{ijk} * a_j * b_k
                c[i] += levi_civita(i, j, k) * a[j] * b[k]
    return c

def outer_product(a, b):
    """并矢 (张量积 / 外积)：a ⊗ b, 结果是一个 3×3 矩阵"""
    result = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            result[i, j] = a[i] * b[j]
    return result

# ============================================================
# 2. 二阶张量（矩阵）运算
# ============================================================
def tensor_add(A, B):
    """二阶张量加法"""
    return A + B

def tensor_scale(lam, A):
    """二阶张量数乘"""
    return lam * A

def tensor_vec_dot(A, v, right_multiply=True):
    """
    矩阵与向量的点积（缩并一次）：
    - right_multiply=True: A·v （A 右乘向量 v，即默认）
    - right_multiply=False: v·A （向量左乘矩阵）
    返回向量。
    """
    n = A.shape[0]
    result = np.zeros(n)
    if right_multiply:   # A v
        for i in range(n):
            for j in range(n):
                result[i] += A[i, j] * v[j]
    else:                # v^T A
        for j in range(n):
            for i in range(n):
                result[j] += v[i] * A[i, j]
    return result

def tensor_tensor_dot(A, B):
    """
    矩阵乘法（两个二阶张量单点积缩并一次）：A·B
    结果仍是二阶张量。
    """
    n = A.shape[0]
    result = np.zeros((n, n))
    for i in range(n):
        for k in range(n):
            for j in range(n):
                result[i, k] += A[i, j] * B[j, k]
    return result

def double_dot(A, B):
    """
    双点积 A : B：将所有对应元素相乘再全部相加（缩并两次）
    结果是一个标量。
    """
    result = 0.0
    n = A.shape[0]
    for i in range(n):
        for j in range(n):
            result += A[i, j] * B[i, j]
    return result

def tensor_outer(A, B):
    """
    两个二阶张量的张量积（外积）A ⊗ B
    结果是一个四阶张量，形状为 (n, n, n, n)。
    （这里只演示生成方式，不打印具体数值以免太长）
    """
    n = A.shape[0]
    result = np.zeros((n, n, n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    result[i, j, k, l] = A[i, j] * B[k, l]
    return result

# ============================================================
# 3. 用张量积 + Levi-Civita 缩并实现叉乘（验证）
# ============================================================
def cross_via_tensorops(a, b):
    """
    叉乘 = ϵ : (a ⊗ b)
    即先做外积 a ⊗ b 得到二阶张量，再用 Levi-Civita 张量
    与其双点积缩并。
    """
    ab = outer_product(a, b)   # 形状 (3,3)
    c = np.zeros(3)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # ϵ_{ijk} * (a⊗b)_{jk}
                c[i] += epsilon[i, j, k] * ab[j, k]
    return c

# ============================================================
# 4. 演示题1中的 T × ∇（离散近似）
# ============================================================
def discrete_nabla_T(T_spatial, dx=0.01):
    """
    在二维或三维规则网格上对二阶张量场 T 计算其旋度。
    这里仅为了演示原理，我们在一维 x 轴上演算，
    假设 T 只依赖于 x，并且我们只取两个点做中心差分。
    返回在某个点处的 (T × ∇) 矩阵。
    
    实际计算：
    (T × ∇)_{ik} = Σ_{p,q} ε_{kpq} ∂_p T_{iq}
    用中心差分替代偏导数。
    
    注意：输入 T_spatial 应是一个形状为 (3, 3, n) 的数组，
    代表在 n 个空间点上的二阶张量场。
    本函数仅作为一个示意函数，实际调用时可传入具体数据。
    """
    # 这里假设 T 只依赖 x (第一维)，所以 ∂_1 非零，其他 ∂_2=∂_3=0
    # 我们取中间点索引 n//2 的偏导数
    n = T_spatial.shape[2]
    mid = n // 2
    # 中心差分求 dT/dx
    dT_dx = (T_spatial[:, :, mid+1] - T_spatial[:, :, mid-1]) / (2*dx)
    # 现在计算 (T × ∇) 矩阵，p=0 对应 x 分量
    # 公式：result[i, k] = ε_{k0q} ∂_0 T_{i,q} = ε_{k0q} dT_dx[i, q]
    result = np.zeros((3, 3))
    for i in range(3):
        for k in range(3):
            total = 0.0
            for q in range(3):
                total += epsilon[k, 0, q] * dT_dx[i, q]
            result[i, k] = total
    return result

# ============================================================
# 5. 主演示程序（所有运算一目了然）
# ============================================================
if __name__ == "__main__":
    # ---------- 定义示例向量和矩阵 ----------
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, -1.0, 2.0])
    A = np.array([[1, 0, 2],
                  [0, 3, 1],
                  [4, 1, 0]], dtype=float)
    B = np.array([[0, 1, -1],
                  [2, 0, 3],
                  [1, -1, 2]], dtype=float)

    # ---------- 1. 向量运算 ----------
    print("="*50)
    print("向量运算")
    print("="*50)
    print("a =", a)
    print("b =", b)
    print("a + b =", vec_add(a, b))
    print("2.5 * a =", vec_scale(2.5, a))
    print("a · b =", dot_product(a, b))
    print("a × b =", cross_product(a, b))
    print("a ⊗ b (并矢/外积) =\n", outer_product(a, b))

    # ---------- 2. 验证叉乘 = ϵ : (a⊗b) ----------
    print("\n验证：叉乘 = ϵ : (a⊗b) →", cross_via_tensorops(a, b))

    # ---------- 3. 二阶张量运算 ----------
    print("\n" + "="*50)
    print("二阶张量 (矩阵) 运算")
    print("="*50)
    print("A =\n", A)
    print("B =\n", B)
    print("A + B =\n", tensor_add(A, B))
    print("3.2 * A =\n", tensor_scale(3.2, A))

    # 矩阵乘向量
    v = np.array([1, 0, -1], dtype=float)
    print("A · v (右乘) =", tensor_vec_dot(A, v))
    print("v · A (左乘) =", tensor_vec_dot(A, v, right_multiply=False))

    # 矩阵乘法
    print("A · B =\n", tensor_tensor_dot(A, B))

    # 双点积
    print("A : B =", double_dot(A, B))

    # 二阶张量的外积（只展示形状）
    outer4 = tensor_outer(A, B)
    print("A ⊗ B 的形状:", outer4.shape, "(四阶张量，不打印具体数据)")

    # ---------- 4. Levi-Civita 张量展示 ----------
    print("\n" + "="*50)
    print("三维 Levi-Civita 张量 ε (非零切片)")
    print("="*50)
    print("ε[0, :, :] =\n", epsilon[0])   # 展示 i=0 的切片
    print("ε[1, :, :] =\n", epsilon[1])
    print("ε[2, :, :] =\n", epsilon[2])

    # ---------- 5. 演示 T × ∇ (离散，仅示意) ----------
    print("\n" + "="*50)
    print("离散的 T × ∇ 示例（仅 x 方向梯度）")
    print("="*50)
    # 构造一个简单的人工场：T 在三个 x 位置的值
    # 例如：T(x) = x * A 作为线性场
    x_vals = np.array([-1.0, 0.0, 1.0])
    T_field = np.zeros((3, 3, len(x_vals)))
    for idx, x in enumerate(x_vals):
        T_field[:, :, idx] = x * A   # 每个位置上的矩阵与 x 成正比
    T_cross_nabla = discrete_nabla_T(T_field, dx=x_vals[1]-x_vals[0])
    print("在 x=0 处的 (T × ∇) 矩阵:\n", T_cross_nabla)
    print("注意：此结果等同于 A × e_x（因为 dT/dx = A）")