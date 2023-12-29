import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

path = 'D://file//s13数据.xlsx'
# df = pd.read_excel(path)
df = pd.read_excel(path, sheet_name='last')
# df1 = pd.read_excel(path, sheet_name='all')
# df1 = pd.read_excel(path, sheet_name='8')
df1 = pd.read_excel(path, sheet_name='last')
# print(df1.head())
# print(aaaa)
df = df.dropna(how='any')
df = df.reset_index(drop=False)

# print(df.info())
# print(df['推塔'].head(10))
lis = list(df.columns)[5:]
# lis_all = list(df.columns)[:]
lis1 = list(df.columns)[4:]
# print(lis)
print('对比特征：', lis1)

# df3 = pd.DataFrame(columns=df.columns)
df3 = df.loc[df['战队名'] == 'JDG']
# df3 = df1.loc[df1['战队名'] == 'WBG']
# df3 = df1.loc[df1['战队名'] == 'JDG']
df4 = df1.loc[df1['战队名'] == 'T1']
# df4 = df1.loc[df1['战队名'] == 'T1']
df5 = df.loc[df['战队名'] == 'BLG']
# df5 = df1.loc[df1['战队名'] == 'BLG']
# df6 = df.loc[df['战队名'] == 'T1']
df6 = df1.loc[df1['战队名'] == 'WBG']

# print('JDG:')
# print(df3[lis1].mean())
# print('T1:')
# print(df4[lis1].mean())
# print('T1:')
# print(df5[lis1].mean())
# print('WBG:')
# print(df6[lis1].mean())

# for j in lis1:
df3 = pd.DataFrame([df3[lis1].mean(), df4[lis1].mean(), df5[lis1].mean(), df6[lis1].mean()])
# df3 = pd.DataFrame([df3[lis1].mean(), df4[lis1].mean()])
df3 = df3.reset_index(drop=False)

# print(df3.head())
# print(aaaa)

# for i in lis:
#     df[i] = list(map(lambda x, y: y/x, df['时长'], df[i]))
#     df3[i] = list(map(lambda x, y: y/x, df['时长'], df3[i]))

# print(df.head())
# print(df3.head())
# print(aaaa)

for i in lis:
    df[i] = list(map(lambda x, y: y/x, df['时长'], df[i]))
    df3[i] = list(map(lambda x, y: y/x, df['时长'], df3[i]))
    df[i] = list(map(lambda a, b, c, d: b-c if a % 2 == 0 else b-d, df['index'], df[i], df[i].shift(-1), df[i].shift(1)))
    df3[i] = list(map(lambda a, b, c, d: b-c if a % 2 == 0 else b-d, df3['index'], df3[i], df3[i].shift(-1), df3[i].shift(1)))

# df3.to_excel('./test.xlsx')
# print(df3[lis1].values)
# print(df.corr())

# print(df3.head())
# print(type(df3))
# print(aaaa)
# JDG =

# print(df.head())
# print(df[lis].values)

train_data = df[lis1].values
# train_data = df[lis].values
result_data = df[['胜负']].values

test_data = df3[lis1].values
# test_data = df3[lis].values
# print(test_data)
# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(train_data, result_data, test_size=0.2, random_state=42)

# print(X_test)

# 创建逻辑回归模型
clf1 = LogisticRegression(random_state=42)
# clf = LogisticRegression()
# # 创建决策树模型
clf2 = DecisionTreeClassifier(random_state=42)
# # 创建随机森林模型
clf3 = RandomForestClassifier(random_state=42)
# # 创建梯度提升机模型
clf4 = GradientBoostingClassifier(random_state=42)

# 训练模型
clf1.fit(train_data, result_data)
clf2.fit(train_data, result_data)
clf3.fit(train_data, result_data)
clf4.fit(train_data, result_data)

# 预测测试集
y_pred1 = clf1.predict(test_data)
y_pred2 = clf2.predict(test_data)
y_pred3 = clf3.predict(test_data)
y_pred4 = clf4.predict(test_data)
# y_pred = clf.predict(train_data)

# accuracy = accuracy_score(result_data, y_pred)
# print(f"Accuracy: {accuracy*100:.2f}%")

# y_pred = clf.predict_proba(test_data)
print('逻辑回归预测结果', y_pred1)
print('决策树预测结果', y_pred2)
print('随机森林预测结果', y_pred3)
print('梯度提升机预测结果', y_pred4)

# # 计算预测准确率
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy*100:.2f}%")
#
# # 输出每个特征的系数
# print(f"Coefficients: {clf.coef_}")
#
# print(df.head())
# print(df.info())

# df1 = df.iloc[::2]
# df2 = df.iloc[1::2]

# print(df1.head())
# print(df2.head())
# print(df1.info())
# print(df2.info())

# df3 = pd.DataFrame(columns=df.columns)
# print(df3.info())


#
# print(lis)
# print(type(lis))

# for i in df.columns:
#     if i in lis:
#         df3[[i]] = df1[[i]].sub(df2[[i]], axis=0)
#     # else:
#         # df3[i] = df1[i]
#
# print(df3.head())
