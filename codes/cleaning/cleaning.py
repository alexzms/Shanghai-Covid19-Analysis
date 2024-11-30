import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('各区情况.csv')
# clean step 1: define the fuction to clean NaN


def nan(x):
    if np.isnan(x):
        return 0
    else:
        return x


# apply the map
df = df.applymap(nan)
# clean step 2: fill the NaN in '管控新增阳性.csv' and '风险新增阳性.csv'
# fill with interpolate
guankong = pd.read_csv('管控新增阳性.csv')
fengxian = pd.read_csv('风险新增阳性.csv')
guankong = guankong.interpolate()
fengxian = fengxian.interpolate()
df.to_csv('各区情况(cleaned).csv', encoding="utf-8")
guankong.to_csv('管控新增阳性(cleaned).csv', encoding="utf-8")
fengxian.to_csv('风险新增阳性(cleaned).csv', encoding="utf-8")
