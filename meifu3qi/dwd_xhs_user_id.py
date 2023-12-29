import sql_test
import pandas as pd
import re
import numpy as np
import math

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dwd_xiaohongshu_03'

port = 63306
a = sql_test.dbconnect(host, username, password, database, port)

sql = 'select publisher_id from dwd_xiaohongshu_main_keywordMerge where user_sort is null'
# df = a.read_database(table_name='dwd_xiaohongshu_main')
df = a.read_select_sql(sql=sql)

print(df.info())

df.to_excel('xhs_userId_10_20.xlsx')
