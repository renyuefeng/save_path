# -*- coding: utf-8 -*-

from jieba.analyse import *
import jieba
import os, re
from Meifu import text_abstract
import matplotlib.pyplot as plt
import openpyxl
from wordcloud import WordCloud
import pandas

def get_keywords_a(text,path2):
    # path = os.getcwd() + '\\' + 'stopwords-master\hit_stopwords.txt'
    # print(path)
    # set_stop_words(path)
    set_stop_words('./stopwords-master/hit_stopwords.txt')
    jieba.load_userdict("./stopwords-master/ew_words.txt")

    # path3 = os.getcwd() + '\\' + 'stopwords-master\\new_words.csv'
    # pd = pandas.read_csv(path3, encoding='utf-8')
    # pd = pandas.read_csv('D:\Python\Project\Meifu\Meifu\stopwords-master\new_words.csv', encoding='utf-8')
    # print(pd)
    # lines = pd.shape[0]
    # for i in range(lines):
    #     jieba.add_word(pd['name'][i], tag=pd['tag'][i])
        # print(pd['name'][i])
    jieba.add_word('金美孚', tag='n')
    jieba.add_word('美孚一号', tag='n')
    jieba.add_word('美孚1号', tag='n')
    jieba.add_word('金美孚一号', tag='n')
    jieba.add_word('爱车一族', tag='n')
    jieba.add_word('爱车', tag='n')
    jieba.add_word('做保养', tag='v')
    jieba.add_word('坑爹', tag='a')
    jieba.add_word('合成机油', tag='n')
    jieba.add_word('半合成机油', tag='n')
    jieba.add_word('矿物油', tag='n')
    jieba.add_word('合成科技', tag='n')
    jieba.add_word('合成技术', tag='n')
    jieba.add_word('合成技术油', tag='n')
    jieba.add_word('上上之选', tag='a')
    jieba.add_word('4S店', tag='a')
    jieba.add_word('三桶油', tag='a')
    jieba.add_word('4S', tag='n')
    jieba.add_word('超凡喜力', tag='n')
    jieba.add_word('极护', tag='n')
    jieba.add_word('涡轮增压', tag='n')
    jieba.add_word('道达尔', tag='n')
    jieba.add_word('力魔', tag='n')
    jieba.add_word('龙蟠', tag='n')
    jieba.add_word('四儿子', tag='n')
    jieba.add_word('苏宁易购', tag='n')
    jieba.add_word('途虎', tag='n')
    jieba.add_word('明锐', tag='n')
    # print(path)
    text = re.sub(r"美孚1号","美孚一号",text)
    text = re.sub(r"18000公里","一万八千公里",text)
    text = re.sub(r"一万八公里","一万八千公里",text)
    text = re.sub(r"5000公里","五千公里",text)
    text = re.sub(r"4儿子","4S",text)
    text = re.sub(r"4S","四儿子",text)
    text = re.sub(r"4s","四儿子",text)
    text = re.sub(r"妹夫","美孚",text)
    text = re.sub(r"狗东","京东",text)
    text = re.sub(r"5000","五千",text)
    text = re.sub(r"10000","一万",text)
    text = re.sub(r"18000","一万八千",text)
    text = re.sub(r"金美孚","金美",text)
    # text = re.sub(r"1号","一号",text)
    text = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+", ",", text)  # 替换标点符号
    # print(text)
    import jieba.posseg as pseg
    word = pseg.cut(text)
    words = []
    f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\正面情感词语（中文）.txt', 'r', encoding='utf-8')
    for i in f.readlines():
        words.append(i.strip('\n'))
    f.close()
    print('words',words)
    f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\正面评价词语（中文）.txt', 'r', encoding='utf-8')
    for i in f.readlines():
        words.append(i.strip('\n'))
    f.close()
    print('words',words)
    f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\负面情感词语（中文）.txt', 'r', encoding='utf-8')
    for i in f.readlines():
        words.append(i.strip('\n'))
    f.close()
    print('words',words)
    f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\负面评价词语（中文）.txt', 'r', encoding='utf-8')
    for i in f.readlines():
        words.append(i.strip('\n'))
    f.close()
    print('words',words)


    # for w in word:
    #     if w.flag[0] == 'a':
    #         words.append(w.word)
    # print(words)

    # f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\key_words.txt', 'w', encoding='utf-8')
    # for w in word:
    #     if w.flag[0] == 'n':
    #         words.append(w.word)
    #         print(w.word, w.flag)
    # keywords = extract_tags(text, topK=600,withWeight=True)
    # for keyword, weight in extract_tags(text, topK=600, withWeight=True):
    #     if keyword in words:
    #         print(keyword, weight)
    #         f.write(keyword + '\n')
    # f.close()
    # f = open('D:\Python\Project\Meifu\Meifu\stopwords-master\key_words2.txt', 'r', encoding='utf-8')
    # for i in f.readlines():
    #     words.append(i.strip('\n'))
    # f.close()
    # print('words',words)
    #
    # keywords = extract_tags(text, topK=60,withWeight=True)
    # for keyword, weight in extract_tags(text, topK=60, withWeight=True):
    #     if keyword in words:
    #         print(keyword, weight)

    keywords = extract_tags(text, topK=2000,withWeight=True)

    # for keyword, weight in extract_tags(text, topK=100, withWeight=True):
    #     print(keyword, weight)

    # print(keywords)
    ret_words = {}
    for word in keywords:
        if word[0] in words:
            # print(word)
            ret_words[word[0]] = word[1]
    print(ret_words)
    generate_word_cloud(ret_words,path2)
    return keywords

