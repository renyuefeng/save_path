import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import re
import pandas as pd


# 定义指数函数
def exp_func(x, a, b):
    # print('result:', a * np.exp(b * x))
    return a * np.exp(b * x)

path = './日本-202309.xlsx'
df_dict = pd.read_excel(path, sheet_name=None, header=3)

df1 = pd.DataFrame()

print(df_dict)
pattern = re.compile('^\d+')
for sheet_name, df in df_dict.items():


    dic = {}
    lis = []
    # print(sheet_name)
    # print(df.info())
    for i in df.columns:
        if pattern.search(i):
            dic[i] = int(pattern.search(i).group())
            lis.append(int(pattern.search(i).group()))
    df.rename(columns=dic, inplace=True)
    # df = df[df['Unnamed: 0'].str.contains('中国')]
    df = df[df['Unnamed: 0'].isin(['中国'])]
    # df = df.iloc[7]
    # print(df.head())
    # df = df.loc[['中国']]
    # print(df.info())
    df = df[lis]
    df1 = pd.concat([df, df1])
# print(df1.info())
# df1.to_excel('./test.xlsx', index=False)
data = np.array(df1[7].iloc[:17].to_list())
# data = np.array(df1[9].iloc[:17].to_list())
print(data)
print(df1[8].iloc[:17].to_list())
# print(range(len(data)))
months = np.array(list(range(len(data))))
print(months)

# 使用curve_fit进行指数回归
params, params_covariance = curve_fit(exp_func, months, data)

# 输出估计的参数
print("a = ", params[0])
print("b = ", params[1])

data = np.array(df1[8].iloc[:].to_list())
# data = np.array(df1[9].iloc[:].to_list())
months = np.array(list(range(len(data))))

# 使用模型进行预测
predictions = exp_func(months, params[0], params[1])
print(predictions)

# 绘制数据点和预测曲线
plt.scatter(months, data, color='blue')
plt.plot(months, predictions, color='red')
plt.show()