import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Chinese
plt.rcParams['font.sans-serif'] = ['Heiti TC']

# read the data
data = pd.read_excel('上海数据.xlsx', sheet_name='各区情况')

# 整理分类
district = list(data['区名称'])[0:-1]
posiRate = list(data['人口阳性率'])
density = list(data['人口密度(万人/平方公里)'])
# density = list(data['人均GDP(万元/人)'])


shposi = float(posiRate.pop(-1))
shdesi = float(density.pop(-1))


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


# infection rate with population density
plt.figure(figsize=(30, 24))

# average line
# 上海人口密度
Y = np.linspace(0, max(posiRate), 100)
X = shdesi * np.ones(100, dtype=int)
plt.plot(X, Y, ls='dashdot', linewidth=8, c='#e3b4a0')

# 上海感染率
X = np.linspace(0, max(density), 100)
Y = shposi * np.ones(100, dtype=int)
plt.plot(X, Y, ls='dashdot', linewidth=8, c='#e3b4a0')

# 上海平均值
X = np.linspace(0, max(density), 100)
Y = []
for point in list(shposi*X/shdesi):
    if point <= max(posiRate):
        Y.append(point)
X = list(X)[0:len(Y)]
plt.plot(X, Y, ls='dotted', linewidth=5, c='#e2bdbd')

# scatter
# plt.scatter(density, posiRate, s=2000, color=ColorBar('#bef2e5', '#6e89a2', posiRate))
plt.scatter(density, posiRate, s=2000, color=ColorBar('#e8ffba', '#f38b95', posiRate))

# 标签与标题
font_size = 40  # 设置字号
big_font_size = font_size + 5
small_font_size = font_size - 10
plt.tick_params(labelsize=font_size)
plt.axis(xmin=0, ymin=0)
plt.title('各区阳性感染率与人口密度的关系', fontdict={'size': big_font_size})
# plt.title('各区阳性感染率与人均GDP的关系', fontdict={'size': big_font_size})
plt.xlabel('人口密度：万人/平方公里', fontdict={'size': big_font_size})
# plt.xlabel('人均GDP:万元/人', fontdict={'size': big_font_size})
plt.ylabel('各区感染率', fontdict={'size': big_font_size})

# 标注
for i, rate in enumerate(posiRate):
    if district[i] == '奉贤区' or district[i] == '杨浦区':
        plt.annotate(district[i], xy=(density[i], rate), xytext=(density[i] + 0.05, rate),
                     fontsize=small_font_size)
    else:
        plt.annotate(district[i], xy=(density[i], rate), xytext=(density[i]+0.05, rate-0.0005), fontsize=small_font_size)
    # plt.annotate(district[i], xy=(density[i], rate), xytext=(density[i] + 0.5, rate - 0.0005),
    #              fontsize=small_font_size)
plt.annotate('上海平均人口密度', xy=(shdesi, max(posiRate)), xytext=(shdesi, max(posiRate)), fontsize=font_size)
# plt.annotate('上海人均GDP', xy=(shdesi, max(posiRate)), xytext=(shdesi, max(posiRate)), fontsize=font_size)
plt.annotate('上海总感染率', xy=(max(density), shposi), xytext=(max(density), shposi-0.001), fontsize=font_size)

plt.grid()
plt.savefig('各区阳性感染率与人口密度的关系')

plt.show()
