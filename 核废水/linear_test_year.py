import re

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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
# data = np.array(df1[8].iloc[:17].to_list())
for i in range(len(df1)):
    data = np.array(df1.iloc[i].to_list())

    print(data)
# print(df1[8].iloc[:17].to_list())
# print(range(len(data)))
    months = np.array(list(range(len(data))))
    print(months)

    # 创建线性回归模型
    model = LinearRegression()

    # 训练模型
    X = months.reshape(-1, 1)  # 将months转换为二维数组
    model.fit(X, data)

    # 输出模型的系数和截距
    print("model: ", model)
    print("Coefficient: ", model.coef_)
    print("Intercept: ", model.intercept_)

    X_test = [[17], [18]]

    pred = model.predict(X_test)

    print(pred)
    # 绘制数据和回归线
    plt.scatter(months, data, color='blue')
    plt.plot(months, model.predict(X), color='red')
    plt.show()
