import sql_test
import sql_test_new
import re
import pandas as pd
import jieba
import datetime, time
import numpy as np

jieba.setLogLevel(jieba.logging.INFO)

def isTimeContinuous(df, sum_count='count', time_move=1):

    sum_count = df[sum_count].sum()
    len_df = df.shape[0]
    if len_df <= 10:
        df['flag'] = 0
        df['flag_sj_1'] = '0'
        df['flag_sj_2'] = '0'
        df['flag_sj_3'] = '0'
        return df
    else:
        if time_move == 1:
            df['count_shift'] = df['count'].shift(1)
            df['count_shift_d'] = df['count'].shift(-1)
            df['time_shift'] = df['timestamp'].shift(1)
            df['time_shift_d'] = df['timestamp'].shift(-1)

            df['flag'] = list(map(lambda x, y, a, b: '0' if pd.isna(y) else('0.2' if (int(eval(x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(eval(x + '-' + y)) == 77) and ((a - b) > (sum_count / len_df)) else '0'), df['timestamp'], df['time_shift'], df['count'], df['count_shift']))
            df['flag1'] = list(map(lambda x, y, a, b: '0' if pd.isna(x) else('0.05' if (int(eval(x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(eval(x + '-' + y)) == 77) and ((b - a) > (sum_count / len_df)) else '0'), df['time_shift_d'], df['timestamp'], df['count_shift_d'], df['count']))
            df['flag'] = list(map(lambda x, y: str(eval(x + '+' + '0.1')) if y > 2 * sum_count/len_df else x, df['flag'], df['count']))
            df['flag'] = list(map(lambda x, y: eval(x + '+' + y), df['flag'], df['flag1']))

            df['flag_sj_1'] = list(map(lambda x, y, a, b: '0' if pd.isna(y) else('0.2' if (int(eval(x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(eval(x + '-' + y)) == 77) and ((a - b) > (sum_count / len_df)) else '0'), df['timestamp'], df['time_shift'], df['count'], df['count_shift']))
            df['flag_sj_2'] = list(map(lambda x, y, a, b: '0' if pd.isna(x) else('0.05' if (int(eval(x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(eval(x + '-' + y)) == 77) and ((b - a) > (sum_count / len_df)) else '0'), df['time_shift_d'], df['timestamp'], df['count_shift_d'], df['count']))
            df['flag_sj_3'] = list(map(lambda x, y: '0.1' if y > 2 * sum_count/len_df else '0', df['flag'], df['count']))

            df.drop(['flag1'], axis=1, inplace=True)

            # print(df[['timestamp', 'time_shift', 'count', 'count_shift', 'count_shift_d', 'flag']].head())
            # print(sum_count/len_df)
        else:
            pass
        return df

def stdCountSum(df):

    std_count = np.std(df['count'])
    df['std_count'] = std_count

    return df

# path = './data/通用去水-微博(1).txt'
#
# with open(path) as d:
#     dat = d.readlines()
#     lis = []
#     for i in dat:
#         lis.append(re.sub('\n', '', i))
#     b = '|'.join(lis)
# pattern = re.compile(b)
# print('aaaa')

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
port = 63306

# sql = 'select replier, comment_content, url_link from dim_summery_comment'
sql = 'select replier, comment_content, url_link, comment_time, sentiment_flag from dim_summery_comment where url_link in (select distinct url_link from dim_summery where pub_time between 20220301 and 20220911)'

a = sql_test_new.dbconnect(host, username, password, database, port)
# df = a.read_database(table_name='dim_summery_comment', list_field=['replier', 'comment_content', 'content_id'])
df = a.read_select_sql(sql=sql)

df = df.loc[df['comment_time'].notnull()]

# df = sql_test_new.pandasReadSQL(host=host, username=username, password=password, database=database, port=port, sql=sql)
####### 昵称判断 ######## 0.15
pattern = re.compile('[\Wa-zA-Z]$')
df['flag'] = list(map(lambda x: 0.1 if pd.notna(x) and x != '' and x != ' ' and len(list(jieba.cut(x, cut_all=False))[-1]) <= 1 else(0.1 if pd.notna(x) and pattern.search(x)!=None else 0), df['replier']))
df['flag'] = list(map(lambda y, x: y + 0.05 if pd.notna(x) and 5 < len(x) <= 8 else y, df['flag'], df['replier']))
df['flag_nc'] = df['flag']
########### 评论判定 ############ 0.35
pattern1 = re.compile('太棒了|很有感觉|超级美|润滑油|不错|好棒|支持|给力|实力|宠粉|大家|相见恨晚|征服|放心|有了|感谢|认准|车用润滑油|分享|好用|希望|关注|热爱|养车|中奖|信赖|好赞|不赖|欢迎|需要|氛围感|一直|好车|好油|好的产品|太赞了|哇哦|厉害了|优惠|优秀|价格便宜|特别好|快点|参与|推荐|羡慕|销量|力度|吸睛|赶快|相当|中国品牌|国货之光|鼓掌|高性能|强悍|创新|开始|深爱|冬奥|东奥|迷恋|吸引|美孚|嘉实多|壳牌|统一|长城|昆仑|龙蟠|道达尔')
pattern2 = re.compile('不好|不行|垃圾|不买|好贵|太贵|不建议|不好用|不要|不太行|不怎么好')

df['flag_pl'] = list(map(lambda y: 0.05 if pd.notna(y) and 10 < len(y) <= 30 else 0, df['comment_content']))
df['flag'] = list(map(lambda y, x: y + 0.05 if pd.notna(x) and 10 < len(x) <= 30 else y, df['flag'], df['comment_content']))
df['flag'] = list(map(lambda x, y: y + 0.3 if pd.notna(x) and pattern1.search(x)!=None and pattern2.search(x)==None else y, df['comment_content'], df['flag']))

########### 时间判定 ############ 0.4
# 修改时间格式
df['month'] = df.comment_time.dt.month
df['month'] = list(map(lambda x: '0' + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['month']))
df['day'] = df.comment_time.dt.day
df['day'] = list(map(lambda x: '0' + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['day']))
df['year'] = df.comment_time.dt.year
df['hour'] = df.comment_time.dt.hour
df['hour'] = list(map(lambda x: '0' * (2 - len(str(x).strip('.'))) + str(x).strip('.') if len(str(x).strip('.')) < 2 else str(x), df['hour']))
df['timestamp'] = list(map(lambda a, b, c, d: str(a) + str(b) + str(c) + str(d), df['year'], df['month'], df['day'], df['hour']))
df.drop(columns=['month', 'day', 'year', 'hour'], axis=1, inplace=True)
# 统计每个url_link时间下发帖
df1 = df.groupby(by=['url_link', 'timestamp'])['comment_time'].count().reset_index()
df1.rename(columns={'comment_time': 'count'}, inplace=True)

# 计算连续时间内贴文的突增值
df1 = df1.groupby('url_link').apply(isTimeContinuous)
df1 = df1.groupby(df1['url_link']).apply(stdCountSum)

df1['flag_comment'] = list(map(lambda x: 0.05 if x > 10 else 0, df1['std_count']))
df1['flag_sj_4'] = df1['flag_comment']
df1['flag_comment'] = list(map(lambda x, y: x + y, df1['flag_comment'], df1['flag']))
df1.drop(['flag'], axis=1, inplace=True)
# 合并数据 #
df = pd.merge(df, df1, on=['url_link', 'timestamp'], how='outer')
# print(df.info())
df['flag'] = list(map(lambda x, y: x + y, df['flag_comment'], df['flag']))

df.drop(['flag_comment'], axis=1, inplace=True)
# df.rename(columns={'flag_comment': 'flag_sj_4'}, inplace=True)
df.drop(['count_shift', 'count_shift_d', 'time_shift', 'time_shift_d', 'std_count'], axis=1, inplace=True)

############ 正负向 ############ 0.1

df['flag'] = list(map(lambda x, y: x + 0.1 if y == 1 else x, df['flag'], df['sentiment_flag']))
print(df.info())
# print(df.value_counts('flag'))

def sumWaterPeople(df):

    avg_flag = df.shape[0]
    sum_count = df['flag'].sum()
    df['avg_flag'] = sum_count/avg_flag

    return df
df = df.groupby('url_link').apply(sumWaterPeople)

a = sql_test_new.dbconnect(host, username, password, database, port)
# df.to_excel('./shuijun.xlsx', encoding='utf-8')
a.insert_database(table_name='dim_summery_comment_shuijun', data=df, if_exists='truncate')


# df.to_excel('../yhjx.xlsx', encoding='utf-8')
# df.groupby('comment_time').apply()

# df = a.read_select_sql(sql=sql)
# print('aaaa')
#
# df['flag'] = list(map(lambda x: 1 if pd.notna(x) and pattern.search(x)!=None else 0, df['comment_content']))
# df = df.loc[df['flag'] == 1]
# # def replyCommentJudge(col=''):
# #
# #
# #     return df
#
# df1 = df.groupby('replier')['content_id'].count().reset_index()
# # df1 = df1.set_index(['replier', 'count'])
# df1.rename(columns={'content_id': 'count'}, inplace=True)
# # print(df1.info())
# # print(df1.head())
# df = pd.merge(df[['content_id', 'replier']], df1, on='replier', how='left')
# df.drop_duplicates(['replier', 'count'], inplace=True)
# # print(df.info())
# # print(df.head())
# df = df.sort_values(by='count', ascending=False)
# # df = df.loc[df['count'] >= 50]
# df.to_excel('./data/water.xlsx')
# df1.head(20)
# print(df.head(20))
