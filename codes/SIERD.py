import numpy as np
import matplotlib.pyplot as plt

# 总人数
P = 24894300
# 日死亡率
k = 0.0035
# 日转阳率
i = 1/7
# 日恢复率
r = 1/10
# 接触率
a = 1/P
# 感染效率
b = 0.6
# 传染能量C
C = a * b * P
# 传播系数
R = C / r

# 模拟天数
T = 200

# 生成长度为T的数组
S = np.zeros(T) # 易感者数量
I = np.zeros(T) # 感染者数量
E = np.zeros(T) # 潜伏者数量
R = np.zeros(T) # 恢复者数量
D = np.zeros(T) # 死亡者数量

# 初始数值
S[0] = P - 48
I[0] = 48
E[0] = 0
R[0] = 0
D[0] = 0

# 差分方程
for t in range(T-1):
    # 前10天，大家没有防备
    if (t < 10):
        a = 10/P
        b = 1
    # 10-20天，大家戴上了口罩
    elif t >= 10 and t < 20:
        a = 4/P
        b = 0.4
    # 隔离在家
    else:
        a = 0.02/P
        b = 0.01
    h = a * b * I[t]
    E[t+1] = E[t] + h * S[t] - i * E[t]
    I[t+1] = I[t] + i * E[t] - (r + k) * I[t]
    R[t+1] = R[t] + r * I[t]
    D[t+1] = D[t] + k * I[t]
    S[t+1] = P - I[t+1] - E[t+1] - R[t+1] - D[t+1]
    print("第%d天:" % (t+1), end="")
    print("新增感染者:%d" % (I[t+1] - I[t]), end="\n")

# 绘制图像
# plt.plot(S, label='S')
plt.plot(I, label='I')
plt.plot(E, label='E')
plt.plot(R, label='R')
plt.plot(D, label='D')
plt.legend()
plt.show()
