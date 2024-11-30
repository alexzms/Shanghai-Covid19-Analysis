import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


P = 24894300    # 总人数
k = 0.0035  # 日死亡率
i = 1 / 7   # 日转阳率
r = 1 / 10  # 日恢复率
a = 1 / P   # 接触率
b = 0.6     # 感染效率
C = a * b * P   # 传染能量C
R = C / r   # 传播系数

T = 200    # 模拟天数

# 生成长度为T的数组
S = np.zeros(T)  # 易感者数量
I = np.zeros(T)  # 感染者数量
E = np.zeros(T)  # 潜伏者数量
R = np.zeros(T)  # 恢复者数量
D = np.zeros(T)  # 死亡者数量

# 初始数值
S[0] = P - 48
I[0] = 48
E[0] = 0
R[0] = 0
D[0] = 0

# 差分方程
for t in range(T - 1):
    # 前10天，大家没有防备
    if t < 10:
        a = 10 / P
        b = 0.4
    # 10-30天，大家戴上了口罩
    elif 10 <= t < 30:
        a = 3.4 / P
        b = 0.2
    # 隔离在家
    else:
        a = 0.02 / P
        b = 0.01
    h = a * b * I[t]
    E[t + 1] = E[t] + h * S[t] - i * E[t]
    I[t + 1] = I[t] + i * E[t] - (r + k) * I[t]
    R[t + 1] = R[t] + r * I[t]
    D[t + 1] = D[t] + k * I[t]
    S[t + 1] = P - I[t + 1] - E[t + 1] - R[t + 1] - D[t + 1]
    print("第%d天:" % (t + 1), end="")
    print("新增感染者:%d" % (i * E[t]), end="\n")

# 绘制图像
# 预测值
# plt.plot(S, label='S')
plt.plot(I, label='Infection', c='#B6d9f2')
plt.plot(E, label='Latent', c='#98bfb6')
plt.plot(R, label='Recover', c='#e2bdbd')
plt.plot(D, label='Death', c='#3f7186')

# 真实情况
data = pd.read_excel('上海数据.xlsx')
posi = np.array(data['累计治愈人数'])
plt.plot(posi, c='#af231c', label='Recover in reality')
plt.title('IERD Figure and Recover in reality')
plt.legend()

plt.savefig('IERD Figure and Recover in reality')
plt.show()

