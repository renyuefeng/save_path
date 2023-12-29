import difflib
import io
import re
import PyPDF2
import pandas as pd
import os
import fitz  # 这个就是PyMuPDF模块
import pytesseract
import cv2  # opencv-python
from aip import AipOcr
import numpy as np
import time
import requests
import shutil
import webbrowser


# import pdfplumber


def pd_output_str(func: object) -> object:
    def innfunc(lis_name, *args, **kwargs):
        df = func(*args, **kwargs)
        strings = eval('df.{a}.to_list()[0]'.format(a=lis_name))
        return strings

    return innfunc


def data_clean(text):
    # 清洗excel中的非法字符，都是不常见的不可显示字符，例如退格，响铃等
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    text = ILLEGAL_CHARACTERS_RE.sub(r'', text)

    return text


def clean_data(df, col='', pattern_str='', method='search'):
    pattern_search = re.compile('(?<=[:： \n]){}+'.format(pattern_str))
    pattern_sub = re.compile('[^{}]+'.format(pattern_str))
    if isinstance(df, str):
        if method == 'search':
            df = pattern_search.search(df).group()
        elif method == 'sub':
            df = pattern_sub.sub('', df)
    else:
        if method == 'search':
            df[col] = list(map(lambda x: pattern_search.search(x).group() if pd.notna(x) and pattern_search.search(
                x) != None else x, df[col]))
        elif method == 'sub':
            df[col] = list(
                map(lambda x: pattern_sub.sub('', x) if pd.notna(x) and pattern_sub.search(x) != None else x, df[col]))
    return df


class baiduAipConnect:
    """docstring for ClassName"""

    def __init__(self):
        self.APP_ID = '30038818'
        self.API_KEY = 'fFt80P5GdYMXUQUKSCc9ttku'
        self.SECRET_KEY = 'GR4lxAaLiYTIiuNBa9tftUwZRS20VLOs'
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.options = dict()
        self.options["detect_direction"] = "false"
        self.options["probability"] = "true"
        self.options["language_type"] = "ENG"

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def useBaiduAip(self, path):
        image = self.get_file_content(path)
        # 带参数调用通用文字识别（高精度版） """
        data_ocr = self.client.basicAccurate(image, self.options)
        strings = ''
        for i in data_ocr['words_result']:
            data_ocr = i["words"].replace(" ", "") if i else list()
            strings = strings + '\n' + data_ocr
        return strings

    def Image_Excel(self, images, image_path):
        # df_count = 0
        # dic = {}
        df_out = pd.DataFrame()
        for image in images:

            start_time = time.time()

            # 以二进制方式打开图片
            img_open = open(image, 'rb')
            # 读取图片
            img_read = img_open.read()
            # 调用表格识别模块识别图片
            table = self.client.tableRecognitionAsync(img_read)

            end_time = time.time()
            print(start_time - end_time, '调用表格识别模块识别图片读取文件表格抽取信息: %.6f' % (end_time - start_time))

            # table = self.client.form(img_read)
            # table = self.client.table(img_read)
            # print(table)
            # 获取请求ID
            try:
                request_id = table['result'][0]['request_id']
                print(request_id)
            except:
                continue
            # 获取表格处理结果
            start_time = time.time()

            result = self.client.getTableRecognitionResult(request_id)

            # 处理状态是“已完成”，获取下载地址
            while result['result']['ret_msg'] != '已完成':
                time.sleep(2)  # 暂停2秒再刷新
                result = self.client.getTableRecognitionResult(request_id)
            # print('result', result)



            download_url = result['result']['result_data']
            # webbrow = webbrowser.open(download_url)
            # print(webbrow)
            # df = pd.read_html(download_url, encoding='utf-8')
            # df = pd.read_html(download_url, encoding="GB2312")
            # df = pd.read_html(download_url, encoding="GB18030")
            # print(df, type(df))
            # 获取表格数据
            excel_data = requests.get(download_url)
            # print(io.BytesIO(excel_data.content))
            df = pd.io.excel.read_excel(io.BytesIO(excel_data.content))
            end_time = time.time()
            print(start_time - end_time, '从网上请求地址下载图片信息: %.6f' % (end_time - start_time))
            df_out = pd.concat([df_out, df])
            # print(df.info())
            # print(type(excel_data))
            # print(excel_data['data'])
            # print(excel_data.text)

            # response = requests.post(url, data=multipart_encoder, headers=headers).json()
            # print(response)
            # print(pd.read_csv(StringIO(response['data']), sep =','))

            # # 根据图片名字命名表格名称
            # xlsx_name = image.split(".")[0] + ".xlsx"
            # xlsx = open(xlsx_name, 'wb')
            # 将数据写入excel文件并保存
            # xlsx.write(excel_data.content)
            # xlsx.write(excel_data.content)
            # 新建excel文件
            # df = pd.read_excel(xlsx_name)
            # print(df.info())

            # if len(df) > 0:
            #     dic['{a}_{b}'.format(a=image_path, b=df_count)] = df.to_dict('list')
            #     df_count += 1
        start_time = time.time()

        df_out = df_out.dropna(thresh=int(0.25*len(df_out.columns)))

        end_time = time.time()
        print(start_time - end_time, '数据清洗: %.6f' % (end_time - start_time))

        return df_out
        # return dic


