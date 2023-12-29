import re
from aip import AipOcr
import pandas as pd
import PyPDF2
import numpy as np
import os
import pdfplumber
from defSet import generalDef
# from pdf2image import convert_from_path
import os.path
import re
import datetime
import pytesseract
import os
import fitz    # 这个就是PyMuPDF模块
# from aip import AipOcr
from PIL import Image
import difflib
import requests
import time
import cv2
import pinyin
from PIL import ImageEnhance

def osWalkFilePath(func):
    def wapper(df, file_path=''):
        i = 0
        # df = pd.DataFrame()
        for root, dirs, files in os.walk(file_path):
            for j in files:
                i += 1
                path = root + '/' + j
                # df.loc[i] = ['index', i]
                df['index'] = i
                strs = func(path)
                print(strs)
                # df.loc[(df['index'] == i), 'main'] = strs
                df['main'] = strs
        return df
    return wapper


# 读取pdf去除换行符
# @osWalkFilePath
def readDataFromPDF(file, if_split=False):

    pattern = re.compile('(?<=[\w、，])\n(?=\w)')
    pdfFileObj = open(file, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdfFileObj)
    if if_split:
        dic = {}
        for i in range(len(pdf_reader.pages)):
            try:
                dic[i] = pattern.sub('', pdf_reader.pages[i].extract_text())
            except:
                break
        return dic
    else:
        strs = ''
        for i in range(len(pdf_reader.pages)):
            # strs += pattern.sub('', pdf_reader.pages[i].extract_text())
            strs += pdf_reader.pages[i].extract_text()
        return strs


def readFormPdf(file):

    pattern = re.compile('(?<=[\w、，])\n(?=\w)')
    pdf = pdfplumber.open(file)
    data = []
    for i in range(len(pdf.pages)):
        for j in pdf.pages[i].extract_table():
            try:
                data_m = (pattern.sub('', ','.join(j)) if pattern.search(','.join(j))!=None else ','.join(j)).split(',')
                data.append(data_m)
            except:
                pass
    df = pd.DataFrame(data[1:], columns=data[0])
    df.drop_duplicates()
    return df


def mergeShiftAndNext(df, col='订单编号', merge_col='型号及配置描述'):

    df = generalDef.dropSpanData(df)
    df[merge_col] = list(map(lambda a, b, c, d: str(c) + str(d) if pd.notna(a) and (pd.isna(b) or b == '' or b == ' ') else c, df[col], df[col].shift(-1), df[merge_col], df[merge_col].shift(-1)))
    df.dropna(subset=[col])

    return df

def mergeShiftAndNextTest(df, col='订单编号', merge_col='型号及配置描述'):
    df = generalDef.dropSpanData(df)
    df[merge_col] = list(
        map(lambda a, b, c, d: str(c) + str(d) if pd.notna(a) and (pd.isna(b) or b == '' or b == ' ') else c, df[col], df['1'], df[merge_col],
            df['2']))
    df.dropna(subset=[col])

    return df

def readMainMethod(df, lis='', out_lis='main'):

    pattern = re.compile('(?<=[一二三四五六七八九十]\W).*?(?=\n)')
    df[out_lis] = list(
        map(lambda x: '\n'.join(pattern.findall(x)) if pd.notna(x) and pattern.search(x) != None else np.nan, df[lis]))

    return df


def readMainSonMethod(df, lis='', out_lis='main'):

    return df


def searchAAndB(df, lis=''):

    patternA = re.compile('甲[(（\w)）]*?[:：]+?[ ]*?(\w+)')
    patternB = re.compile('乙[(（\w)）]*?[:：]+?[ ]*?(\w+)')
    # df['A_Name'] = list(map(lambda x: ','.join(list(set(patternA.findall(x)))) if pd.notna(x) and patternA.search(
    #     x) != None else np.nan, df[lis]))
    # df['B_Name'] = list(map(lambda x: ','.join(list(set(patternB.findall(x)))) if pd.notna(x) and patternB.search(
    #     x) != None else np.nan, df[lis]))
    df['A_Name'] = list(map(lambda x: patternA.search(x).group() if pd.notna(x) and patternA.search(
        x) != None else np.nan, df[lis]))
    df['B_Name'] = list(map(lambda x: patternB.search(x).group() if pd.notna(x) and patternB.search(
        x) != None else np.nan, df[lis]))

    return df


