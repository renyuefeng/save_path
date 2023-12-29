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
df = a.read_database(table_name='dwd_xiaohongshu_main')
df1 = a.read_database(table_name='dwd_xiaohongshu_publisher', list_field=['publisher_id', 'fans_count'])
pattern = re.compile(
    'edge|EDGE|Edge|NBA总决赛|昆仑机油|勇士总冠军|昆仑润滑油|LPL2022|NBA突破时刻|长城机油|LPL夏季赛|Discovery探索频道|英超联赛2022|美孚1号|英雄联盟职业联赛|克莱汤普森|KlayThompson|英雄联盟赛事|统一机油|王者荣耀职业联赛|嘉实多|统一润滑油|KPL夏季赛|长城润滑油|美孚1号NBA|LPL深夜档|美孚NBA|恒久动力，驰骋天地|嘉实多磁护|无畏竞巅峰|美孚速霸|美孚车用润滑油|突破无止境|拯救者 LPL|嘉实多极护|嘉实多magnatec|嘉实多2021/22英超关键先生|壳牌先锋|KPL王者荣耀职业联赛|嘉实多2021/22英超赛季最佳|嘉实多Castrol官方微博|萧敬腾 LPL|为爱而聚 E起前进|嘉实多EDGE|2022KPL夏季赛|美孚1号突破礼盒|关键时刻燃擎护航|壳牌锐净|探索未知世界，寻找自然奇迹；挑战已知界限，释放无限潜力|壳牌|美孚|LPL|lpl|kpl|Kpl|KPl|Lpl|龙蟠机油|龙蟠润滑油|EDG|edg|Edg|2022 KPL|决赛|NBA|Nba|nba|道达尔|KPL|英雄联盟|英超|Discovery|discovery|DISCOVERY|王者荣耀|勇士|冠军|磁护|极护|超凡喜力|克莱'
)

df['keyword'] = list(
    map(lambda x, y: ','.join(list(set(pattern.findall(x + y)))) if pd.notna(x) and pd.notna(y) and pattern.search(
        x + y) != None else (','.join(list(set(pattern.findall(x)))) if pd.notna(x) and pd.isna(y)
                             else (
        ','.join(list(set(pattern.findall(y)))) if pd.isna(x) and pd.notna(y) else np.nan)), df['content'],
        df['title']))

df['keyword'] = list(
    map(lambda x: re.compile('\W*(EDG)(?=\W|$)|\W*(edg)(?=\W|$)|\W*(Edg)(?=\W|$)').sub('', x) if pd.notna(
        x) and re.compile('\W*(EDG)(?=\W|$)|\W*(edg)(?=\W|$)|\W*(Edg)(?=\W|$)').search(x) != None and re.compile(
        '2022 KPL|KPL|王者荣耀职业联赛|KPL夏季赛|KPL王者荣耀职业联赛|2022KPL夏季赛|kpl|王者荣耀|Kpl').search(x) != None else x, df['keyword']))

# df['keyword'] = list(map(lambda x, y: x if pd.isna(y) else(x + ',' + y if pd.notna(x) else y), df['keyword'], df['collect_word']))

