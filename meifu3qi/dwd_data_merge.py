import sql_test
import pandas as pd
import re
import numpy as np
import math

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
port = 63306

# database = 'dwd_weibo'
# a = sql_test.dbconnect(host, username, password, database, port)
# df = a.read_database(table_name='dwd_weibo_main_keywordMerge', list_field=['keyword', 'activity', 'collect_word', 'url_link', 'content', 'content_id', 'pub_time', 'tag', 'publisher', 'user_sort', 'pub_id', 'identity', 'forward_count', 'comment_count', 'like_count', 'interactive_count'])
# df['platform'] = '微博'
# # df.rename({}, inplace=True)
#
# database = 'dwd_hupu_03'
# a = sql_test.dbconnect(host, username, password, database, port)
# df1 = a.read_database(table_name='dwd_hupu_main_keywordMerge', list_field=['keyword', 'activity', 'article_keyword', 'url_link', 'title', 'content', 'pub_time', 'publisher', 'user_sort', 'publisher_link', 'forward_count', 'comment_count', 'like_count', 'click_count', 'interactive_count'])
# df1['platform'] = '虎扑'
# df1 = df1.rename(columns={'article_keyword': 'collect_word', 'publisher_link': 'pub_id'})
# # print(df1.info())
# database = 'dwd_xiaohongshu_03'
# a = sql_test.dbconnect(host, username, password, database, port)
# df2 = a.read_database(table_name='dwd_xiaohongshu_main_keywordMerge', list_field=['keyword', 'activity', 'collect_keyword', 'url_link', 'title', 'content', 'url_link_id', 'pub_time', 'publisher', 'user_sort', 'publisher_id', 'comment_count', 'like_count', 'interactive_count'])
# df2['platform'] = '小红书'
# df2 = df2.rename(columns={'url_link_id': 'content_id', 'publisher_id': 'pub_id', 'collect_keyword': 'collect_word'})

# database = 'dwd_zhihu'
# a = sql_test.dbconnect(host, username, password, database, port)
# df3 = a.read_database(table_name='dwd_zhihu_main_keywordMerge', list_field=['keyword', 'activity', 'collect_word', 'url_link', 'title', 'content', 'url_link_id', 'answer_time', 'answer_nickname', 'user_sort', 'comment_count', 'like_count', 'interactive_count'])
# df3['platform'] = '知乎'
# df3 = df3.rename(columns={'publisher_id': 'pub_id', 'answer_time': 'pub_time', 'answer_nickname': 'publisher', 'url_link_id': 'pub_id'})

# database = 'dwd_douyin'
# a = sql_test.dbconnect(host, username, password, database, port)
# df4 = a.read_database(table_name='dwd_douyin_main_keywordMerge', list_field=['keyword', 'activity', 'classification', 'url_link', 'title', 'pub_time', 'publisher_nickname', 'publisher_link', 'user_sort', 'comment_count', 'like_count', 'interactive_count'])
# df4['platform'] = '抖音'
# df4 = df4.rename(columns={'classification': 'collect_word', 'publisher_link': 'pub_id', 'publisher_nickname': 'publisher', 'title': 'content'})

database = 'dwd_bilibili'
a = sql_test.dbconnect(host, username, password, database, port)
df4 = a.read_database(table_name='dwd_bilibili_main_keywordMerge', list_field=['keyword', 'activity', 'collect_keyword', 'url_link', 'title', 'content', 'pub_time', 'publisher_nickname', 'publisher_id', 'user_sort', 'comment_count', 'like_count', 'forward_count', 'interactive_count', 'click_count', 'tag'])
df4['platform'] = 'bilibili'
df4 = df4.rename(columns={'publisher_id': 'pub_id', 'collect_keyword': 'collect_word', 'publisher_nickname': 'publisher', '': ''})

# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# df5 = a.read_database(table_name='dim_海量3期', list_field=['keyword', 'activity', 'collect_keyword', 'url_link', 'title', 'content', 'pub_time', 'publisher_nickname', 'publisher_id', 'user_sort', 'comment_count', 'like_count', 'interactive_count'])
# df5['platform'] = '海量'
# df5 = df5.rename(columns={'publisher_id': 'pub_id', 'collect_keyword': 'collect_word', 'publisher_nickname': 'publisher'})

# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery', data=df, if_exists='truncate')
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery', data=df1, if_exists='append')
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery', data=df2, if_exists='append')
# database = 'dim_summery'
# a = sql_test.dbconnect(host, username, password, database, port)
# a.insert_database(table_name='dim_summery', data=df3, if_exists='append')
database = 'dim_summery'
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dim_summery', data=df4, if_exists='append')
