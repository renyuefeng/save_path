# https://blog.csdn.net/weixin_46275180/article/details/116247288
# import jieba
# import pandas as pd
# import jieba.posseg as pseg
#
# path = '../../Meifu/weibo_hws_0914.jpg.csv'
#
# df = pd.read_csv(path, header=None)
#
# df.rename(columns={0: 'word', 1: 'percent'}, inplace=True)
# print(df.info())
#
# jieba.enable_paddle()

import jieba
import jieba.posseg as pseg
import pandas as pd

import sql_test

path = '../../Meifu/result_0914.xlsx'

df = pd.read_excel(path, sheet_name='content')
# df = df.loc[df['url_link']=='https://m.weibo.cn/detail/4942543885960403']

lis_mid = df['content'].values.tolist()
print('------')
string = ''
for i in lis_mid:
    try:
        if i is not None:
            string = string + str(i)
    except:
        print(i)

jieba.add_word('岸田文雄')
jieba.add_word('岸田')
jieba.add_word('核废水')
jieba.add_word('核污水')
jieba.add_word('核污染水')
jieba.add_word('日本人')
jieba.add_word('北赤道')
jieba.add_word('日本国')
jieba.add_word('日本岛')
jieba.add_word('侵华战争')
jieba.add_word('火速围观')
jieba.add_word('美丽国')
jieba.add_word('漂亮国')
jieba.add_word('嘴炮')
jieba.add_word('小日本')
jieba.add_word('全世界人')

words = pseg.cut(string)
print(type(words))
# print('jieba默认模式')
word_lis = []
for word, flag in words:
    if flag in ['ng', 'n', 'nr', 'ns', 'nt', 'nz'] and len(word) > 1:
        word_lis.append('%s %s' % (word, flag))
#         print('%s %s' % (word, flag))
# print(list(set(word_lis)))
with open('./日本排海.txt', mode='w') as f:
    for i in list(set(word_lis)):
        f.write(i)
        f.write('\n')

# print('+' * 10)
# # jieba.enable_paddle()  # 启动paddle模式。
# words = pseg.cut("我关注了微信公众号数据STUDIO", use_paddle=True)  # paddle模式
# print('paddle模式')
# for word, flag in words:
#     print('%s %s' % (word, flag))
# print('+' * 10)

