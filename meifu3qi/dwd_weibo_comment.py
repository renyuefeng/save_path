import sql_test
import pandas as pd
import re
import numpy as np

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dwd_weibo'

port = 63306
a = sql_test.dbconnect(host, username, password, database, port)
df_main = a.read_database(table_name='dwd_weibo_main_keywordMerge_delete', list_field=['activity', 'content_id'])
df = a.read_database(table_name='dwd_weibo_comment')

df = pd.merge(df, df_main, on='content_id')
df = df.loc[df['activity'].notnull()]

a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_weibo_comment_keywordMerge', data=df, if_exists='truncate')