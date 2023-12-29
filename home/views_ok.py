import difflib
import json
import base64
import re
import time
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods

from smart_contract_manager.settings import MEDIA_ROOT
from .models import PurchaseContract, PurchaseContractTime
from .pdfMethod import readDataFromPDF, pdf2image
from .fieldExtract import dealContractMessage
import datetime
from concurrent.futures import ThreadPoolExecutor



dic_name = {'contract_number': '合同编号', 'first_party': '甲方', 'second_party': '乙方', 'place_of_signing': '签订地点',
            'time_of_signing': '签订时间', 'delivery_time': '交（提）货时间', 'delivery_place': '交（提）货地点', 'deliverer': '交货人',
            'deliverer_phone': '交货人联系方式', 'payment_method': '付款方式', 'dispute_resolution_method': '争议解决方式', 'total_amount': '合计金额',
            'product_name': '产品名称', 'money': '合计金额', 'contract_sort': '合同分类'}

def run_method(str1, str2, method='', data_time=False):
    if method:
        original = dealContractMessage(str1)
        submit = dealContractMessage(str2)
        first = eval('original.{}'.format(method))
        second = eval('submit.{}'.format(method))
    else:
        first = str1
        second = str2
    output = False
    if data_time == 0:
        if difflib.SequenceMatcher(None, first, second).ratio() < 0.55:
            output = {'a': first, 'b': second}
    else:
        if first != second:
            output = {'a': first, 'b': second}
    return output

@require_http_methods(['POST'])
def contract_submit(request):

    # dic = {'message': '', 'code': 200}
    original_file = request.FILES.get('original_file')
    submit_file = request.FILES.get('submit_file')

    # start = time.time()

    newdoc = PurchaseContractTime(file_path=original_file, contract_sort='purchase', file_name=str(original_file))
    newdoc.save()
    original_file = PurchaseContractTime.objects.get(id=newdoc.id).file_path

    newdoc = PurchaseContractTime(file_path=submit_file, contract_sort='purchase', file_name=str(submit_file))
    newdoc.save()
    # dic['fid'] = newdoc.id
    submit_file = PurchaseContractTime.objects.get(id=newdoc.id).file_path

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(readDataFromPDF, original_file)
        future2 = executor.submit(readDataFromPDF, submit_file)

    strings_original = future1.result()
    strings_submit = future2.result()

    # start_time = time.time()

    # strings_original = readDataFromPDF(original_file)
    if strings_original == 0 or strings_original == '' or strings_original == ' ':
        dic1, strings_original = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=original_file),
                                  pic_path='{}/pic'.format(MEDIA_ROOT))

    # end_time = time.time()
    # print(start_time - end_time, 'pdf1读取运行时长: %.6f' % (end_time - start_time))

    # start_time = time.time()

    # strings_submit = readDataFromPDF(submit_file)
    if strings_submit == 0 or strings_submit == '' or strings_submit == ' ':
        dic2, strings_submit = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=submit_file),
                                  pic_path='{}/pic'.format(MEDIA_ROOT))

    # end_time = time.time()
    # print(start_time - end_time, 'pdf2读取运行时长: %.6f' % (end_time - start_time))

    original_name = np.nan
    pattern = re.compile('产品名称')
    # print(dic1.info())
    # print(dic1.head())
    # for i in dic1.values():
    #     for key, value in i.items():
    #         if pattern.search(key):
    for i in dic1.columns:
        if pattern.search(i):
            original_name = list(set(dic1[i].tolist()))
    for i in dic2.columns:
        if pattern.search(i):
            submit_name = list(set(dic2[i].tolist()))
    # print(dic2.info())
    # print(dic2.head())
    # submit_name = np.nan
    # for i in dic2.values():
    #     for key, value in i.items():
    #         if pattern.search(key):
    #             submit_name = list(set([v for v in value if pd.notna(v) and v]))
    # else:
    #     try:
    #         form_pdf = readFormPdf(file_path)
    #         print(form_pdf)
    #     except:
    #         print('no form')
    # print(dic1)

    # 抽取对应字段
    # original = dealContractMessage(strings_original)
    ouput = []
    dic1 = {}
    dic2 = {}
    # submit = dealContractMessage(strings_submit)
    lis = run_method(strings_original, strings_submit, 'searchA()')
    if lis:
        lis['key'] = dic_name['first_party']
        ouput.append(lis)
        # dic1['first_party'] = lis[0]
        # dic2['first_party'] = lis[1]
    lis = run_method(strings_original, strings_submit, 'searchB()')
    if lis:
        lis['key'] = dic_name['second_party']
        ouput.append(lis)
        # dic1['second_party'] = lis[0]
        # dic2['second_party'] = lis[1]
    lis = run_method(strings_original, strings_submit, 'searchSignPlace()')
    if lis:
        lis['key'] = dic_name['place_of_signing']
        ouput.append(lis)
        # dic1['place_of_signing'] = lis[0]
        # dic2['place_of_signing'] = lis[1]

    lis = run_method(strings_original, strings_submit, 'searchSignTime(out_put_type="string")', data_time=True)
    if lis:
        lis['key'] = dic_name['time_of_signing']
        ouput.append(lis)
        # if lis[0]:
        #     dic1['time_of_signing'] = lis[0].strftime('%Y-%m-%d')
        # if lis[1]:
        #     dic2['time_of_signing'] = lis[1].strftime('%Y-%m-%d')
    lis = run_method(strings_original, strings_submit, 'searchDeliveryTime()', data_time=True)
    if lis:
        lis['key'] = dic_name['delivery_time']
        ouput.append(lis)
        # dic1['delivery_time'] = lis[0]
        # dic2['delivery_time'] = lis[1]

    lis = run_method(strings_original, strings_submit, 'searchDeliveryPlace()')
    if lis:
        lis['key'] = dic_name['delivery_place']
        ouput.append(lis)
        # dic1['delivery_place'] = lis[0]
        # dic2['delivery_place'] = lis[1]
    lis = run_method(strings_original, strings_submit, 'searchDeliveryPeople()')
    if lis:
        lis['key'] = dic_name['deliverer']
        ouput.append(lis)
        # dic1['deliverer'] = lis[0]
        # dic2['deliverer'] = lis[1]
    lis = run_method(strings_original, strings_submit, 'searchDeliveryPhone()')
    if lis:
        lis['key'] = dic_name['deliverer_phone']
        ouput.append(lis)

    lis = run_method(strings_original, strings_submit, 'select_money()', data_time=True)
    if lis:
        lis['key'] = dic_name['money']
        ouput.append(lis)

    # lis_submit = {}
    # lis = run_method(original_name, submit_name)
    lis_mid = []
    for i in original_name:
        for j in submit_name:
            if i == j:
                lis_mid.append(i)
    for i in lis_mid:
        original_name.remove(i)
        submit_name.remove(i)
    lis_submit = {'a': ','.join(original_name), 'b': ','.join(submit_name), 'c': ','.join(lis_mid)}
    if lis_submit:
        lis_submit['key'] = dic_name['product_name']
        ouput.append(lis_submit)
        # dic1['deliverer_phone'] = lis[0]
        # dic2['deliverer_phone'] = lis[1]
    # first_party = original.searchA()
    # second_party = original.searchB()
    # place_of_signing = original.searchSignPlace()
    # time_of_signing = original.searchSignTime()
    # delivery_time = original.searchDeliveryTime()
    # delivery_place = original.searchDeliveryPlace()
    # deliverer = original.searchDeliveryPeople()
    # deliverer_phone = original.searchDeliveryPhone()
    # # deliverer = re.sub(delivery_place, '', deliverer)
    # # deliverer = re.sub(deliverer_phone, '', deliverer)
    # payment_method = original.paymentMethod()
    # dispute_resolution_method = original.disputeResolutionMethod()
    # ouput.append(dic1)
    # ouput.append(dic2)
    # ouput.append(lis)
    # print(ouput)
    # end_time = time.time()
    # print(start - end_time, '运行时长: %.6f' % (end_time - start_time))

    return JsonResponse(ouput, safe=False)


