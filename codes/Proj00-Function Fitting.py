import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = pd.read_excel('上海数据.xlsx')
# read the data in every column
diag = np.array(data['新增确诊'])
asym = np.array(data['新增无症状'])
posi = np.array(data['新增阳性'])
# get the date list
date = pd.date_range('2022-03-06', '2022-05-31').strftime("%m-%d")
xlist = np.arange(1, len(date) + 1)


# 折线图
def LineChart():
    plt.figure(figsize=(20, 6))  # 设置图片长宽
    plt.plot(date, diag, c='#2f4342', label='The new diagnosis')  # 深绿色表示确诊
    plt.plot(date, asym, c='#acbcb2', label='New asymptomatic')  # 浅绿色表示无症状
    plt.plot(date, posi, c='#d19c79', label='New positive')  # 陶黄色表示阳性
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))  # 隐藏部分xlabel避免过于密集
    plt.title('The line chart of COVID-19 daily increased in Shanghai, 2022.3.6-2022.5.31')
    plt.legend()
    plt.savefig('折线图')
    plt.show()


# Curve Fit by Least Square Method and Ridge Regression
def CurveFit(xlist, ylist, k: int, alpha: float = 0):
    Yarray = np.transpose(np.array(ylist))

    # 计算nxarray
    nXlist = []
    for x in xlist:
        temlist = []
        for i in range(k + 1):
            temlist.append(x ** i)
        nXlist.append(temlist)
    nXarray = np.array(nXlist)

    # 算出thetaalpha
    X = nXarray
    Y = Yarray
    I = np.identity(k + 1)
    M = np.linalg.inv(np.dot(np.transpose(X), X) + alpha * I)
    thetaalpha = np.dot(np.dot(M, np.transpose(X)), Y)

    # 按照格式输出
    pointLst = []
    for i in range(len(xlist)):
        temlist = [xlist[i], ylist[i]]
        pointLst.append(temlist)

    # draw the fitting curve
    x = np.linspace(min(xlist), max(xlist), 100)
    y = 0
    for m, coefficients in enumerate(thetaalpha):
        y += coefficients * x ** m
    plt.plot(x, y, color='#ebc9c7', linewidth=1.5, label='CurveFit')
    # set the range of x,y axes
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(100))
    # set the title of figure
    plt.title('Curve Fit by Least Square Method of the diagnosis, ' + 'k=%d' % k + ', alpha=%a' % alpha)

    return thetaalpha


# plt.scatter(date, diag, c='#97a7be', marker='.', label='The new diagnosis')   # 散点图
# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))  # 隐藏部分xlabel避免过于密集
# plt.savefig('diag拟合')   # 保存图片
# plt.legend()    # 显示label
# plt.show()
print(xlist)