# 读取pdf去除换行符
# @osWalkFilePath
def readDataFromPDF(file, if_split=False):
    pattern = re.compile('(?<=[\w、，])\n(?=\w)')
    # pdfFileObj = open(file, 'rb')
    # pdf_reader = PyPDF2.PdfReader(pdfFileObj)
    pdf_reader = PyPDF2.PdfReader(file)
    if if_split:
        dic = {}
        for i in range(len(pdf_reader.pages)):
            try:
                dic[i] = pattern.sub('', pdf_reader.pages[i].extract_text())
            except:
                break
        return dic
    else:
        # print('no split')
        strs = ''
        for i in range(len(pdf_reader.pages)):
            strs += pdf_reader.pages[i].extract_text()
        return strs


# def readFormPdf(file):
#
#     pattern = re.compile('(?<=[\w、，])\n(?=\w)')
#     pdf = pdfplumber.open(file)
#     print('pdf.pages', pdf.pages)
#     data = []
#     for i in range(len(pdf.pages)):
#         for j in pdf.pages[i].extract_table():
#             try:
#                 data_m = (pattern.sub('', ','.join(j)) if pattern.search(','.join(j))!=None else ','.join(j)).split(',')
#                 data.append(data_m)
#             except:
#                 pass
#     df = pd.DataFrame(data[1:], columns=data[0])
#     df.drop_duplicates()
#     print('form_df', df.info())
#     return df

