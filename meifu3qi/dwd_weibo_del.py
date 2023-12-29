import sql_test
import pandas as pd
import re
import numpy as np

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dwd_weibo'

sql = 'select url_link from dwd_weibo_main where url_link in (select url_link from url_link)'

port = 63306
a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_select_sql(sql=sql)
df_m = a.read_database(table_name='dwd_weibo_main')

lis_url = df['url_link'].to_list()
# print(df_m.info())
df_m['flag'] = list(map(lambda x: 0 if x in lis_url else 1, df_m['url_link']))
df_m = df_m.loc[df_m['flag'] == 1]
df_m.drop(['flag'], axis=1, inplace=True)
# print(df_m.info())

a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_weibo_main_copy1', data=df_m, if_exists='truncate')