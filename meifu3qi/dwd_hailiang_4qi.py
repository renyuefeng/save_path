import sql_test
import pandas as pd
import re
import numpy as np

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dwd_海量'
port = 63306

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dwd_t_data_4st_quarter', list_field=['url', 'title', 'release_date', 'author', 'comments_count', 'click_count'])
df.rename(columns={'url': 'url_link', 'release_date': 'pub_time', 'author': 'publisher', 'comments_count': 'comment_count'}, inplace=True)
# print(aaa)
df['voice_count'] = list(map(lambda x: x + 1, df['comment_count']))
pattern = re.compile('香港|惠州|美孚新村|皇家美孚|香港美孚|公寓|老鼠|茶餐廳|港铁|地下鐵路|九华径|美孚站|唐美孚|美孚基|洋行|美孚教育|海南省博物馆|根斯堡|麦当劳|科伦|咖啡|西乡|阳性|新冠|马斯克|美股|美媒|道指|石油|拜登|新邨|环球时报|华尔街日报|乌克兰|美国|俄|警方|A股|股票|美元|股权|福布斯|股东|区块链| Odoptu OP-11油井|美孚酱|美孚英语|gregmat|多多饼店|港独|袭警|西部世界|飞马文学奖|埃克森美孚|对华政策|天然气|原油|哈萨克斯坦|食物链|加仓|马来西亚|西方国家|孙燕姿|普京|西方|原始社会|王思聪|感染|埃里克|驱蚊|蚊香液|违章停车|蚊子|孕妇|儿童|避蚊胺|轨迹|阳性|大壳牌怒音|阳性|新冠|马斯克|美股|美媒|道指|拜登|环球时报|华尔街日报|乌克兰|美国|俄|警方|A股|股票|美元|股权|福布斯|股东|区块链|华晨宇|伊丽莎白|地震|方便面|媒体|交通|椰壳牌')
df['flag'] = list(map(lambda x: 1 if pd.notna(x) and pattern.search(x)!=None else 0, df['title']))
df = df.loc[df['flag'] == 0]
df.drop(['flag'], axis=1, inplace=True)

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
port = 63306
a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dim_海量3期_copy', data=df, if_exists='append')
