import json
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import re
from home.fieldExtract import dealContractMessage
from home.models import PurchaseContractTime, PurchaseContract
from home.pdfMethod import readDataFromPDF, pdf2image
from smart_contract_manager.settings import MEDIA_ROOT
from pycorrector.macbert.macbert_corrector import MacBertCorrector
import tabula
import pandas as pd

# @require_http_methods(['POST'])
# def word_examine(request):
#
#     nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct
#     # fid = request.body
#     fid = request.POST
#     print(request.POST)
#     # print(fid)
#     # fid = json.loads(fid)
#     fid = int(fid['fid'])
#     main_constract = PurchaseContractTime.objects.get(id=fid)
#     file_path = main_constract.file_path
#     strings = readDataFromPDF(file_path)
#     # print(strings_original)
#     if strings == 0 or strings == '' or strings == ' ':
#         dic1, strings = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=file_path),
#                                   pic_path='{}/pic'.format(MEDIA_ROOT))
#
#     # print(strings)
#     response = FileResponse(file_path)

    #
    # return JsonResponse(strings, safe=False)


@require_http_methods(['POST'])
def word_examine(request):

    # nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct
    nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese/pytorch_model.bin").macbert_correct
    info = {}
    dic = {}
    # fid = request.POST
    fid = request.body
    fid = json.loads(fid)
    fid = int(fid['fid'])

    main_constract = PurchaseContractTime.objects.get(id=fid)
    file_path = main_constract.file_path

    # pages = tabula.read_pdf(file_path, pages='all')
    # df = pd.concat(pages)

    strings = readDataFromPDF(file_path)
    # print(strings_original)
    if strings == 0 or strings == '' or strings == ' ':
        dic1, strings = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=file_path),
                                  pic_path='{}/pic'.format(MEDIA_ROOT))
    # print(dic1)
    # print(strings)
    text_new, details = nlp(strings)
    # print(details)
    lis = []
    for i in details:
        print(i)
        lis_mid = []
        lis_mid.append(i[0])
        lis_mid.append(i[1])
        lis.append(lis_mid)

    print(type(details))
    return JsonResponse(lis, safe=False)


# 主页详情信息 + 搜索
@require_http_methods(['POST'])
def show_examine_message(requeset):
    pattern = re.compile('\.pdf$')
    lis = []
    # 加载
    # file_dir = list(PurchaseContract.objects.all().values('id', 'contract_number', 'first_party', 'second_party', 'sole_id'))
    # file_dir = list(PurchaseContractTime.objects.all().values('id', 'upload_time', 'contract_number', 'first_party', 'second_party', 'sole_id'))
    pur_obj = PurchaseContract.objects.all().order_by('-sole_id_id')
    # .values('contract_number', 'first_party', 'second_party', 'sole_id')
    for i in pur_obj:
        file_dir = {}
        file_dir['contract_number'] = i.contract_number
        # file_dir['first_party'] = i.first_party
        # file_dir['second_party'] = i.second_party
        file_dir['sole_id'] = i.sole_id.id
        file_dir['id'] = i.id
        file_dir['update_time'] = i.sole_id.upload_time.strftime('%Y-%m-%d')
        file_dir['file_name'] = pattern.sub('', i.sole_id.file_name)
        lis.append(file_dir)
    file_dir = lis
    print('file_dir', file_dir)
    # 搜索
    # data = requeset.GET
    data = requeset.body
    data = json.loads(data)
    print('data', data)
    if data:
        pattern = re.compile('^ +| +$')
        file_dir = []
        # if requeset.body.contract_number:
        # contract_number = data.get('contract_number', '')
        contract_number = pattern.sub('', data['contract_number']) if 'contract_number' in data else None
        # file_name = data.get('file_name', '')
        file_name = pattern.sub('', data['file_name']) if 'file_name' in data else None
        # first_party = data.get('first_party', '')
        # second_party = data.get('second_party', '')
        # starttime = data.get('update_time[0]', '')
        if 'update_time' in data:
            starttime = data['update_time']['0'] if '0' in data['update_time'] else None
            # endtime = data.get('update_time[1]', '')
            endtime = data['update_time']['1'] if '1' in data['update_time'] else None
        else:
            starttime = None
            endtime = None
        # print(update_time)
        sql = 'SELECT * from((SELECT upload_time, id, file_name from purchase_contract_time) A LEFT JOIN(SELECT contract_number, sole_id_id from purchase_contract) B ON A.id=B.sole_id_id)'
        # sql = 'SELECT upload_time, contract_number, id, file_name from purchase_contract_time'
        if contract_number or file_name or starttime or endtime:
            sql = sql + ' where '
            if contract_number:
                sql = sql + 'contract_number like "%%{}%%" and '.format(contract_number)
            if file_name:
                sql = sql + 'file_name like "%%{}%%" and '.format(file_name)
            if starttime and endtime:
                sql = sql + 'upload_time between "{a} 00:00:00" and "{b} 23:59:59" and '.format(a=starttime, b=endtime)
        pattern = re.compile(' *and *$')
        sql = pattern.sub('', sql)
        sql = sql + ' ORDER BY A.upload_time desc'
        print(sql)
        # file_dir_all = PurchaseContract.objects.raw('select id, contract_number, first_party, second_party, sole_id_id from purchase_contract where contract_number like "%%{a}%%" and first_party like "%%{b}%%" and second_party like "%%{c}%%";'.format(a=contract_number, b=first_party, c=second_party))
        file_dir_all = PurchaseContract.objects.raw(sql)
        if file_dir_all:
            for i in file_dir_all:
                dic = {}
                dic['id'] = i.id
                dic['sole_id'] = i.id
                dic['contract_number'] = i.contract_number
                # dic['first_party'] = i.first_party
                # dic['second_party'] = i.second_party
                dic['update_time'] = i.upload_time.strftime('%Y-%m-%d')
                dic['file_name'] = i.file_name
                file_dir.append(dic)
        print(file_dir)
    return JsonResponse(file_dir, safe=False)

