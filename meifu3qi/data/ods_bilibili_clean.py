import sql_test
import pandas as pd
import re
import numpy as np
import math

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'ods_bilibili'

port = 63306
a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='帖子_新增_copy1')

pattern = re.compile(' ')
pattern1 = re.compile('[\d\.]+')
# df['danmaku_count'] = list(map(lambda x: int(pattern.sub('', x)) if pd.notna(x) and pattern.search(x)!=None and pattern.sub('', x)!='' else 0, df['danmaku_count']))
# df['fans_count'] = list(map(lambda x: 0 if pd.isna(x) or x == '' else(float(pattern1.search(x).group()) * 10000 if '万' in x else int(x)), df['fans_count']))
# df['favourite_count'] = list(map(lambda x: 0 if pd.isna(x) or x == '' else(float(pattern1.search(x).group()) * 10000 if '万' in x else int(x)), df['favourite_count']))
#
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='帖子_新增_copy1', data=df, if_exists='truncate')

print(df.info())
df['keyword'] = '美孚速霸'
df['activity'] = '美孚'

df['interactive_count'] = list(map(lambda a, b, c, d, e, f, g: 0.01 * a + b + c + d + e + f + g, df['click_count'], df['danmaku_count'], df['coin_count'], df['like_count'], df['comment_count'], df['forward_count'], df['favourite_count']))

a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_bilibili_main_keywordMerge_copy1', data=df, if_exists='truncate')