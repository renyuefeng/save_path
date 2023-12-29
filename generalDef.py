import pandas as pd
import re
import numpy as np


# 将文件中所有字符串转换为pattern
def fileToPattern(path):

    with open(path) as d:
        dat = d.readlines()
        lis = []
        for i in dat:
            lis.append(re.sub('\n', '', i))
        b = '|'.join(lis)
    return b


# 修改时间格式为时间戳(小时)
def timeStamp(df):

    df['month'] = df.comment_time.dt.month
    df['month'] = list(map(lambda x: '0' + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['month']))
    df['day'] = df.comment_time.dt.day
    df['day'] = list(map(lambda x: '0' + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['day']))
    df['year'] = df.comment_time.dt.year
    df['hour'] = df.comment_time.dt.hour
    df['hour'] = list(map(lambda x: '0' * (2 - len(str(x).strip('.'))) + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['hour']))
    df['timestamp'] = list(map(lambda a, b, c, d: str(a) + str(b) + str(c) + str(d), df['year'], df['month'], df['day'], df['hour']))
    return df

# 空数据替换为np.nan
def dropSpanData(df, col=[]):

    pattern = re.compile('[\n ]+')
    if col:
        pass
    else:
        col = df.columns
    for i in col:
        df[i + '1'] = df[i]
        df[i + '1'] = list(map(lambda x: pattern.sub('', x) if pd.notna(x) and pattern.search(x)!=None else x, df[i]))
        df[i + '1'] = list(map(lambda x: x if pd.notna(x) or x != '' or x != '' else np.nan, df[i + '1']))
        df[i] = list(map(lambda x, y: x if pd.notna(y) else y, df[i], df[i + '1']))
        df.drop(columns=[i + '1'], axis=1, inplace=True)
    return df


