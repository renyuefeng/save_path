from snownlp import SnowNLP
import sql_test
import pandas as pd
import re
import numpy as np
import math

# host = '139.224.197.121'
# username = 'meifu_03'
# password = r'Zj690!#'
# database = 'dim_summery'
# port = 63306
#
# a = sql_test.dbconnect(host, username, password, database, port)
# # df = a.read_database(table_name='dim_summery')
# df1 = a.read_database(table_name='dim_summery_comment')
# print(df1.info())
#
# # 0.3-0.8
# df1['sentiment_analysis'] = list(map(lambda x: SnowNLP(x).sentiments if pd.notna(x) else np.nan, df1['comment_content']))
# df1['sentiment_analysis'] = list(map(lambda x: 0 if x <= 0.3 else(1 if x >= 0.8 else 2), df1['sentiment_analysis']))
#
# print(df1.info())
text = '美孚太好了'
s = SnowNLP(text)
print(s.sentiments)

# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery_comment', data=df1, if_exists='truncate')