def searchAAndBPhone(df, lis=''):

    pattern = re.compile('(?<=)[电话手机][\w ]+[:： ]*?[\d\- ]+')
    # df['APhone'] = list(map(lambda x, y: re.compile(x + '.*?' + '联系[\w ]+?[:：][ ]*?\d+').search(y).group() if pd.notna(y) and re.compile(x + '.*?' + '联系[\w ]+?[:：][ ]*?\d+').search(y)!=None else np.nan, df['AName'], df[lis]))
    # df['BPhone'] = list(map(lambda x, y: re.compile(x + '.*?' + '联系[\w ]+?[:：][ ]*?\d+').search(y).group() if pd.notna(y) and re.compile(x + '.*?' + '联系[\w ]+?[:：][ ]*?\d+').search(y)!=None else np.nan, df['BName'], df[lis]))
    df['APhone'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['BPhone'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df


def searchAAndBPiece(df, lis=''):

    pattern = re.compile('(?<=地址|住所|坐落)[:：][ ]*?[\w （）()]+')
    df['APiece'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['BPiece'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df

# 税务登记号
def searchAAndBTaxNumber(df, lis=''):

    pattern = re.compile('(?<=纳税人识别号)[:： ]*?[\da-zA-Z ]{15,20}|(?<=税务登记号)[:： ]*?[\da-zA-Z ]{15,20}')
    df['ATax'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['BTax'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df

# 银行账号
def searchAAndBBankNumber(df, lis=''):

    pattern = re.compile('[账号]+[:： ]*?[\d ]{15,20}')
    pattern1 = re.compile('[开户支付行]+[:： ]*?[\w ]+')
    df['ABank'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['ABankType'] = list(map(lambda x: pattern1.findall(x)[0] if pd.notna(x) and pattern1.search(x)!=None else np.nan, df[lis]))
    df['BBank'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['BBankType'] = list(map(lambda x: pattern1.findall(x)[1] if pd.notna(x) and pattern1.search(x)!=None else np.nan, df[lis]))

    return df

def hasConfidentiality(df, lis=''):

    pattern = re.compile('第*?[\d一二三四五六七八九十]+.*?保密[\w\n]*?')
    df['hasConfident'] = list(
        map(lambda x: 1 if pd.notna(x) and pattern.search(x) != None else 0, df[lis]))

    return df

def searchAAndBName(df, lis=''):

    pattern = re.compile('[联系人 委托]+?[:：;；]*?[ ]*?[(（]*?[\w ]+[)）]*?')
    df['AName'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))
    df['BName'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df


def searchAAndBMoney(df, lis=''):

    pattern = re.compile('(?<=支付|共计|金费)\w*?[每年月日]*?[$￥\d ,，\.]+元[\W每年月日]*?|(?<=服务费)\w*?[$￥每年月日]*?[\d ,，\.]+元[\W每年月日]*?')
    df['Money'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df

def searchAAndBData(df, lis=''):

    pattern = re.compile('[期限日]{2}\w*?[:：;；]*?[\d \\/年月日时分秒\- 到至\n]+')
    df['dateTime'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df

def searchAAndBCondition(df, lis=''):

    pattern = re.compile(r'[基于提供]{2}. +[服务]+?|购买')
    df['condition'] = list(map(lambda x: ','.join(list(set(pattern.findall(x)))) if pd.notna(x) and pattern.search(x)!=None else np.nan, df[lis]))

    return df

def searchAAndBResponsibility(df, lis=''):

    patternA = re.compile('[^。]+?甲方[应需][^。]+?(?=。)|[^。]+?甲方保证[^。]+?(?=。)')
    patternB = re.compile('[^。]+?乙方[应需][^。]+?(?=。)|[^。]+?乙方保证[^。]+?(?=。)')
    df['AResponsibility'] = list(map(lambda x: '\n'.join([re.sub('\n', '', i) for i in list(set(patternA.findall(x)))]) if pd.notna(x) and patternA.search(x)!=None else np.nan, df[lis]))
    df['BResponsibility'] = list(map(lambda x: '\n'.join([re.sub('\n', '', i) for i in list(set(patternB.findall(x)))]) if pd.notna(x) and patternB.search(x)!=None else np.nan, df[lis]))

    patternABBreach = re.compile('[^\n]+违约[^\n]+?(?=\n)')

    df['ABreach'] = list(map(lambda x: '\n'.join([re.sub('\n', '', i) for i in list(set(patternABBreach.findall(x)))]) if pd.notna(x) and patternABBreach.search(x)!=None else np.nan, df['AResponsibility']))
    df['BBreach'] = list(map(lambda x: '\n'.join([re.sub('\n', '', i) for i in list(set(patternABBreach.findall(x)))]) if pd.notna(x) and patternABBreach.search(x)!=None else np.nan, df['BResponsibility']))
    df['AResponsibility'] = list(map(lambda x: '\n'.join(i for i in x.split('\n') if i != '') if pd.notna(x) and patternABBreach.search(x)!=None else x, df['AResponsibility']))
    df['BResponsibility'] = list(map(lambda x: '\n'.join(i for i in x.split('\n') if i != '') if pd.notna(x) and patternABBreach.search(x)!=None else x, df['BResponsibility']))
    # df['']
    # patternBBreach = re.compile('[^\n]+违约[^\n]+')



    return df

def knowsARegulation(df, lis='', out_lis='knowsA'):

    pattern = re.compile('(?<=甲方\*\?应).*?(?=[。])')
    df[out_lis] = list(
        map(lambda x: '\n'.join(pattern.findall(x)) if pd.notna(x) and pattern.search(x) != None else np.nan, df[lis]))

    return df


def knowsBRegulation(df, lis='', out_lis='knowsB'):
    pattern = re.compile('(?<=乙方\*\?应).*?(?=[。])')
    df[out_lis] = list(
        map(lambda x: '\n'.join(pattern.findall(x)) if pd.notna(x) and pattern.search(x) != None else np.nan, df[lis]))

    return df


# def searchDate(df, lis='', out_lis='dateTime'):
#
#     pattern = re.compile('(?<=日期\w\*\?[:： ]\+)[\d年月日]+')
#     df[out_lis] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(
#         x) != None else np.nan, df[lis]))
#
#     return df

def data_clean(text):

    # 清洗excel中的非法字符，都是不常见的不可显示字符，例如退格，响铃等
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)

    return text

def makeANdReadDir(func):
    def inner(path):
        pattern = re.compile('^.*?(?=\.\w)')
        for parent, dirnames, file in os.walk(path):
            print(file)
            for j in file:
                os.makedirs(path + '/' + pattern.search(j).group())
                func(path=path + '/' + pattern.search(j).group(), pic_path=path + '/' + file)
        return inner()

def data_clean(text):

    # 清洗excel中的非法字符，都是不常见的不可显示字符，例如退格，响铃等
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
    return text

def sameDif(df, lis_dif=['dateTime']):
    lis = []
    for i in df.columns:
        if i == 'main':
            pass
        elif i in lis_dif:
            if str(df[i].to_list()[0]) == str(df[i].to_list()[1]):
                pass
            else:
                lis.append(i)
        else:
            if difflib.SequenceMatcher(None, str(df[i].to_list()[0]), str(df[i].to_list()[1])).ratio() < 0.55:
                lis.append(i)
    df = df[lis]
    return df

# @makeANdReadDir
def pdf2image2(path, pic_path):

    f = open('result.txt', 'w', encoding='utf-8')
    checkIM = r'/Subtype(?= */Image)'
    pdf = fitz.open(path)
    lenXREF = pdf.xref_length()
    count = 1
    for i in range(1, lenXREF):
        text = pdf.xref_object(i)
        isImage = re.search(checkIM, text)
        if not isImage:
            continue
        pix = fitz.Pixmap(pdf, i)
        if pix.size < 10000:
            continue
        new_name = f'img_{count}.png'
        pix.save(os.path.join(pic_path, new_name))
        count += 1
        pix = None
    strings = ''
    for root, dirs, files in os.walk(pic_path):
        for img in files:
            print(pic_path + '/' + img)
            im = Image.open(pic_path + '/' + img)
            # 图片二值化
            Img = im.convert('L')

            threshold = 200
            table = []
            for i in range(256):
                if i < threshold:
                    table.append(0)
                else:
                    table.append(1)

            photo = Img.point(table, '1')
            strings += pytesseract.image_to_string(photo, lang='chi_sim')
            strings = data_clean(strings)



            # print(strings)
    df = pd.DataFrame([[strings]], columns=['main'])
    return df


def useBaiduAip(path, APP_ID='30038818', API_KEY='fFt80P5GdYMXUQUKSCc9ttku',
                SECRET_KEY='GR4lxAaLiYTIiuNBa9tftUwZRS20VLOs'):
    # APP_ID = '30038818'
    # API_KEY = 'fFt80P5GdYMXUQUKSCc9ttku'
    # SECRET_KEY = 'GR4lxAaLiYTIiuNBa9tftUwZRS20VLOs'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(path)
    # print(image)
    client.basicGeneral(image)
    options = dict()
    options["detect_direction"] = "false"
    options["probability"] = "true"
    options["language_type"] = "ENG"
    # 带参数调用通用文字识别（高精度版） """
    data_ocr = client.basicAccurate(image, options)
    # print(data_ocr)
    strings = ''
    for i in data_ocr['words_result']:
        data_ocr = i["words"].replace(" ", "") if i else list()
        strings = strings + '\n' + data_ocr
    return strings

def grayScaleImage(path, img_path):
    # img_final
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    binary = cv2.adaptiveThreshold(image, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 15)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    se = cv2.morphologyEx(se, cv2.MORPH_CLOSE, (2, 2))
    mask = cv2.dilate(binary, se)
    mask1 = cv2.bitwise_not(mask)
    binary = cv2.bitwise_and(image, mask)
    result = cv2.add(binary, mask1)
    cv2.imwrite(img_path, result)

# 获取文件夹中所有图片
def get_image(image_path):
    images = []  # 存储文件夹内所有文件的路径（包括子目录内的文件）
    for root, dirs, files in os.walk(image_path):
        path = [os.path.join(root, name) for name in files]
        images.extend(path)
    return images

def Image_Excel(images, image_path, APP_ID='30038818', API_KEY='fFt80P5GdYMXUQUKSCc9ttku',
                SECRET_KEY='GR4lxAaLiYTIiuNBa9tftUwZRS20VLOs'):
    #  调用百度AI接口
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 循环遍历文件家中图片
    # images = get_image(image_path)
    df_count = 0
    dic = {}
    for image in images:
        # 以二进制方式打开图片
        img_open = open(image, 'rb')
        # 读取图片
        img_read = img_open.read()
        # 调用表格识别模块识别图片
        table = client.tableRecognitionAsync(img_read)
        # 获取请求ID
        try:
            request_id = table['result'][0]['request_id']
        except:
            continue
        # 获取表格处理结果
        result = client.getTableRecognitionResult(request_id)
        # 处理状态是“已完成”，获取下载地址
        while result['result']['ret_msg'] != '已完成':
            time.sleep(2)  # 暂停2秒再刷新
            result = client.getTableRecognitionResult(request_id)
        # print(result)
        download_url = result['result']['result_data']
        # print(download_url)
        # 获取表格数据
        excel_data = requests.get(download_url)
        # print(excel_data)
        # print(type(excel_data))
        # # 根据图片名字命名表格名称
        xlsx_name = image.split(".")[0] + ".xlsx"
        xlsx = open(xlsx_name, 'wb')
        # 将数据写入excel文件并保存
        xlsx.write(excel_data.content)
        xlsx.write(excel_data.content)
        # 新建excel文件
        df = pd.read_excel(xlsx_name)
        if len(df) > 0:
            dic['{a}_{b}'.format(a=image_path, b=df_count)] = df.to_dict()
            # dic = df.to_dict('list')
            df_count += 1
    return dic


def pdf2image(path, pic_path):
    pattern = re.compile('\w+$')
    sheet_name = pattern.search(pic_path).group()
    # 根据拼音第一个字母创建文件夹，后续函数包不识别中文问题
    try:
        os.makedirs(pic_path)
    except:
        print('aaaaaaaa')
    # 日志（未用到）
    f = open('result.txt', 'w', encoding='utf-8')
    checkIM = r'/Subtype(?= */Image)'
    # 读取pdf
    pdf = fitz.open(path)
    lenXREF = pdf.xref_length()
    count = 1
    # 遍历pdf页数转换图片储存
    for i in range(1, lenXREF):
        text = pdf.xref_object(i)
        isImage = re.search(checkIM, text)
        if not isImage:
            continue
        pix = fitz.Pixmap(pdf, i)
        if pix.size < 10000:
            continue
        new_name = f'img_{count}.png'
        pix.save(os.path.join(pic_path, new_name))
        count += 1
        pix = None
    strings = ''
    images = []
    # 读取图片内容
    for root, dirs, files in os.walk(pic_path):

        for img in files:
            # im = Image.open(pic_path + '/' + img)
            print(pic_path + '/' + img)
            pattern = re.compile('(?<=Orientation in degrees: )[\d.]+')
            try:
                # 检测图片方向
                x = pattern.search(pytesseract.image_to_osd(pic_path + '/' + img)).group()
                print(x)
                # 如图片旋转，将图片转正
                if x != '0':
                    imge = eval("Image.open(pic_path + '/' + img).transpose(Image.ROTATE_{})".format(x))
                    img_final = np.array(imge)
                    # print(type(imge))

                    # imge.save(pic_path + '/' + img)
                    # imgglo = cv2.imread(pic_path + '/' + img)
                    # gray = cv2.cvtColor(imgglo, cv2.COLOR_BGR2GRAY)
                    # Image_Inversed = cv2.bitwise_not(gray)
                    # cv2.threshold(Image_Inversed, 10, 255, cv2.THRESH_BINARY_INV)
                    # img_final = np.array(Image_Inversed)
                    #
                    # mask = Image.fromarray(np.uint8(img_final))
                    # mask.save(pic_path + '/' + img)

                    imge.save(pic_path + '/' + img)
                    grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)
                    grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)

                strings += useBaiduAip(pic_path + '/' + img)
                strings = data_clean(strings)
                # print(strings)
            except:
                print('疑似空白图片')
                continue
        path = [os.path.join(root, name) for name in files]
        print(path)

        images.extend(path)
    print(images)

    dic = Image_Excel(images, image_path=sheet_name)
    print('---------------dic------------------', dic)
    df = pd.DataFrame([[strings]], columns=['main'])
    return dic, df


