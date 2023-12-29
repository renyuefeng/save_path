import sql_test
import pandas as pd
import re
import numpy as np
import math
host = '139.224.197.121'
username = 'db_e_commerce'
password = r'Zj690!#'
database = 'db_e_commerce_data_analysis'
port = 63306

a = sql_test.dbconnect(host, username, password, database, port)
df2 = a.read_database(table_name='db_e_commerce_data_chuimei', list_field=['brand', 'platform', 'url_link', 'title', 'content', 'pub_time', 'publisher', 'comment_count'])
df2.rename(columns={'brand': 'keyword'}, inplace=True)
# df2['platform'] = '垂媒'
a = sql_test.dbconnect(host, username, password, database, port)
df3 = a.read_database(table_name='db_e_commerce_data', list_field=['keyword', 'Product_SKU', 'Store_name', 'model'])
df3['platform'] = '电商'
df3.rename(columns={'Store_name': 'publisher', 'Product_SKU': 'title'}, inplace=True)
df3['url_link'] = df3['title']
# print(df3.info())
df4 = df3.groupby(by=['title', 'publisher'])['model'].count().reset_index()
df4.rename(columns={'model': 'comment_count'}, inplace=True)
# print(df4.info())
df3 = pd.merge(df3, df4, on=['title', 'publisher'], how='outer')
# print(df3.info())

# print(aaa)
host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dim_summery', list_field=['keyword', 'url_link', 'title', 'content', 'pub_time', 'platform', 'tag', 'publisher', 'comment_count'])
# df['platform'] = '3q'
a = sql_test.dbconnect(host, username, password, database, port)
df1 = a.read_database(table_name='dim_海量3期', list_field=['keyword', 'url_link', 'title', 'content', 'pub_time', 'platform', 'tag', 'publisher', 'comment_count'])
# df1['platform'] = '海量'

df = pd.concat([df, df1, df2, df3])
print(df.info())
df.drop_duplicates(subset=['url_link', 'title'], keep='first', inplace=True)
pattern = re.compile('0w{0,1}.{0,1}16', re.IGNORECASE)
# df['flag'] = list(map(lambda x, y, z: 1, df['title'], df['content'], df['tag']))

df['tag'] = list(map(lambda x: x if pd.notna(x) else '', df['tag']))
df['title'] = list(map(lambda x: x if pd.notna(x) else '', df['title']))
df['content'] = list(map(lambda x: x if pd.notna(x) else '', df['content']))

patternTab = re.compile(' ')
df['flag'] = list(
    map(lambda x, y, z: 1 if pd.notna(str(x) + str(y) + str(z)) and pattern.search(
        patternTab.sub('', str(x) + str(y) + str(z))) != None else np.nan, df['content'],
        df['tag'], df['title']))

df['tag'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['tag']))
df['title'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['title']))
df['content'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['content']))

# print(df.info())
df = df.loc[df['flag'] == 1]

# print(df.info())
pattern2 = re.compile('美孚|嘉实多|壳牌|长城|龙蟠|昆仑|统一|道达尔|Castrol|Mobil|shell', re.IGNORECASE)
df['keyword1'] = list(map(lambda x, y, z: ','.join(list(set(pattern2.findall(str(x) + str(y) + str(z))))) if pd.notna(str(x) + str(y) + str(z)) and pattern.search(str(x) + str(y) + str(z)) != None else np.nan
                         , df['content'], df['tag'], df['title']))
patternm = re.compile('Mobil', re.IGNORECASE)
patternj = re.compile('Castrol', re.IGNORECASE)
patternq = re.compile('shell', re.IGNORECASE)

df['keyword1'] = list(map(lambda x: patternm.sub('美孚', x) if pd.notna(x) and patternm.search(x)!=None else x, df['keyword1']))
df['keyword1'] = list(map(lambda x: patternj.sub('嘉实多', x) if pd.notna(x) and patternj.search(x)!=None else x, df['keyword1']))
df['keyword1'] = list(map(lambda x: patternq.sub('壳牌', x) if pd.notna(x) and patternq.search(x)!=None else x, df['keyword1']))

df['keyword'] = list(map(lambda x, y: x if pd.notna(x) else y, df['keyword1'], df['keyword']))

df.drop(['flag', 'keyword1'], axis=1, inplace=True)

df = df.drop(['keyword'], axis=1).join(df['keyword'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('keyword'))
df = df.drop_duplicates()

a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dim_meifu_0w16_bak_1206', data=df, if_exists='truncate')