@require_http_methods(['POST'])
def select_contract_submit(request):

    # fid = request.body
    # fid = json.loads(fid)
    # fid1 = int(fid['fid1'])
    # fid2 = int(fid['fid2'])
    fid1 = request.POST.get('fid1')
    fid2 = request.POST.get('fid2')

    first_contract = PurchaseContractTime.objects.get(id=fid1)
    second_contract = PurchaseContractTime.objects.get(id=fid2)
    print(first_contract.purchase_contract.values()[0]['first_party'])
    print(type(first_contract.purchase_contract.values()[0]['first_party']))
    # lis = run_method(str1=first_contract., strings_submit)
    ouput = []
    dic1 = {}
    dic2 = {}
    # submit = dealContractMessage(strings_submit)
    lis = run_method(str1=first_contract.purchase_contract.values()[0]['first_party'], str2=second_contract.purchase_contract.values()[0]['first_party'])
    if lis:
        lis['key'] = dic_name['first_party']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['second_party'], str2=second_contract.purchase_contract.values()[0]['second_party'])
    if lis:
        lis['key'] = dic_name['second_party']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['place_of_signing'], str2=second_contract.purchase_contract.values()[0]['place_of_signing'])
    if lis:
        lis['key'] = dic_name['place_of_signing']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['time_of_signing'].strftime('%Y-%m-%d'), str2=second_contract.purchase_contract.values()[0]['time_of_signing'].strftime('%Y-%m-%d'), data_time=True)
    if lis:
        lis['key'] = dic_name['time_of_signing']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['delivery_time'], str2=second_contract.purchase_contract.values()[0]['delivery_time'], data_time=True)
    if lis:
        lis['key'] = dic_name['delivery_time']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['delivery_place'], str2=second_contract.purchase_contract.values()[0]['delivery_place'])
    if lis:
        lis['key'] = dic_name['delivery_place']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['deliverer'], str2=second_contract.purchase_contract.values()[0]['deliverer'])
    if lis:
        lis['key'] = dic_name['deliverer']
        ouput.append(lis)

    lis = run_method(str1=first_contract.purchase_contract.values()[0]['deliverer_phone'], str2=second_contract.purchase_contract.values()[0]['deliverer_phone'])
    if lis:
        lis['key'] = dic_name['deliverer_phone']
        ouput.append(lis)

    # lis = run_method(str1=first_contract.purchase_contract_details.values()[0]['total_amount'], str2=second_contract.purchase_contract_details.values()[0]['total_amount'])
    # if lis:
    #     lis['key'] = dic_name['total_amount']
    #     ouput.append(lis)

    # print(ouput)

    return JsonResponse(ouput, safe=False)
