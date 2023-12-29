import sql_test
import pandas as pd
import re
import numpy as np
import math

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
port = 63306
database = 'dwd_weibo'

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dwd_weibo_publisher')
pattern = re.compile('北京|上海|天津|重庆')
pattern1 = re.compile('^\w+(?= )')
df['area'] = list(map(lambda x: '其他' if pd.isna(x) else(pattern.search(x).group() if pd.notna(x) and pattern.search(x)!=None
                                                        else(pattern1.search(x).group() if pd.notna(x) and pattern1.search(x)!=None else x)), df['area']))
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_weibo_publisher_copy', data=df, if_exists='truncate')

database = 'dwd_xiaohongshu_03'
a = sql_test.dbconnect(host, username, password, database, port)
pattern2 = re.compile('^中国\W+')
df1 = a.read_database(table_name='dwd_xiaohongshu_publisher')
df1['location'] = list(map(lambda x: pattern2.sub('', x) if pd.notna(x) and pattern2.search(x)!=None else x, df1['location']))
df1['location'] = list(map(lambda x: '其他' if pd.isna(x) or x == '中国' or x == '地球的某一片红薯地' else(pattern.search(x).group() if pattern.search(x)!=None else(pattern1.search(x).group() if pattern1.search(x)!=None else x)), df1['location']))
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_xiaohongshu_publisher_copy', data=df1, if_exists='truncate')

database = 'dwd_hupu_03'
a = sql_test.dbconnect(host, username, password, database, port)
pattern_p = re.compile('\w+(?=省)')
pattern_c = re.compile('\w+(?=市)')
df2 = a.read_database(table_name='dwd_hupu_publisher')
df_c = pd.read_excel('./地区划分省市.xlsx')
df2['priv'] = list(map(lambda x: pattern_p.search(x).group() if pd.notna(x) and pattern_p.search(x)!=None else np.nan, df2['address']))
df2['city'] = list(map(lambda x, y: np.nan if pd.notna(y) else(pattern_c.search(x).group() if pd.notna(x) and pattern_c.search(x)!=None else x), df2['address'], df2['priv']))
df2 = pd.merge(df2, df_c, left_on='city', right_on='城市', how='left')
print(df2.info())
df2['address'] = list(map(lambda x, y, z: x if pd.notna(x) else(y if pd.notna(y) else z), df2['priv'], df2['省'], df2['address']))
df2.drop(columns=['城市', '省', 'priv', 'city'], axis=1, inplace=True)
# database = 'dwd_hupu_03'
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_hupu_publisher_copy', data=df2, if_exists='truncate')

# df2['address'] = list(map(lambda x: pattern2.sub('', x) if pd.notna(x) and pattern2.search(x)!=None else x, df2['address']))



