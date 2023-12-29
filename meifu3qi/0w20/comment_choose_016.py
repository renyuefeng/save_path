import sql_test
import pandas as pd
import re
import numpy as np
import math
from defSet import dataCleanDef
from snownlp import SnowNLP

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
port = 63306

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dim_meifu_0w16_bak_1206')
df1 = df.loc[df['url_link'].notnull()]
url_list = df1['url_link'].values.tolist()
df2 = df.loc[df['url_link'].isnull()]
ch_list = df2['url_link'].values.tolist()
url_list = ['\"' + str(i) + '\"' for i in url_list]
ch_list = ['\"' + str(i) + '\"' for i in ch_list]
# print(url_list)
# print(ch_list)
sql = 'select url_link, replier, comment_content, comment_time, sentiment_analysis, sentiment_flag, purchase_intention  from dim_summery_comment where url_link in ({})'.format(','.join(url_list))
# sql1 = 'select c_url, author, title, release_date  from dwd_t_comment_3nd_quarter where c_url in ({})'.format(','.join(url_list))
sql2 = 'select url_link, replier, comment_content, comment_time from db_e_commerce_data_vm_comment where url_link in ({})'.format(','.join(url_list))
sql3 = 'select Product_SKU, Nickname, Comment, Comment_time from db_e_commerce_data where Product_SKU in ({})'.format(','.join(url_list))
df = a.read_select_sql(sql)
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# df1 = a.read_select_sql(sql1)
# df1.rename(columns={'c_url': 'url_link', 'author': 'replier', '': ''}, inplace=True)
username = 'db_e_commerce'
password = r'Zj690!#'
database = 'db_e_commerce_data_analysis'
a = sql_test.dbconnect(host, username, password, database, port)
df2 = a.read_select_sql(sql2)
# print(df2.info())
df3 = a.read_select_sql(sql3)
df3 = df3.rename(columns={'Product_SKU': 'url_link', 'Nickname': 'replier', 'Comment': 'comment_content', 'Comment_time': 'comment_time'})
df1 = pd.concat([df3, df2])
# print(df1.info())

pattern = re.compile('优惠|促销|双十一|618|双十二|机油推荐|推荐的机油|机油怎么样|双11|双12|818|抢购|价格|购买')
df1['purchase_intention'] = list(map(lambda x: 1 if pd.notna(x) and pattern.search(x)!=None else 0, df1['comment_content']))
df1['sentiment_analysis'] = list(map(lambda x: SnowNLP(x).sentiments if pd.notna(x) else np.nan, df1['comment_content']))
df1['sentiment_flag'] = list(map(lambda x: 0 if x <= 0.01 else(1 if x >= 0.8 else 2), df1['sentiment_analysis']))

# pattern = re.compile('动力|长效|噪音|保护|抗磨|清洁|静音|积碳|粘度|磨损|冷启动|抖动|油泥|油膜')
# df['characteristic'] = list(map(lambda x: ','.join(list(set(pattern.findall(x)))) if pd.notna(x) and pattern.search(x) != None else np.nan, df['comment_content']))

df = pd.concat([df, df1])
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dim_meifu_0w16_comment', data=df, if_exists='truncate')
