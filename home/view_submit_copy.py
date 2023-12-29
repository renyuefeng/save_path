import json
import re
import time
import numpy as np
import tabula
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from smart_contract_manager.settings import MEDIA_ROOT
from .models import PurchaseContract, PurchaseContractTime, PurchaseContractDetails
from .pdfMethod import readDataFromPDF, pdf2image
from .fieldExtract import dealContractMessage
import datetime

name_dic = {'[产货]品名称|存货名称|名称': 'product_name', '产品规格|规格型号': 'product_specification', '单位': 'unit', '数量': 'quantity', '单价': 'unit_price', '总额|金额': 'gross_amount', '合计金额': 'total_amount', '税率': 'tax_rate'}

def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# 抽取文件字段
@require_http_methods(['POST'])
def get_files(request):
    dic = {'message': '', 'code': 200}
    # print(request.POST)
    # print(request.FILES)
    upload_file = request.FILES
    # upload_file = json.loads(upload_file)
    upload_file = request.FILES.get('file')
    print('upload_file', upload_file)
    start = time.time()
    if upload_file:

        # start_time = time.time()
        file_data = request.FILES['file']
        # uploader = request.POST.get('uploader')
        # end_time = time.time()
        # print(start_time - end_time, '传输文件: %.6f' % (end_time - start_time))
        #
        # start_time = time.time()
        newdoc = PurchaseContractTime(file_path=file_data, contract_sort='采购合同', file_name=str(upload_file))
        newdoc.save()
        # end_time = time.time()
        # print(start_time - end_time, '第一次存表: %.6f' % (end_time - start_time))

        # start_time = time.time()
        dic['fid'] = newdoc.id
        file_name = PurchaseContractTime.objects.get(id=newdoc.id).file_path
        # 读数据
        strings = readDataFromPDF(file_data)
        df1 = pd.DataFrame(columns=['product_name', 'product_specification', 'unit', 'quantity', 'unit_price', 'gross_amount', 'total_amount', 'tax_rate'])
        # dic1 = {}
        if strings == 0 or strings == '' or strings == ' ':
            df, strings = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=file_name), pic_path='{}/pic'.format(MEDIA_ROOT))

            # end_time = time.time()
            # print(start_time - end_time, '读取文件: %.6f' % (end_time - start_time))

        else:
            start_time = time.time()
            # pages = tabula.read_pdf('{a}/{b}'.format(a=MEDIA_ROOT, b=file_name), pages='all')
            # df = pd.concat(pages)
            # print(df.info())
            pages = tabula.read_pdf(file_data, pages='all')
            df = pd.concat(pages)
            end_time = time.time()
            print(start_time - end_time, '读取文件表格抽取信息: %.6f' % (end_time - start_time))
            # print(df.info())
            # df, strings = pdf2image(path='{a}/{b}'.format(a=MEDIA_ROOT, b=file_name), pic_path='{}/pic'.format(MEDIA_ROOT))
            #
        # else:
        #     try:
        #         form_pdf = readFormPdf(file_path)
        #         print(form_pdf)
        #     except:
        #         print('no form')

        # print(strings)
        product_name = np.nan
        # print(df.columns)
        # print(df.info())
        for i in name_dic.keys():
            pattern = re.compile(i)
            for j in df.columns:
                # print('j', j)
                if pattern.search(j):
                    df.rename(columns={j: name_dic[i]}, inplace=True)
        # print(df1.info())
        # print(df1.head())
        # print(df.info())
        df = pd.concat([df1, df])
        # print(df.info())

        # product_name = ','.join(list(set([v for v in df['product_name'].to_list() if pd.notna(v) and v])))
        # dic['product_name'] = product_name
        # pattern = re.compile('[产货]品名称')
        # print(df.columns)
        # for i in df.columns:
        #     if pattern.search(i):
        #         product_name = ','.join(list(set([v for v in df[i].to_list() if pd.notna(v) and v])))
        # print(product_name)

        # if dic1:
        #     for i in dic1.values():
        #         for key, value in i.items():
        #             if pattern.search(key):
        #                 product_name = ','.join(list(set([v for v in value if pd.notna(v) and v])))

        # 抽取对应字段
        start_time = time.time()

        dcm = dealContractMessage(strings)
        first_party = dcm.searchA()
        second_party = dcm.searchB()
        place_of_signing = dcm.searchSignPlace()
        time_of_signing = dcm.searchSignTime()
        delivery_time = dcm.searchDeliveryTime()
        delivery_place = dcm.searchDeliveryPlace()
        deliverer = dcm.searchDeliveryPeople()
        deliverer_phone = dcm.searchDeliveryPhone()
        money = dcm.select_money()

        # deliverer = re.sub(delivery_place, '', deliverer)
        # deliverer = re.sub(deliverer_phone, '', deliverer)
        payment_method = dcm.paymentMethod()
        dispute_resolution_method = dcm.disputeResolutionMethod()

        end_time = time.time()
        print(start_time - end_time, '抽取字段信息: %.6f' % (end_time - start_time))

        # start_time = time.time()

        save_data = PurchaseContract(
            first_party=first_party,
            second_party=second_party,
            sole_id=newdoc,
            place_of_signing=place_of_signing,
            time_of_signing=time_of_signing,
            delivery_time=delivery_time,
            delivery_place=delivery_place,
            deliverer=deliverer,
            deliverer_phone=deliverer_phone,
            payment_method=payment_method,
            dispute_resolution_method=dispute_resolution_method,
        )
        save_data.save()

        for index, row in df.iterrows():
            instance = PurchaseContractDetails(
                total_amount=money,
                product_name=row['product_name'],
                sole_id=newdoc,
                product_specification=row['product_specification'],
                unit=row['unit'],
                quantity=row['quantity'],
                unit_price=row['unit_price'],
                gross_amount=row['gross_amount'],
                tax_rate=row['tax_rate']
            )
            instance.save()

        # end_time = time.time()
        # print(start_time - end_time, '存表: %.6f' % (end_time - start_time))

        # save_data1 = PurchaseContractDetails(
        #     total_amount=money,
        #     product_name=product_name,
        #     sole_id=newdoc,
        #     product_specification=newdoc,
        # )
        # save_data1.save()

    else:
        dic['message'] = '文件不能为空'
        dic['code'] = 404
    print(dic)
    end_time = time.time()
    print(start - end_time, 'time cost: %.6f'%(start-end_time))

    return JsonResponse(dic)