df = df.drop(['keyword'], axis=1).join(
    df['keyword'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('keyword'))

print(df.info())
df = df.drop_duplicates(subset=['keyword', 'url_link'])
print(df.info())

df = df.loc[(df['keyword'].notnull()) & (df['keyword'] != '')]

## 分类汇总
pattern_m = re.compile('美孚1号NBA|美孚NBA')
pattern_j = re.compile('嘉实多2021/22英超关键先生|嘉实多2021/22英超赛季最佳|嘉实多magnatec')
pattern_q = re.compile('F1 壳牌')
pattern_a = re.compile('英超|NBA|LPL|KPL|Discovery|F1')
df['activity'] = list(map(lambda x: '美孚,NBA'
if pd.notna(x) and pattern_m.search(x) != None else ('嘉实多,英超' if pd.notna(x) and pattern_j.search(x) != None
                                                     else (
    '壳牌,F1' if pd.notna(x) and pattern_q.search(x) != None else '')), df['keyword']))
print(df.info())
df = df.drop(['activity'], axis=1).join(
    df['activity'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('activity'))

pattern_1 = re.compile('^EDG$|LPL 2022|LPL|LPL 夏季赛|英雄联盟职业联赛|英雄联盟赛事|LPL深夜档|无畏竞巅峰|拯救者 LPL|萧敬腾 LPL|为爱而聚 E起前进|英雄联盟|lpl|^edg$|^Edg$|Lpl|LPl|LpL')
pattern_2 = re.compile('NBA总决赛|勇士总冠军|NBA突破时刻|克莱汤普森 Klay Thompson|美孚1号NBA|美孚NBA|恒久动力，驰骋天地|突破无止境|美孚1号突破礼盒|nba|NBA|Nba|克莱汤普森|Klay Thompson|勇士|冠军|决赛|克莱')
pattern_3 = re.compile('2022 KPL|KPL|王者荣耀职业联赛|KPL夏季赛|KPL王者荣耀职业联赛|2022KPL夏季赛|kpl|王者荣耀|Kpl|KPl|KpL')
pattern_4 = re.compile('英超联赛2022|嘉实多magnatec|嘉实多 2021/22英超关键先生|嘉实多 2021/22英超赛季最佳|关键时刻燃擎护航|英超')
pattern_5 = re.compile('Discovery探索频道|探索未知世界，寻找自然奇迹；挑战已知界限，释放无限潜力|Discovery|discovery|DISCOVERY')
pattern_6 = re.compile('美孚1号|美孚NBA|美孚速霸|美孚车用润滑油|美孚1号突破礼盒|美孚|美孚一号')
pattern_7 = re.compile('嘉实多|嘉实多磁护|嘉实多极护|嘉实多magnatec|嘉实多2021|嘉实多Castrol官方微博|嘉实多EDGE|EDGE极护|嘉实多 EDGE|EDGE 极护|磁护|极护')
pattern_8 = re.compile('壳牌先锋|壳牌锐净|壳牌|超凡喜力')
pattern_9 = re.compile('\w*(?=机油|润滑油)')
pattern_10 = re.compile('法拉利 壳牌|夏尔·勒克莱尔|F1 2022赛季|极竞非凡，敢战不可能|夏尔·勒克莱尔 壳牌|F1|f1')
pattern_11 = re.compile('道达尔')

df['activity'] = list(map(lambda x, y: y if pd.notna(y) and y != '' else ('LPL' if pattern_1.search(x) != None
                                                                          else ('NBA' if pattern_2.search(x) != None
                                                                                else (
    'KPL' if pattern_3.search(x) != None
    else ('英超' if pattern_4.search(x) != None
          else ('Discovery' if pattern_5.search(x) != None
                else ('美孚' if pattern_6.search(x) != None
                      else ('嘉实多' if pattern_7.search(x) != None
                            else ('壳牌' if pattern_8.search(x) != None
                                  else ('F1' if pattern_10.search(x) != None
                                        else ('道达尔' if pattern_11.search(x) != None
                                              else (
        pattern_9.search(x).group() if pattern_9.search(x) != None else np.nan))))))))))), df['keyword'],
                          df['activity']))

pattern_m1 = re.compile('美孚1号|美孚1号突破礼盒')
pattern_mj = re.compile('美孚速霸')
pattern_jc = re.compile('嘉实多磁护|嘉实多magnatec|磁护')
pattern_jj = re.compile('嘉实多极护|极护|嘉实多EDGE|edge|EDGE|Edge')
pattern_qx = re.compile('壳牌喜力')
pattern_qc = re.compile('壳牌超级喜力')
df['keyword'] = list(map(lambda y: '美孚一号' if pattern_m1.search(y) != None and pd.notna(y)
else ('美孚速霸' if pattern_mj.search(y) != None and pd.notna(y)
      else ('嘉实多磁护' if pattern_jc.search(y) != None and pd.notna(y)
            else ('嘉实多极护' if pattern_jj.search(y) != None and pd.notna(y)
                  else ('壳牌喜力' if pattern_qx.search(y) != None and pd.notna(y)
                        else ('壳牌超级喜力' if pattern_qc.search(y) != None and pd.notna(y) else y))))), df['keyword']))
print('去重', df.info())
df.drop_duplicates(subset=['activity', 'url_link'], inplace=True)
print(df.info())


pattern_d = re.compile('感染|埃里克|驱蚊|蚊香液|违章停车|蚊子|孕妇|儿童|避蚊胺|轨迹|阳性')
pattern_m = re.compile(
    '香港|惠州|美孚新村|皇家美孚|公寓|老鼠|茶餐廳|九华径|美孚站|唐美孚|洋行|美孚教育|海南省博物馆|根斯堡|麦当劳|科伦|西乡|阳性|新冠|马斯克|美股|美媒|道指|拜登|新邨|环球时报|华尔街日报|乌克兰|俄|警方|A股|股票|股权|福布斯|股东|区块链| Odoptu OP-11油井|美孚酱|美孚英语|gregmat|多多饼店|港独|袭警|西部世界|飞马文学奖')
pattern_j = re.compile('肠粉|阳性|新冠|马斯克|美股|美媒|道指|拜登|环球时报|华尔街日报|乌克兰|美国|俄|警方|A股|股票|美元|股权|福布斯|股东|区块链')
pattern_q = re.compile('大壳牌怒音|阳性|新冠|马斯克|美股|美媒|道指|拜登|环球时报|华尔街日报|乌克兰|美国|俄|警方|A股|股票|美元|股权|福布斯|股东|区块链')

df['flag'] = list(map(lambda x, y: 0 if x == '美孚' and pattern_m.search(y) != None and '车养护' not in y else (
    0 if x == '道达尔' and pattern_d.search(y) != None
    else (0 if x == '嘉实多' and pattern_j.search(y) != None
          else (0 if x == '壳牌' and pattern_q.search(y) != None else 1))), df['activity'], df['content']))
print('无关', df.info())
df = df.loc[df['flag'] == 1]
print(df.info())
df['interactive_count'] = list(
    map(lambda x, y, z: x + y + z, df['favorites_count'], df['like_count'], df['comment_count']))

df2 = df1.sort_values(by=['fans_count'], ascending=False).head(1000)[['publisher_id']]
df2['user_sort'] = 'PGC'
df1 = pd.merge(df1, df2, on='publisher_id', how='left')
print(df1.info())
# pattern_g = re.compile('官方')
df1['user_sort'] = list(map(lambda x: x if pd.notna(x) else 'UGC', df1['user_sort']))
df1.drop(['fans_count'], axis=1, inplace=True)
print('合并', df.info())
df = pd.merge(df, df1, on='publisher_id', how='left')
print(df.info())
df['interactive_count'] = list(
    map(lambda x, y, z: x + y + z, df['favorites_count'], df['like_count'], df['comment_count']))
# df['interactive_count'] = list(map(lambda x, y, z: x + y + z, df['favorites_count'], df['like_count'], df['comment_count']))

# pattern_1 = re.compile('EDG|LPL 2022|LPL|LPL 夏季赛|英雄联盟职业联赛|英雄联盟赛事|LPL深夜档|无畏竞巅峰|拯救者 LPL|萧敬腾 LPL|为爱而聚 E起前进|英雄联盟|lpl')
# df['activity'] = list(map(lambda x: 'LPL'
# if pd.notna(x) and pattern_1.search(x) != None else np.nan, df['keyword']))
#
# pattern_2 = re.compile('NBA总决赛|勇士总冠军|NBA突破时刻|克莱汤普森 Klay Thompson|美孚1号NBA|美孚NBA|恒久动力，驰骋天地|突破无止境|美孚1号突破礼盒|nba|NBA')
# df['activity'] = list(map(lambda x, y: 'NBA'
# if pd.notna(x) and pattern_2.search(x) != None else y, df['keyword'], df['activity']))
#
# pattern_3 = re.compile('2022 KPL|KPL|王者荣耀职业联赛|KPL夏季赛|KPL王者荣耀职业联赛|2022KPL夏季赛|kpl')
# df['activity'] = list(map(lambda x, y: 'KPL'
# if pd.notna(x) and pattern_3.search(x) != None else y, df['keyword'], df['activity']))
#
# pattern_4 = re.compile('英超联赛2022|嘉实多magnatec|嘉实多 2021/22英超关键先生|嘉实多 2021/22英超赛季最佳|关键时刻燃擎护航|英超')
# df['activity'] = list(map(lambda x, y: '英超'
# if pd.notna(x) and pattern_4.search(x) != None else y, df['keyword'], df['activity']))
# pattern_5 = re.compile('Discovery探索频道|探索未知世界，寻找自然奇迹；挑战已知界限，释放无限潜力|Discovery')
# df['activity'] = list(map(lambda x, y: 'Discovery'
# if pd.notna(x) and pattern_5.search(x) != None else y, df['keyword'], df['activity']))
# pattern_6 = re.compile('美孚1号|美孚NBA|美孚速霸|美孚车用润滑油|美孚1号突破礼盒|美孚')
# df['activity'] = list(map(lambda x, y: '美孚'
# if pd.notna(x) and pattern_6.search(x) != None else y, df['keyword'], df['activity']))
# pattern_7 = re.compile('嘉实多|嘉实多磁护|嘉实多极护|嘉实多magnatec|嘉实多2021|嘉实多Castrol官方微博|嘉实多EDGE')
# df['activity'] = list(map(lambda x, y: '嘉实多'
# if pd.notna(x) and pattern_7.search(x) != None else y, df['keyword'], df['activity']))
# pattern_8 = re.compile('壳牌先锋|壳牌锐净|壳牌')
# df['activity'] = list(map(lambda x, y: '壳牌'
# if pd.notna(x) and pattern_8.search(x) != None else y, df['keyword'], df['activity']))
##########
df.drop(['flag'], axis=1, inplace=True)
# df.drop(['collect_word', 'keyword'], axis=1, inplace=True)

a = sql_test.dbconnect(host, username, password, database, port)
a.insert_database(table_name='dwd_xiaohongshu_main_keywordMerge', data=df, if_exists='truncate')
