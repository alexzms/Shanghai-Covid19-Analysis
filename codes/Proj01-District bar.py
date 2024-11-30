import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

# Chinese
plt.rcParams['font.sans-serif'] = ['Heiti TC']

# 默认是按照GDP排序
data = pd.read_excel('上海数据.xlsx', sheet_name='各区情况')
# 按照人口密度排序
# data = data.sort_values(by="人口密度(万人/平方公里)", ascending=False)
# 按照总人数排序
data = data.sort_values(by="常住人口数(万人)", ascending=False)
# 按照面积排序
# data = data.sort_values(by="面积(平方公里)", ascending=True)

district = list(reversed(list(data['区名称'])))
TotalPosi = list(reversed(list(data['累计阳性(人)'])))
posiRate = list(reversed(list(data['人口阳性率'])))


def ColorBar(color0, color1, points: list):
    # 先从16进制转成十进制
    color0 = [int(color0[1:3], 16), int(color0[3:5], 16), int(color0[5:7], 16)]
    color1 = [int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)]

    # 归一化
    deno = max(points)
    mean = np.mean(points)
    normpoints = []
    for num in points:
        if num > mean:
            num = 0.5 + 2 * (num - mean) / deno
        else:
            num = 0.5 * num / mean
        if num > 1:
            normpoints.append(1)
        else:
            normpoints.append(num)

    color = []
    for num in normpoints:
        temcolor = []
        for i in range(3):
            temcolor.append(int(color0[i] + num * (color1[i] - color0[i])))  # 平均计算
        str = '#' + hex(temcolor[0])[2:] + hex(temcolor[1])[2:] + hex(temcolor[2])[2:]  # 转成16进制
        color.append(str)
    return color


# plt.barh(district, TotalPosi, color=ColorBar('#e8ffba', '#f38b95', TotalPosi))
plt.barh(district, posiRate,  color=ColorBar('#bef2e5', '#6e89a2', posiRate))
plt.title('各区人口感染率（按常住人口数排序）')
# 标记数量
for i, num in enumerate(posiRate):
    plt.text(num, i - 0.3, num)
plt.savefig('感染率常住人口数')
plt.show()
