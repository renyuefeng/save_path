import re

import sql_test
import pandas as pd
import numpy as np
from snownlp import SnowNLP

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
port = 63306

database = 'dwd_weibo'
a = sql_test.dbconnect(host, username, password, database, port)
sql = 'SELECT B.url_link,A.replier,A.comment_content,A.comment_time FROM (SELECT content_id,replier,comment_content,comment_time FROM dwd_weibo_comment) A LEFT JOIN (SELECT content_id,url_link FROM dwd_weibo_main) B ON A.content_id = B.content_id'
# df = a.read_database(table_name='dwd_weibo_comment', list_field=['url_link', 'replier', 'comment_content', 'comment_time'])
df = a.read_select_sql(sql=sql)
# df['platform'] = '微博'
# df.rename({}, inplace=True)
# #
# database = 'dwd_hupu_03'
# a = sql_test.dbconnect(host, username, password, database, port)
# df1 = a.read_database(table_name='dwd_hupu_comment', list_field=['url_link', 'replier', 'comment_content', 'comment_time'])
#
# # df1['platform'] = '虎扑'
# # df1 = df1.rename(columns={'article_keyword': 'collect_word', 'publisher_link': 'pub_id'})
# print(df1.info())
# database = 'dwd_xiaohongshu_03'
# a = sql_test.dbconnect(host, username, password, database, port)
# df2 = a.read_database(table_name='dwd_xiaohongshu_comment', list_field=['url_link', 'replier', 'comment_content', 'comment_time'])

# 无评论时间
# database = 'dwd_zhihu'
# a = sql_test.dbconnect(host, username, password, database, port)
# df3 = a.read_database(table_name='dwd_zhihu_comment', list_field=['url_link_id', 'replier_nickname', 'reply_content'])
# df_z = a.read_database(table_name='dwd_zhihu_main_keywordMerge', list_field=['url_link', 'url_link_id'])
# df3 = pd.merge(df3, df_z, on='url_link_id')
# df3.rename(columns={'replier_nickname': 'replier', 'reply_content': 'comment_content'}, inplace=True)
# df3.drop(['url_link_id'], axis=1, inplace=True)
#
# database = 'dwd_douyin'
# a = sql_test.dbconnect(host, username, password, database, port)
# df4 = a.read_database(table_name='dwd_douyin_comment', list_field=['url_link', 'replier_nickname', 'comment_content', 'comment_time'])
# df4.rename(columns={'replier_nickname': 'replier'}, inplace=True)

database = 'dwd_bilibili'
a = sql_test.dbconnect(host, username, password, database, port)
sql = 'select DISTINCT url_link, bv_no from dwd_bilibili_main_keywordMerge'
# df_b = a.read_database(table_name='dwd_bilibili_main_keywordMerge', list_field=['url_link', 'bv_no'])
df_b = a.read_select_sql(sql=sql)
df5 = a.read_database(table_name='dwd_bilibili_comment', list_field=['bv', 'replier', 'comment_content', 'comment_time'])
print(df_b.info())
print(df5.info())
df5 = pd.merge(df5, df_b, left_on='bv', right_on='bv_no', how='left')
df5.dropna(subset=['url_link'], axis=0, inplace=True)
df5.drop(['bv', 'bv_no'], axis=1, inplace=True)
# df5.rename(columns={'replier_nickname': 'replier'}, inplace=True)
print(df5.info())
print(df5.shape[0])
# df2['platform'] = '小红书'
# df2 = df2.rename(columns={'url_link_id': 'content_id', 'publisher_id': 'pub_id', 'collect_keyword': 'collect_word'})

# df_all = pd.concat([df3, df4])
df_all = df5
# df_all = df1
pattern = re.compile('优惠|促销|双十一|618|双十二|机油推荐|推荐的机油|机油怎么样|双11|双12|818|抢购|价格|购买')
df_all['purchase_intention'] = list(map(lambda x: 1 if pd.notna(x) and pattern.search(x)!=None else 0, df_all['comment_content']))
df_all['sentiment_analysis'] = list(map(lambda x: SnowNLP(x).sentiments if pd.notna(x) else np.nan, df_all['comment_content']))
df_all['sentiment_flag'] = list(map(lambda x: 0 if x <= 0.01 else(1 if x >= 0.8 else 2), df_all['sentiment_analysis']))

database = 'dim_summery'
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dim_summery_comment', data=df_all, if_exists='append')
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery_comment', data=df1, if_exists='append')
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery_comment', data=df2, if_exists='append')