# 显示文件内容，返回文件类型
@require_http_methods(['POST'])
def show_file(request):

    fid = request.body
    fid = json.loads(fid)
    fid = int(fid['fid'])
    main_constract = PurchaseContractTime.objects.get(id=fid)
    file_path = main_constract.file_path
    response = FileResponse(file_path)

    return response


# 显示详细信息
@require_http_methods(['POST'])
def show_file_message(request):
    info = {}
    fid = request.body
    fid = json.loads(fid)
    fid = int(fid['fid'])
    try:
    # if PurchaseContractTime.objects.get(id=fid):
        main_constract = PurchaseContractTime.objects.get(id=fid)
        # info = main_constract.purchase_contract.values()
        # info['data'] = list(info)[0]
        info['data'] = list(main_constract.purchase_contract.values())[0]
        # print('info', main_constract.purchase_contract_details.values())
        # print('info', len(main_constract.purchase_contract_details.values()))
        # print('info', info['data'])
        try:
            if main_constract.purchase_contract_details.values()[0]['total_amount']:
                info['data']['total_amount'] = main_constract.purchase_contract_details.values()[0]['total_amount']
            if main_constract.purchase_contract_details.values()[0]['product_name']:

                info['data']['product_name'] = ','.join(list(set([i['product_name'] for i in main_constract.purchase_contract_details.values()])))
                # print(info['data']['product_name'])
                # product_name = ','.join(list(set([v for v in df['product_name'].to_list() if pd.notna(v) and v])))
                # dic['product_name'] = product_name

            if main_constract.contract_sort:
                info['data']['contract_sort'] = main_constract.contract_sort
        except:
            pass
        # info['data1'] = list(main_constract.purchase_contract_details.values('money'))[0]
        info['contract_sort'] = main_constract.contract_sort
    except:
    # else:
        info = {}

    return JsonResponse(info, safe=False)
    # return response, dic
    # dcm = dcm.searchAAndB(str=dcm)