# 4.生成词云图并保存
def generate_word_cloud(dict, path):
    # color_mask = imread('./background.jpg')
    cloud = WordCloud(
        # 设置字体，不指定就会出现乱码，文件名不支持中文
        # font_path="C:/Windows/Fonts/simkai.ttf",
        font_path="C:/Windows/Fonts/simsun.ttc",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色，默认为黑，可根据需要自定义为颜色
        background_color='white',
        # 清晰度
        scale=16,
        # 词云形状，
        # mask=color_mask,
        # 允许最大词汇
        max_words=400,
        # 最大号字体，如果不指定则为图像高度
        max_font_size=150,
        # 画布宽度和高度，如果设置了mask则不会生效
        # width=200,
        # height=200,
        # 词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1
        prefer_horizontal=0.8
    )
    cloud.generate_from_frequencies(frequencies=dict)
    print(path)
    cloud.to_file(path)
    # # plt.imshow(cloud)
    # # 不现实坐标轴
    # plt.axis('off')
    # # 绘制词云
    # plt.figure(dpi = 600)
    # # image_colors = ImageColorGenerator(color_mask)
    # # # 重新上色
    # # plt.imshow(cloud.recolor(color_func=image_colors))
    # # 保存图片
    # plt.savefig('./result2.png')
    # plt.show()

if __name__ == '__main__':
    txt= '十八大以来的五年，4s是党和国家发展进程中极不平凡的五年。面对世界经济复苏乏力、局部冲突和动荡频发、全球性问题加剧的外部环境，面对我国经济发展进入新常态等一系列深刻变化，我们坚持稳中求进工作总基调，迎难而上，开拓进取，取得了改革开放和社会主义现代化建设的历史性成就。'
    # txt, sentences = text_abstract.get_text('汽车之家 跟帖 美孚.xlsx')
    get_keywords_a(txt, '1234.jpg')
    #
    # print('----')
    #
    # txt, sentences = text_abstract.get_text('汽车之家 跟帖 嘉实多.xlsx')
    # get_keywords(txt, 'Castrol.jpg')
    #
    # print('----')
    #
    # txt, sentences = text_abstract.get_text('汽车之家 跟帖 壳牌.xlsx')
    # get_keywords(txt, 'Shell.jpg')