def pdf2image(path, pic_path):
    pattern = re.compile('\w+$')

    # start_time = time.time()

    sheet_name = pattern.search(pic_path).group()
    # 根据拼音第一个字母创建文件夹，后续函数包不识别中文问题
    if os.path.exists(pic_path):
        # try:
        shutil.rmtree(pic_path)
        os.makedirs(pic_path)
            # print('rmtree')
        # except:
        #     print('aaaaaaaa')
    else:
        # print('makedirs')
        os.makedirs(pic_path)
    # end_time = time.time()
    # print(start_time - end_time, '创建/清空文件夹: %.6f' % (end_time - start_time))
    checkIM = r'/Subtype(?= */Image)'

    # start_time = time.time()

    # 读取pdf
    pdf = fitz.open(path)

    # 未测试
    ## 调整分辨率与方向
    # rotate = int(0)
    # zoom_x = 2
    # zoom_y = 2
    # mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
    # print(mat)
    # pix = pa

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

    # end_time = time.time()
    # print(start_time - end_time, '储存图片: %.6f' % (end_time - start_time))

    strings = ''
    images = []
    # 读取图片内容
    # start_time = time.time()

    img_excel = baiduAipConnect()
    for root, dirs, files in os.walk(pic_path):

        for img in files:
            # pattern = re.compile('(?<=Orientation in degrees: )[\d.]+')
            # if pattern.search(pytesseract.image_to_osd(pic_path + '/' + img)) != None:
            # try:
            #     x = pattern.search(pytesseract.image_to_osd(pic_path + '/' + img)).group()
            #     if x != '0':
            #         imge = eval("Image.open(pic_path + '/' + img).transpose(Image.ROTATE_{})".format(x))
            #         # print('b')
            #         img_final = np.array(imge)
            #         # print('c')
            #         imge.save(pic_path + '/' + img)
            #         # print('d')
            #         grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)
            #         # grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)
            # except:
            #     continue
            # print('a')

            # end_time = time.time()
            # print(start_time - end_time, '旋转图片: %.6f' % (end_time - start_time))

            # 如图片旋转，将图片转正
            # strings += useBaiduAip(pic_path + '/' + img)
            # start_time = time.time()

            strings += img_excel.useBaiduAip(pic_path + '/' + img)
            strings = data_clean(strings)

            # end_time = time.time()
            # print(start_time - end_time, '读取图片文字: %.6f' % (end_time - start_time))
            # try:
            #     # 检测图片方向
            #     x = pattern.search(pytesseract.image_to_osd(pic_path + '/' + img)).group()
            #     print('a')
            #
            #     # 如图片旋转，将图片转正
            #     if x != '0':
            #         imge = eval("Image.open(pic_path + '/' + img).transpose(Image.ROTATE_{})".format(x))
            #         print('b')
            #         img_final = np.array(imge)
            #         print('c')
            #         imge.save(pic_path + '/' + img)
            #         print('d')
            #         grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)
            #         grayScaleImage(path=pic_path + '/' + img, img_path=pic_path + '/' + img)
            #
            #     # strings += useBaiduAip(pic_path + '/' + img)
            #     strings += img_excel.useBaiduAip(pic_path + '/' + img)
            #     strings = data_clean(strings)
            # except:
            #     print('疑似空白图片')
            #     continue
        path = [os.path.join(root, name) for name in files]
        images.extend(path)
    # start_time = time.time()

    # dic = img_excel.Image_Excel(images, image_path=sheet_name)
    dic = {
        '产品名称': ['接线端子', '接线端子', '双层接线端子', '接线端子'],
        '规格型号': ['HABH76202500K', 'HABH76202500K', 'HAEH50808500K', 'HAEH50808500K'],
        '单位': ['PCS', 'PCS', 'PCS', 'PCS'],
        '数量': ['1000.0', '1000.0', '4000.0', '8000.0'],
        '单价（元）': ['0.49', '1.29', '2.94', '1.76'],
        '总额（元）': ['490.0', '1290.0', '11760.0', '14080.0']
    }
    df = pd.DataFrame(data=dic)
    # print('dic', dic)
    # dic = {'': }

    # end_time = time.time()
    # print(start_time - end_time, '读取图片中表格: %.6f' % (end_time - start_time))
    # df = pd.DataFrame([[strings]], columns=['main'])
    # return dic, df
    return df, strings


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

# def useBaiduAip(path, APP_ID='30038818', API_KEY='fFt80P5GdYMXUQUKSCc9ttku',
#                 SECRET_KEY='GR4lxAaLiYTIiuNBa9tftUwZRS20VLOs'):
#     client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#
#     def get_file_content(filePath):
#         with open(filePath, 'rb') as fp:
#             return fp.read()
#
#     image = get_file_content(path)
#     client.basicGeneral(image)
#     options = dict()
#     options["detect_direction"] = "false"
#     options["probability"] = "true"
#     options["language_type"] = "ENG"
#     # 带参数调用通用文字识别（高精度版） """
#     data_ocr = client.basicAccurate(image, options)
#     strings = ''
#     for i in data_ocr['words_result']:
#         data_ocr = i["words"].replace(" ", "") if i else list()
#         strings = strings + '\n' + data_ocr
#     return strings
