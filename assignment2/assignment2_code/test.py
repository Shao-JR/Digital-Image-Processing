import numpy as np

# 创建两个复数
G = np.array([1 + 2j, 3 + 4j], dtype=np.complex128)
H = np.array([2.0 + 0j, 1.0 + 0j], dtype=np.complex128)  # 实数，但类型是 complex

# 执行复数除法
F_hat = G / H
print(F_hat)
# 输出：[0.5+1.j 3. +4.j] —— 正确！实部虚部分别被2和1除