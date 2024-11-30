from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pandas as pd
import numpy as np

# Chinese
plt.rcParams['font.sans-serif'] = ['Heiti TC']

# 确定上海的经纬度范围
mainmap = Basemap(llcrnrlon=120.8, llcrnrlat=30.6, urcrnrlon=122.2, urcrnrlat=31.9)

# 绘制经纬线
parallels = np.linspace(30.6, 31.8, 4)
mainmap.drawparallels(parallels, labels=[True, False, False, False])
meridians = np.linspace(121, 122, 3)
mainmap.drawmeridians(meridians, labels=[False, False, False, True])

mainmap.readshapefile('上海市/上海市', 'Shanghai', color='#414141')  # 各区边界


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


# Get basic info
data = pd.read_excel('上海数据.xlsx', sheet_name='各区情况')
TotalPosi = list(data['累计阳性(人)'])
posiRate = list(data['人口阳性率'])
totalcolor = ColorBar('#000000', '#ffffff', TotalPosi)
ratecolor = ColorBar('#000000', '#ffffff', posiRate)

colorDict = {}
for i, area in enumerate(list(data['区名称'])):
    colorDict[area] = [totalcolor[i], ratecolor[i]]

ax = plt.gca()

for i, area in enumerate(mainmap.Shanghai_info):
    name = area['name'].strip(b'\x00'.decode())
    ax.add_patch(Polygon(mainmap.Shanghai[i], facecolor=colorDict[name][1]))

plt.title('各区阳性率行政区划可视化')
# plt.savefig('阳性率行政区划')
plt.show()
