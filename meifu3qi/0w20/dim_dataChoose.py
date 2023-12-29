import sql_test
import pandas as pd
import re
import numpy as np
import math
from defSet import dataCleanDef


host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
port = 63306

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dim_meifu_0w20')
print(df.info())
df['tag'] = list(map(lambda x: x if pd.notna(x) else '', df['tag']))
df['title'] = list(map(lambda x: x if pd.notna(x) else '', df['title']))
df['content'] = list(map(lambda x: x if pd.notna(x) else '', df['content']))

df['all_text'] = list(
    map(lambda x, y, z: str(str(x) + str(y) + str(z)) if pd.notna(str(x) + str(y) + str(z)) else np.nan, df['content'],
        df['tag'], df['title']))
# 机油特性
pattern = re.compile('动力|长效动力|长效抗磨|长效保护|长效|噪音|保护|抗磨|清洁|静音|积碳|粘度|磨损|冷启动|抖动|油泥|油膜')
patternb = re.compile('保护性能好|更好的保护|更强保护|保护好|保护能力|保护作用|保护能力|保护发动机|发动机保护|油膜保护|保护油膜|高温保护|磨损保护|抗磨保护|抗磨损保护|保护性能好|更好的保护|更强保护|保护好|保护能力|保护作用|保护能力|保护发动机|发动机保护|油膜保护|保护油膜|高温保护|磨损保护|抗磨保护|抗磨损保护|保护性能好|更好的保护|更强保护|保护好|保护能力|保护作用|保护能力|保护发动机|发动机保护|油膜保护|保护油膜|高温保护|磨损保护|抗磨保护|抗磨损保护')
patternd = re.compile('动力好|动力强|动力方面|动力响应快|动力不错|动力澎湃|动力应该很不错|动力更好|动力很强|动力体感好|动力确实不错|动力很好|动力还算可以|动力不弱|动力更强|动力最强|动力非常好|动力很棒|动力没得说|动力挺好|动力很满意|动力很足|动力给力|动力也不差|动力很不错|动力强大|动力还是可以的|动力不差|动力挺好的|动力还行|动力也还可以|动力还是可以|日常加速动力|动力表现不错|动力带劲|动力表现令人满意|动力还好|动力表现')
patternq = re.compile('清洁能力好|清洁能力不错|清洁能力也强|清洁能力更好|清洁能力可真不错|清洁性好|清洁性比较好|清洁性不错|清洁性行|清洁性也不错|清洁性更好|清洁性可真不错|清洁度高|清洁度好|清洁作用|清洁作用好|清洁作用不错|清洁性能|清洁性能好|清洁保护性能|清洁效果|清洁效果好|长效性清洁|强清洁|主打清洁|超强清洁|环保清洁|清洁作用更加出|清洁分散|清洁棒|清洁力方面')
patternn = re.compile('高温粘度|粘度高|粘度低|粘度值|粘度较大|粘度越大|粘度等级|粘度级别|更低的粘度|低粘度|高粘度')
df['flag'] = list(map(lambda x, y: ','.join(list(set(patternb.findall(y)))) if pd.notna(x) and pd.notna(y) and '保护' in x and patternb.search(y)!=None else np.nan, df['characteristic'], df['all_text']))
df['flag1'] = list(map(lambda x, y: ','.join(list(set(patternd.findall(y)))) if pd.notna(x) and pd.notna(y) and '动力' in x and patternd.search(y)!=None else np.nan, df['characteristic'], df['all_text']))
df['flag2'] = list(map(lambda x, y: ','.join(list(set(patternn.findall(y)))) if pd.notna(x) and pd.notna(y) and '粘度' in x and patternn.search(y)!=None else np.nan, df['characteristic'], df['all_text']))
df['flag3'] = list(map(lambda x, y: ','.join(list(set(patternq.findall(y)))) if pd.notna(x) and pd.notna(y) and '粘度' in x and patternq.search(y)!=None else np.nan, df['characteristic'], df['all_text']))

df['characteristic'] = list(
    map(lambda x: ','.join(list(set(pattern.findall(x)))) if pd.notna(x) and pattern.search(x) != None else np.nan,
        df['all_text']))

df['characteristic'] = list(
    map(lambda x: re.sub('噪音', '静音', x) if pd.notna(x) and '噪音' in x else x, df['characteristic']))

pattern1 = re.compile('0w.{0,1}20.{0,5}保护|保护.{0,5}0w.{0,1}20')
df['characteristic'] = list(
    map(lambda x, y: re.sub('保护', '', y) if pd.notna(y) and '保护' in y and pd.notna(x) and pattern1.search(x) == None else y, df['all_text'], df['characteristic']))
# df = df.loc[df['flag'] != 0]
pattern2 = re.compile('发动机.{0,8}磨损|磨损.{0,8}发动机|零件.{0,8}磨损|磨损.{0,8}零件')
df['characteristic'] = list(
    map(lambda x, y: re.sub('磨损', '抗磨', y) if pd.notna(y) and '磨损' in y and pd.notna(x) and pattern1.search(x) == None else y, df['all_text'], df['characteristic']))

df['characteristic'] = list(map(lambda x: ','.join(list(set(x.split(',')))) if pd.notna(x) else x, df['characteristic']))

# df = dataCleanDef.splitSentenceUseSnownlp(df, col='all_text')
df = dataCleanDef.modelClean(df, col='all_text', out_model='model2')

# df = df.drop(['characteristic'], axis=1).join(df['characteristic'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('characteristic'))
df['model'] = list(map(lambda x, y: x if pd.notna(x) else y, df['model'], df['model2']))
print(df.info())

df['tag'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['tag']))
df['title'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['title']))
df['content'] = list(map(lambda x: x if pd.notna(x) and x != '' else np.nan, df['content']))

df.drop(['all_text', 'model2'], axis=1, inplace=True)
a = sql_test.dbconnect(host, username, password, database, port)
# df.to_excel('./shuijun.xlsx', encoding='utf-8')
a.insert_database(table_name='dim_meifu_0w20_bak_1206', data=df, if_exists='truncate')
# df.to_excel('./dataChoose_meifu_20221201.xlsx')
