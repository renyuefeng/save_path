import re
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import VotingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

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

df_train = np.array(df1.iloc[-1].to_list())

df1 = df1.iloc[:-1]

# print(df_train.info())
# print(df1.info())
# print(aaaa)
# print(df1.info())
# df1.to_excel('./test.xlsx', index=False)
# data = np.array(df1[8].iloc[:17].to_list())
model_lis = []
for i in range(len(df1)):
    data = np.array(df1.iloc[i].to_list())
    # print(data)
# print(df1[8].iloc[:17].to_list())
# print(range(len(data)))
    months = np.array(list(range(len(data))))
    # print(months)
    months = months.reshape(-1, 1)  # 将months转换为二维数组
    # 创建一个二次多项式特征实例
    poly_features = PolynomialFeatures(degree=3)

    # 将x转换为多项式特征
    X_poly = poly_features.fit_transform(months)

    # 创建并训练模型
    model = LinearRegression()
    model.fit(X_poly, data)

    # 使用模型进行预测
    predictions = model.predict(X_poly)

    model1 = make_pipeline(poly_features, model)

    model_lis.append(model1)

est = [('model{a}'.format(a=i), model_lis[i]) for i in range(len(model_lis))]
print(est)
voting_reg = VotingRegressor(estimators=[('model{a}'.format(a=i), model_lis[i]) for i in range(len(model_lis))])

months = np.array(list(range(0, 12)))
# print(months)
# predictions = voting_reg.predict(df_train)

# print(len(df_train)-3)
# print(df_train[:-3])
# print(aaa)

voting_reg.fit(months[:-3].reshape(-1, 1), df_train[:-3])
# voting_reg.fit(months[:].reshape(-1, 1), df1[:])

predictions = voting_reg.predict(months.reshape(-1, 1))
print(predictions)
# mse = mean_squared_error(y_test, predictions)
# print("MSE: ", mse)

# 绘制数据点和预测曲线
plt.scatter(months, df_train, color='blue')
plt.plot(months, predictions, color='red')
plt.show()