# 修改数据入库
@require_http_methods(['POST'])
def save_change_message(request):

    data = json.loads(request.body)
    contract_sort = data['contract_sort']
    data_details = {'total_amount': data['total_amount'], 'product_name': data['product_name']}
    data.pop('total_amount')
    data.pop('product_name')
    data.pop('contract_sort')
    sole_id_id = data['sole_id_id']
    tomorrow = datetime.datetime.strptime(data['time_of_signing'], '%Y-%m-%d')
    data['time_of_signing'] = tomorrow
    # for key, values in data.items():
    #     try:
    PurchaseContract.objects.filter(sole_id=sole_id_id).update(**data)
    newdic = PurchaseContractTime.objects.filter(id=sole_id_id)
    newdic.update(contract_sort=contract_sort)
        # except:
    # if PurchaseContractDetails.objects.filter(sole_id=sole_id_id):
    PurchaseContractDetails.objects.filter(sole_id=sole_id_id).update(**data_details)
    # else:
    #     save_data = PurchaseContractDetails(
    #         sole_id=newdic.all(),
    #         total_amount=data_details['total_amount'],
    #         product_name=data_details['product_name'],
    #     )
    #     save_data.save()


    dic = {'message': '', 'code': 200}

    return JsonResponse(dic, safe=False)
# print()

# if request.method == 'GET':
#     sql = 'SELECT * from ((SELECT first_party, second_party, contract_number from purchase_contract) A LEFT JOIN (SELECT contract_number, upload_time FROM purchase_contract_time) B ON A.contract_number=B.contract_number)'
#     main_info = PurchaseContract.objects.raw(sql)
#     # for j in main_info:
#     #     # j.enterprise_name = i.keyword
#     #     i.registration_status = j.registration_status
#     #     i.legal_representative = j.legal_representative
#     #     i.home_city = j.home_city
#     return JsonResponse({'main_info': main_info})
# else:
#     dic = {'message': ''}
#     # print(request.POST)
#
#     # print(request.body)
#     upload_file = request.FILES.get('upload_file')
#     # upload_file = request.body('upload_file', None)
#
#     if upload_file:
#     # if request.method == 'POST':
#         # 存储数据
#         # file_data = request.FILES['upload_file']
#         file_data = request.FILES['upload_file']
#         print(type(file_data))
#         # uploader = request.POST.get('uploader')
#         newdoc = PurchaseContractTime(file_data=file_data)
#         newdoc.save()
#
#         # 读数据
#         if readDataFromPDF(file_data):
#             str = readDataFromPDF(file_data)
#         else:
#             dic, str = pdf2image(file_data, pic_path='../pdfData')
#
#         # 抽取对应字段
#         dcm = dealContractMessage(str)
#         dcm = dcm.searchAAndB()
#         dcm = dcm.searchSignPlace()
#         dcm = dcm.searchSignTime()
#         dcm = dcm.searchDeliveryTime()
#         dcm = dcm.searchDeliveryPlace()
#         dcm = dcm.searchDeliveryPeople()
#         dcm = dcm.searchDeliveryPhone()
#
#         dic = dcm.to_dic()
#         # dcm = dcm.searchAAndB(str=dcm)
#     else:
#         dic['message'] = '文件不能为空'
#     return JsonResponse(dic)

# @require_POST
# def file_upload(request):
#     file = request.FILES.get('upload_file')
#
#     FileHandler.upload_file(FileHandler(), file=file)
#
#     return JsonResponse({"msg": "上传完成"})

# class FileHandler(FileHandlerABC):
#     def upload_file(self, file):
#
#         f_md5 = hashlib.md5(file.file.read()).hexdigest()
#         if FileList.objects.filter(file_md5=f_md5).exists():
#             return
#         f_fmt = file.name.split(".")[-1]
#         fl = FileList.objects.create()
#         fl.file_name = file.name
#         fl.file_md5 = f_md5
#         fl.file_path = file
#         fl.file_format = f_fmt
#
#         sheets = get_sheets(file, f_fmt)
#         for k, v in sheets.items():
#             fm = FileMapping.objects.create(file_target_id=fl.pk, file_sheet=k, file_col=",".join(v))
#             save_sheet(file, f_fmt, k, v, fm.pk, 0)
#         fl.save()
#
#     def __init__(self):
#         pass
